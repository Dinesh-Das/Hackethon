# main.py
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter, ArrayQueryParameter

app = Flask(__name__)
CORS(app)

# Use a global client to manage connections efficiently
try:
    client = bigquery.Client()
    PROJECT_ID = os.environ.get("GCP_PROJECT", client.project)
except Exception as e:
    print(f"Could not initialize BigQuery Client. Ensure you have authenticated. Error: {e}")
    # Fallback for local development without default project
    PROJECT_ID = "prj-hk25-team-3-a" 
    client = bigquery.Client(project=PROJECT_ID)

DATASET_ID = "CleanDS"
MODEL_NAME = "ItemEmbeddingModel"
DETAILS_TABLE = "ProductDetails"
TABLE_FQN = f"`{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}`"
MODEL_FQN = f"`{PROJECT_ID}.{DATASET_ID}.{MODEL_NAME}`"


@app.route("/")
def index():
    """Renders the main HTML page."""
    return render_template("index.html")

# === START: NEW ENDPOINT FOR MODEL EVALUATION ===
@app.route("/model_evaluation", methods=["GET"])
def get_model_evaluation():
    """
    Evaluates the recommendation model and returns its performance metrics.
    For Matrix Factorization, a key metric is Mean Squared Error (MSE), where lower is better.
    """
    eval_query = f"SELECT * FROM ML.EVALUATE(MODEL {MODEL_FQN})"
    
    try:
        query_job = client.query(eval_query)
        # ML.EVALUATE returns one row of metrics
        results = [dict(row) for row in query_job.result()]
        
        if not results:
            return jsonify({"error": "Model evaluation returned no results."}), 404
            
        # Return the first row of metrics
        return jsonify(results[0]), 200

    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500
# === END: NEW ENDPOINT ===


@app.route("/products", methods=["GET"])
def get_all_products():
    """Fetches a paginated list of all products available in the recommendation model."""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    offset = (page - 1) * size
    try:
        count_query = f"SELECT COUNT(*) as total FROM {TABLE_FQN}"
        count_job = client.query(count_query)
        total_rows = list(count_job.result())[0]['total']

        data_query = f"""
            WITH ModelSKUs AS (
              SELECT feature AS SKU_CODE
              FROM ML.WEIGHTS(MODEL {MODEL_FQN})
              WHERE processed_input = 'SKU_CODE'
            )
            SELECT
              details.SKU_CODE, details.PRODUCT_Name, details.CATEGORY, details.SUB_CATEGORY, details.TAGS, details.COLLECTIVE_SET
            FROM {TABLE_FQN} AS details
            INNER JOIN ModelSKUs ON details.SKU_CODE = ModelSKUs.SKU_CODE
            ORDER BY details.SKU_CODE
            LIMIT @size OFFSET @offset;
        """
        job_config = QueryJobConfig(query_parameters=[
            ScalarQueryParameter("size", "INT64", size),
            ScalarQueryParameter("offset", "INT64", offset),
        ])
        query_job = client.query(data_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]
        return jsonify({"products": results, "total": total_rows}), 200
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500


@app.route("/cart_recommendations", methods=["POST"])
def get_cart_recommendations():
    """
    API endpoint to get recommendations based on a list of SKUs in the cart.
    It now identifies the source product and the *specific* reason for the recommendation.
    """
    request_json = request.get_json(silent=True)
    if not request_json or 'skus' not in request_json or not request_json['skus']:
        return jsonify({"recommendations": []})

    cart_skus = request_json['skus']

    recommendations_query = f"""
        WITH
          ProductEmbeddings AS (
            SELECT feature AS SKU_CODE, (SELECT ARRAY_AGG(weight) FROM UNNEST(factor_weights)) AS embedding
            FROM ML.WEIGHTS(MODEL {MODEL_FQN})
            WHERE processed_input = 'SKU_CODE'
          ),
          CartAverageEmbedding AS (
            SELECT
              ARRAY(
                SELECT AVG(e)
                FROM UNNEST(t.embedding) AS e WITH OFFSET AS i
                GROUP BY i ORDER BY i
              ) AS avg_embedding
            FROM ProductEmbeddings t
            WHERE t.SKU_CODE IN UNNEST(@cart_skus)
          )
        SELECT
            other_products.SKU_CODE as recommended_sku_code,
            details.PRODUCT_Name,
            details.CATEGORY,
            details.SUB_CATEGORY,
            details.TAGS,
            details.COLLECTIVE_SET,
            (1 - ML.DISTANCE(cart.avg_embedding, other_products.embedding, 'COSINE')) AS similarity_score
        FROM
            ProductEmbeddings AS other_products,
            CartAverageEmbedding AS cart
        JOIN
            {TABLE_FQN} AS details
            ON details.SKU_CODE = other_products.SKU_CODE
        WHERE
            other_products.SKU_CODE NOT IN UNNEST(@cart_skus)
        ORDER BY
            similarity_score DESC
        LIMIT 10;
        """
    job_config = QueryJobConfig(
        query_parameters=[ArrayQueryParameter("cart_skus", "STRING", cart_skus)]
    )

    try:
        rec_job = client.query(recommendations_query, job_config=job_config)
        recommendations = [dict(row) for row in rec_job.result()]

        if not recommendations:
            return jsonify({"recommendations": []}), 200

        cart_details_query = f"""
            SELECT SKU_CODE, PRODUCT_Name, CATEGORY, SUB_CATEGORY, TAGS
            FROM {TABLE_FQN}
            WHERE SKU_CODE IN UNNEST(@cart_skus)
        """
        cart_details_job = client.query(cart_details_query, job_config=job_config)
        cart_items_details = [dict(row) for row in cart_details_job.result()]
        
        for rec_product in recommendations:
            rec_product['recommendation_reason'] = "Similar Style"
            rec_product['recommended_from_product_name'] = ""

            reason_found = False
            for cart_item in cart_items_details:
                if cart_item.get('CATEGORY') and rec_product.get('CATEGORY') == cart_item.get('CATEGORY'):
                    rec_product['recommendation_reason'] = f"Shared Category: '{rec_product.get('CATEGORY')}'"
                    rec_product['recommended_from_product_name'] = cart_item['PRODUCT_Name']
                    reason_found = True
                    break
            
            if reason_found: continue

            for cart_item in cart_items_details:
                if cart_item.get('SUB_CATEGORY') and rec_product.get('SUB_CATEGORY') == cart_item.get('SUB_CATEGORY'):
                    rec_product['recommendation_reason'] = f"Shared Sub-Category: '{rec_product.get('SUB_CATEGORY')}'"
                    rec_product['recommended_from_product_name'] = cart_item['PRODUCT_Name']
                    reason_found = True
                    break

            if reason_found: continue

            rec_tags = set(str(rec_product.get('TAGS', '') or '').replace(" ", "").split(','))
            rec_tags.discard('')
            if rec_tags:
                for cart_item in cart_items_details:
                    cart_tags = set(str(cart_item.get('TAGS', '') or '').replace(" ", "").split(','))
                    shared_tags = rec_tags.intersection(cart_tags)
                    if shared_tags:
                        tag_example = next(iter(shared_tags)).strip().title()
                        rec_product['recommendation_reason'] = f"Shares Tag: '{tag_example}'"
                        rec_product['recommended_from_product_name'] = cart_item['PRODUCT_Name']
                        reason_found = True
                        break
        
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        print(f"An error occurred during recommendation: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
