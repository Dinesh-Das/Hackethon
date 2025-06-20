import streamlit as st
import pandas as pd
import requests
from google.cloud import bigquery

# --- Page Configuration ---
st.set_page_config(
    page_title="Product Recommender",
    page_icon="🛍️",
    layout="wide"
)

# --- Configuration ---
# This is the API endpoint URL you got after deploying the Cloud Function
API_URL = "YOUR_CLOUD_FUNCTION_TRIGGER_URL_HERE" 
GCP_PROJECT_ID = "prj-hk25-team-3-a"

# --- Caching ---
# Cache the data loading to prevent re-running it on every interaction
@st.cache_data
def load_product_data():
    """Connects to BigQuery and fetches a list of all product SKUs and names."""
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        # NOTE: For a production app with many products, you'd want to paginate or search.
        # For this demo, we fetch a sample.
        query = """
            SELECT SKU_CODE, PRODUCT_DESCRIPTION
            FROM `prj-hk25-team-3-a.CleanDS.ProductDetails`
            ORDER BY SKU_CODE
            LIMIT 5000 
        """
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        st.error(f"Error connecting to BigQuery: {e}")
        return pd.DataFrame()

# --- Main App ---
st.title("🛍️ AI-Powered Product Recommender")
st.markdown("Select a product to see similar items recommended by our Matrix Factorization model.")

# --- Load Data ---
product_df = load_product_data()

if not product_df.empty:
    # --- User Input Section ---
    st.header("1. Select a Product")
    
    # Create a list of options for the selectbox, combining SKU and description
    product_options = product_df.apply(lambda row: f"{row['SKU_CODE']} - {row['PRODUCT_DESCRIPTION']}", axis=1).tolist()
    
    selected_option = st.selectbox(
        "Choose a product from the list:",
        options=product_options,
        index=0 # Default to the first item
    )
    
    # Extract the SKU from the selected option
    target_sku = selected_option.split(' - ')[0]

    if st.button("✨ Get Recommendations", type="primary"):
        if not API_URL or "YOUR_CLOUD_FUNCTION" in API_URL:
            st.error("Please configure the `API_URL` in the Streamlit script first.")
        else:
            # --- API Call and Display Results ---
            st.header("2. Recommended Products")
            
            with st.spinner(f"Finding recommendations for {target_sku}..."):
                try:
                    # Call the Cloud Function API
                    response = requests.post(API_URL, json={"sku": target_sku})

                    if response.status_code == 200:
                        data = response.json()
                        recommendations = data.get("recommendations", [])
                        
                        if recommendations:
                            # Display results in columns
                            num_cols = 3 # Number of columns for display
                            cols = st.columns(num_cols)
                            for i, rec in enumerate(recommendations):
                                with cols[i % num_cols]:
                                    st.subheader(rec['recommended_sku_code'])
                                    st.markdown(f"**Description:** {rec['PRODUCT_DESCRIPTION']}")
                                    st.metric(label="Similarity Score", value=f"{rec['similarity_score']:.2%}")
                                    st.caption(f"Category: {rec['CATEGORY']}\n\nSub-Category: {rec['SUB_CATEGORY']}\n\nColour: {rec['COLOUR']}")
                                    st.divider()
                        else:
                            st.warning("No recommendations were found for the selected product.")

                    elif response.status_code == 404:
                         st.error(f"SKU '{target_sku}' not found or has no recommendations.")
                    else:
                        st.error(f"Error from API: {response.status_code} - {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the recommendation API. Error: {e}")

else:
    st.warning("Could not load product data from BigQuery.")
