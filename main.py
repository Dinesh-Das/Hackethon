import pandas as pd
from flask import Flask, request, jsonify, render_template
from collections import defaultdict

app = Flask(__name__)

# Load and preprocess the dataset
try:
    products_df = pd.read_csv('products.csv', encoding='utf-8')
except UnicodeDecodeError:
    products_df = pd.read_csv('products.csv', encoding='latin1')

# Fill NaN values to prevent errors during string operations
products_df.fillna('', inplace=True)

@app.route('/')
def index():
    """Render the main page."""
    products = products_df.to_dict(orient='records')
    return render_template('index.html', products=products)

@app.route('/cart_recommendations', methods=['POST'])
def get_cart_recommendations():
    """Generate recommendations based on items in the cart."""
    cart_data = request.json
    cart_skus = [item['sku'] for item in cart_data]
    
    if not cart_skus:
        return jsonify([])

    cart_products = products_df[products_df['SKU_CODE'].isin(cart_skus)]
    if cart_products.empty:
        return jsonify([])

    # Use defaultdict to handle scores for products not yet in the dict
    similarity_scores = defaultdict(lambda: {'score': 0, 'reasons': set()})

    # --- Scoring Logic ---
    # Iterate through each item in the cart to find similar products
    for index, cart_product in cart_products.iterrows():
        cart_tags = set(str(cart_product.get('TAGS', '')).split(', '))

        # Iterate through all products in the dataset to compare
        for idx, p in products_df.iterrows():
            # Skip items already in the cart
            if p['SKU_CODE'] in cart_skus:
                continue

            score = 0
            # 1. Compare CATEGORY (highest weight)
            if p['CATEGORY'] and p['CATEGORY'] == cart_product['CATEGORY']:
                score += 3
            
            # 2. Compare SUB_CATEGORY (medium weight)
            if p['SUB_CATEGORY'] and p['SUB_CATEGORY'] == cart_product['SUB_CATEGORY']:
                score += 2
            
            # 3. Compare TAGS (lower weight)
            product_tags = set(str(p.get('TAGS', '')).split(', '))
            shared_tags_count = len(cart_tags.intersection(product_tags))
            score += shared_tags_count

            if score > 0:
                similarity_scores[p['SKU_CODE']]['score'] += score

    # Sort recommendations by score
    sorted_recommendations = sorted(
        similarity_scores.items(), key=lambda item: item[1]['score'], reverse=True
    )
    
    # Get top N recommendations (e.g., top 10)
    N = 10
    top_n_recommendations = []
    cart_products_list = cart_products.to_dict(orient='records')

    for sku, data in sorted_recommendations:
        if len(top_n_recommendations) >= N:
            break

        recommended_product_info = products_df[products_df['SKU_CODE'] == sku].iloc[0].to_dict()
        
        # === START: New Logic for Recommendation Reason ===
        reason = "Based on items in your cart." # Fallback reason
        matched_category = False
        matched_sub_category = False
        
        # Priority 1: Check for Category match
        for cart_item in cart_products_list:
            if recommended_product_info['CATEGORY'] and recommended_product_info['CATEGORY'] == cart_item['CATEGORY']:
                reason = f"Because you like the '{cart_item['CATEGORY']}' category."
                matched_category = True
                break
        
        # Priority 2: Check for Sub-Category match
        if not matched_category:
            for cart_item in cart_products_list:
                if recommended_product_info['SUB_CATEGORY'] and recommended_product_info['SUB_CATEGORY'] == cart_item['SUB_CATEGORY']:
                    reason = f"Because you like the '{cart_item['SUB_CATEGORY']}' sub-category."
                    matched_sub_category = True
                    break

        # Priority 3: Check for shared tags
        if not matched_category and not matched_sub_category:
            recommended_tags = set(str(recommended_product_info.get('TAGS', '')).split(', '))
            cart_tags = set()
            for item in cart_products_list:
                cart_tags.update(str(item.get('TAGS', '')).split(', '))
            
            # Remove empty strings that might result from splitting
            recommended_tags.discard('')
            cart_tags.discard('')

            shared_tags = recommended_tags.intersection(cart_tags)
            if shared_tags:
                reason = f"Shares tags like '{next(iter(shared_tags))}' with items in your cart."
        # === END: New Logic for Recommendation Reason ===

        top_n_recommendations.append({
            "recommended_sku_code": sku,
            "PRODUCT_Name": recommended_product_info["PRODUCT_Name"],
            "CATEGORY": recommended_product_info["CATEGORY"],
            "SUB_CATEGORY": recommended_product_info["SUB_CATEGORY"],
            "TAGS": recommended_product_info["TAGS"],
            "COLLECTIVE_SET": recommended_product_info["COLLECTIVE_SET"],
            "similarity_score": data['score'],
            "recommendation_reason": reason  # Add the new field
        })
        
    return jsonify(top_n_recommendations)

if __name__ == '__main__':
    app.run(debug=True)
