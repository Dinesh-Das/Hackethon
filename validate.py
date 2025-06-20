# import json

# def feature_comparison(json_file, target_sku_code):
#     # Load the JSON data
#     with open(json_file, 'r') as file:
#         products = json.load(file)

#     # Find the target product
#     target_product = next((p for p in products if p['SKU_CODE'] == target_sku_code), None)
#     if not target_product:
#         print(f"Target SKU_CODE {target_sku_code} not found.")
#         return

#     target_tags = set(json.loads(target_product['TAGS']))
#     target_sets = set(json.loads(target_product['COLLECTIVE_SET']))

#     # Compare features
#     for product in products:
#         if product['SKU_CODE'] == target_sku_code:
#             continue

#         product_tags = set(json.loads(product['TAGS']))
#         product_sets = set(json.loads(product['COLLECTIVE_SET']))

#         shared_tags = target_tags & product_tags
#         unique_tags = product_tags - target_tags
#         shared_sets = target_sets & product_sets
#         unique_sets = product_sets - target_sets

#         print(f"SKU_CODE: {product['SKU_CODE']}")
#         print(f"PRODUCT_NAME: {product['PRODUCT_NAME']}")
#         print(f"Shared Tags: {list(shared_tags)}")
#         print(f"Unique Tags: {list(unique_tags)}")
#         print(f"Shared Sets: {list(shared_sets)}")
#         print(f"Unique Sets: {list(unique_sets)}")
#         print("-" * 50)

# # Example usage
# feature_comparison('products.json', 'SKU1000')

import json

def feature_comparison(json_file, target_sku_code):
    # Load the JSON data
    with open(json_file, 'r') as file:
        products = json.load(file)

    # Find the target product
    target_product = next((p for p in products if p['SKU_CODE'] == target_sku_code), None)
    if not target_product:
        print(f"Target SKU_CODE {target_sku_code} not found.")
        return

    target_tags = set(json.loads(target_product['TAGS']))
    target_sets = set(json.loads(target_product['COLLECTIVE_SET']))

    # Prepare the comparison table
    comparison_table = []

    for product in products:
        if product['SKU_CODE'] == target_sku_code:
            continue

        product_tags = set(json.loads(product['TAGS']))
        product_sets = set(json.loads(product['COLLECTIVE_SET']))

        shared_tags = target_tags & product_tags
        unique_tags = product_tags - target_tags
        shared_sets = target_sets & product_sets
        unique_sets = product_sets - target_sets

        correct = len(shared_tags) > 0 and len(shared_sets) > 0

        comparison_table.append({
            "SKU_CODE": product['SKU_CODE'],
            "PRODUCT_NAME": product['PRODUCT_NAME'],
            "Shared Tags": list(shared_tags),
            "Unique Tags": list(unique_tags),
            "Shared Sets": list(shared_sets),
            "Unique Sets": list(unique_sets),
            "Correct Recommendation": correct
        })

    # Print the comparison table
    for row in comparison_table:
        print(f"SKU_CODE: {row['SKU_CODE']}")
        print(f"PRODUCT_NAME: {row['PRODUCT_NAME']}")
        print(f"Shared Tags: {row['Shared Tags']}")
        print(f"Unique Tags: {row['Unique Tags']}")
        print(f"Shared Sets: {row['Shared Sets']}")
        print(f"Unique Sets: {row['Unique Sets']}")
        print(f"Correct Recommendation: {row['Correct Recommendation']}")
        print("-" * 50)

# Example usage
feature_comparison('products.json', 'SKU1000')

