import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS for all routes, allowing your Streamlit app to call it
CORS(app) 

# Initialize the BigQuery client
client = bigquery.Client()

# Get project details from environment variables for better practice
PROJECT_ID = os.environ.get("GCP_PROJECT", "prj-hk25-team-3-a")
DATASET_ID = "CleanDS"
MODEL_NAME = "ItemEmbeddingModel"
DETAILS_TABLE = "ProductDetails"

@app.route("/recommend", methods=["POST"])
def get_recommendations():
    """API endpoint to get product recommendations."""
    request_json = request.get_json(silent=True)
    if not request_json or 'sku' not in request_json:
        return jsonify({"error": "JSON payload with 'sku' key is required."}), 400

    target_sku = request_json['sku']

    sql_query = f"""
        # ... (Your BigQuery SQL from before remains exactly the same) ...
        WITH ProductEmbeddings AS (
          SELECT
            feature AS SKU_CODE,
            (SELECT ARRAY_AGG(weight ORDER BY factor) FROM UNNEST(factor_weights)) AS embedding
          FROM ML.WEIGHTS(MODEL `{PROJECT_ID}.{DATASET_ID}.{MODEL_NAME}`)
          WHERE processed_input = 'SKU_CODE'
        ),
        Recommendations AS (
          SELECT
            other_products.SKU_CODE AS recommended_sku_code,
            (1 - ML.DISTANCE(target_product.embedding, other_products.embedding, 'COSINE')) AS similarity_score
          FROM ProductEmbeddings AS target_product, ProductEmbeddings AS other_products
          WHERE target_product.SKU_CODE = @target_sku AND target_product.SKU_CODE != other_products.SKU_CODE
          ORDER BY similarity_score DESC
          LIMIT 10
        )
        SELECT
          rec.recommended_sku_code, rec.similarity_score, details.PRODUCT_DESCRIPTION,
          details.CATEGORY, details.SUB_CATEGORY, details.COLOUR
        FROM Recommendations AS rec
        JOIN `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}` AS details
        ON rec.recommended_sku_code = details.SKU_CODE
        ORDER BY rec.similarity_score DESC;
    """

    job_config = QueryJobConfig(query_parameters=[ScalarQueryParameter("target_sku", "STRING", target_sku)])

    try:
        query_job = client.query(sql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]
        if not results:
            return jsonify({"message": "No recommendations found."}), 404
        return jsonify({"recommendations": results}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error."}), 500

# This is the entry point for the Gunicorn server in the container
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
