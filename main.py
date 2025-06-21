# main.py
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter, ArrayQueryParameter

app = Flask(__name__)
CORS(app)
client = bigquery.Client()

PROJECT_ID = os.environ.get("GCP_PROJECT", "prj-hk25-team-3-a")
DATASET_ID = "CleanDS"
MODEL_NAME = "ItemEmbeddingModel"
DETAILS_TABLE = "ProductDetails"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products", methods=["GET"])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    offset = (page - 1) * size
    try:
        count_query = f"SELECT COUNT(*) as total FROM `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}`"
        count_job = client.query(count_query)
        total_rows = list(count_job.result())[0]['total']
        
        # --- MODIFIED TO FETCH MORE COLUMNS ---
        data_query = f"""
            SELECT 
                SKU_CODE, PRODUCT_Name, CATEGORY, 
                SubCategory, Tags, Collective_Tags
            FROM `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}`
            ORDER BY SKU_CODE
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
    request_json = request.get_json(silent=True)
    if not request_json or 'skus' not in request_json or not request_json['skus']:
        return jsonify({"recommendations": []})

    cart_skus = request_json['skus']
    print(f"Received request for cart recommendations with SKUs: {cart_skus}")

    # --- MODIFIED TO FETCH MORE COLUMNS FOR RECOMMENDATIONS ---
    sql_query = f"""
        WITH
        ProductEmbeddings AS (
            SELECT feature AS SKU_CODE, (SELECT ARRAY_AGG(weight ORDER BY factor) FROM UNNEST(factor_weights)) AS embedding
            FROM ML.WEIGHTS(MODEL `{PROJECT_ID}.{DATASET_ID}.{MODEL_NAME}`)
            WHERE processed_input = 'SKU_CODE'
        ),
        ValidCartEmbeddings AS (
            SELECT embedding FROM ProductEmbeddings WHERE SKU_CODE IN UNNEST(@cart_skus)
        ),
        CartAverageEmbedding AS (
            SELECT ARRAY(SELECT AVG(e.value) FROM UNNEST(t.embedding) AS e WITH OFFSET AS i GROUP BY i ORDER BY i) AS avg_embedding
            FROM ValidCartEmbeddings t
        )
        SELECT
            other_products.SKU_CODE as recommended_sku_code,
            details.PRODUCT_Name,
            details.CATEGORY,
            details.SubCategory,  -- Added
            details.Tags,         -- Added
            details.Collective_Tags, -- Added
            (1 - ML.DISTANCE(cart.avg_embedding, other_products.embedding, 'COSINE')) AS similarity_score
        FROM
            ProductEmbeddings AS other_products,
            CartAverageEmbedding AS cart
        JOIN
            `{PROJECT_ID}.{DATASET_ID}.{DETAILS_TABLE}` AS details
            ON details.SKU_CODE = other_products.SKU_CODE
        WHERE
            cart.avg_embedding IS NOT NULL AND
            other_products.SKU_CODE NOT IN UNNEST(@cart_skus)
        ORDER BY
            similarity_score DESC
        LIMIT 10;
    """
    job_config = QueryJobConfig(query_parameters=[ArrayQueryParameter("cart_skus", "STRING", cart_skus)])
    try:
        query_job = client.query(sql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]
        return jsonify({"recommendations": results}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
