# # main.py
# import os
# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from google.cloud import bigquery
# from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter

# # Initialize the Flask app
# app = Flask(__name__)
# # Enable CORS for all routes
# CORS(app)

# # Initialize the BigQuery client
# client = bigquery.Client()

# # Get project details from environment variables for best practice
# PROJECT_ID = os.environ.get("GCP_PROJECT", "prj-hk25-team-3-a")
# DATASET_ID = "CleanDS"
# MODEL_NAME = "ItemEmbeddingModel"
# DETAILS_TABLE = "ProductDetails"

# @app.route("/")
# def index():
#     """Serves the frontend HTML file."""
#     return render_template("index.html")

# @app.route("/recommend", methods=["POST"])
# def get_recommendations():
#     """API endpoint to get product recommendations."""
#     request_json = request.get_json(silent=True)
#     if not request_json or 'sku' not in request_json:
#         return jsonify({"error": "JSON payload with 'sku' key is required."}), 400

#     target_sku = request_json['sku']

#     # Note: The column name was corrected to PRODUCT_Name
#     # Ensure this column exists in your `ProductDetails` table.
#     sql_query = f"""
#         WITH ProductEmbeddings AS (
#           SELECT
#             feature AS SKU_CODE,
#             (SELECT ARRAY_AGG(weight ORDER BY factor) FROM UNNEST(factor_weights)) AS embedding
#           FROM ML.WEIGHTS(MODEL `{PROJECT_ID}.{DATASET_ID}.{MODEL_NAME}`)
#           WHERE processed_input = 'SKU_CODE'
#         ),
#         Recommendations AS (
#           SELECT
#             other_products.SKU_CODE AS recommended_sku_code,
#             (1 - ML.DISTANCE(target_product.embedding, other_products.embedding, 'COSINE')) AS similarity_score
#           FROM ProductEmbeddings AS target_product, ProductEmbeddings AS other_products
#           WHERE target_product.SKU_CODE = @target_sku AND target_product.SKU_CODE != other_products.SKU_CODE
#           ORDER BY similarity_score DESC
#           LIMIT 10
#         )
#         SELECT
#           rec.recommended_sku_code,
#           rec.similarity_score,
#           details.PRODUCT_Name,
#           details.CATEGORY,
#           details.SUB_CATEGORY,
#           details.COLOUR
#         FROM Recommendations AS rec
#         JOIN `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}` AS details
#         ON rec.recommended_sku_code = details.SKU_CODE
#         ORDER BY rec.similarity_score DESC;
#     """

#     job_config = QueryJobConfig(query_parameters=[ScalarQueryParameter("target_sku", "STRING", target_sku)])

#     try:
#         query_job = client.query(sql_query, job_config=job_config)
#         results = [dict(row) for row in query_job.result()]
#         if not results:
#             return jsonify({"message": f"No recommendations found for SKU '{target_sku}'. It might not exist in the model."}), 404
#         return jsonify({"recommendations": results}), 200
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": f"An internal server error occurred: {e}"}), 500

# # This is the entry point for Gunicorn in Cloud Run
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


# main.py
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter, ArrayQueryParameter

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Initialize the BigQuery client
client = bigquery.Client()

# Project details
PROJECT_ID = os.environ.get("GCP_PROJECT", "prj-hk25-team-3-a")
DATASET_ID = "CleanDS"
MODEL_NAME = "ItemEmbeddingModel"
DETAILS_TABLE = "ProductDetails"

@app.route("/")
def index():
    """Serves the main interactive frontend HTML file."""
    return render_template("index.html")

@app.route("/products", methods=["GET"])
def get_all_products():
    """Fetches a list of products to display on the main page."""
    try:
        # A simple query to get products for the user to browse.
        # We limit it to 30 for performance. You could add pagination later.
        query = f"""
            SELECT SKU_CODE, PRODUCT_Name, CATEGORY
            FROM `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}`
            ORDER BY SKU_CODE
            LIMIT 30;
        """
        query_job = client.query(query)
        results = [dict(row) for row in query_job.result()]
        return jsonify({"products": results}), 200
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500


@app.route("/cart_recommendations", methods=["POST"])
def get_cart_recommendations():
    """
    API endpoint to get recommendations based on a list of SKUs in the cart.
    It works by averaging the embeddings of all items in the cart to find
    products that match the user's overall taste.
    """
    request_json = request.get_json(silent=True)
    if not request_json or 'skus' not in request_json or not request_json['skus']:
        return jsonify({"recommendations": []}) # Return empty list if cart is empty

    cart_skus = request_json['skus']
    
    # This SQL query is more advanced. It calculates the average embedding of all cart items.
    sql_query = f"""
        WITH
          ProductEmbeddings AS (
            SELECT feature AS SKU_CODE, (SELECT ARRAY_AGG(weight ORDER BY factor) FROM UNNEST(factor_weights)) AS embedding
            FROM ML.WEIGHTS(MODEL `{PROJECT_ID}.{DATASET_ID}.{MODEL_NAME}`)
            WHERE processed_input = 'SKU_CODE'
          ),
          CartAverageEmbedding AS (
            -- 1. Get embeddings for items in the cart
            SELECT
              -- 2. Average the embedding vectors to create a "prototype" vector for the user's taste
              ARRAY(
                SELECT AVG(e.value)
                FROM UNNEST(t.embedding) AS e WITH OFFSET AS i
                GROUP BY i
                ORDER BY i
              ) AS avg_embedding
            FROM ProductEmbeddings t
            WHERE t.SKU_CODE IN UNNEST(@cart_skus)
          )
        -- 3. Find items closest to this average embedding
        SELECT
            other_products.SKU_CODE as recommended_sku_code,
            details.PRODUCT_Name,
            details.CATEGORY,
            (1 - ML.DISTANCE(cart.avg_embedding, other_products.embedding, 'COSINE')) AS similarity_score
        FROM
            ProductEmbeddings AS other_products,
            CartAverageEmbedding AS cart
        JOIN
            `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}` AS details
            ON details.SKU_CODE = other_products.SKU_CODE
        WHERE
            -- 4. Exclude items already in the cart from the recommendations
            other_products.SKU_CODE NOT IN UNNEST(@cart_skus)
        ORDER BY
            similarity_score DESC
        LIMIT 10;
        """

    job_config = QueryJobConfig(
        query_parameters=[
            ArrayQueryParameter("cart_skus", "STRING", cart_skus)
        ]
    )

    try:
        query_job = client.query(sql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]
        return jsonify({"recommendations": results}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
