import streamlit as st
import requests
import json
import os
import time

# Load API key from Streamlit secrets
api_key = st.secrets["TAO_API_KEY"]["value"] if isinstance(st.secrets["TAO_API_KEY"], dict) else st.secrets["TAO_API_KEY"]
if not api_key:
    st.error("API key not found. Ensure the Streamlit secrets are set up correctly and contain 'TAO_API_KEY'.")
    import sys
    sys.exit("Exiting application due to missing API key.")

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='TBD Dashboard',
    page_icon=':pick:',
)

# -----------------------------------------------------------------------------
# Function to get TAO data from TaoStats API.

def get_tao_data():
    """Fetch TAO data from the TaoStats API."""
    api_url = "https://api.taostats.io/api/price/latest/v1?asset=tao"  # Corrected endpoint URL
      # Get the API key from environment variables
    headers = {
        'Authorization': str(api_key),  # Ensure API key is used correctly
        'accept': 'application/json'
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 401:
            st.error("Unauthorized access. Please check your API key in the Streamlit secrets and ensure it is valid.")
        response.raise_for_status()
        return response.json()['data'][0]
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error fetching data: {req_err}")
    return None

# ----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
st.title('🩡 TBD Dashboard :pick:')

# Auto-update data every 30 seconds
placeholder = st.empty()

while True:
    tao_data = get_tao_data()

    if tao_data:
        with placeholder.container():
            # Display metrics for TAO
            st.header('Bittensor (TAO) Metrics', divider='gray')
            ''
            
            # Set up columns for the metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Current Price (USD)",
                    value=f"${float(tao_data['price']):,.2f}",
                    delta=f"{float(tao_data['percent_change_24h']):.2f}% (24h)"
                )

            with col2:
                st.metric(
                    label="Circulating Supply",
                    value=f"{int(float(tao_data['circulating_supply'])):,} T"
                )
            
            with col3:
                st.metric(
                    label="Max Supply",
                    value=f"{int(float(tao_data['max_supply'])):,} T"
                )
            
            ''
            col4, col5 = st.columns(2)
            
            with col4:
                st.metric(
                    label="Market Cap (USD)",
                    value=f"${float(tao_data['market_cap']):,.2f}"
                )
            
            # with col5:
            #     st.metric(
            #         label="Fully Diluted Market Cap (USD)",
            #         value=f"${float(tao_data['fully_diluted_market_cap']):,.2f}"
            #     )
            
            with col5:
                st.metric(
                    label="Volume (24h)",
                    value=f"${float(tao_data['volume_24h']):,.2f}"
                )
            
            # Add more detailed price changes
            st.subheader('Price Changes Over Different Timeframes', divider='gray')
            ''
            st.markdown(
                """
                <style>
                .positive {
                    color: green;
                }
                .negative {
                    color: red;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Price change details with conditional coloring
            price_changes = {
                "1 Hour": float(tao_data['percent_change_1h']),
                "24 Hours": float(tao_data['percent_change_24h']),
                "7 Days": float(tao_data['percent_change_7d']),
                "30 Days": float(tao_data['percent_change_30d']),
                "60 Days": float(tao_data['percent_change_60d']),
                "90 Days": float(tao_data['percent_change_90d']),
            }

            for timeframe, change in price_changes.items():
                color_class = "positive" if change >= 0 else "negative"
                st.markdown(
                    f"- **{timeframe}**: <span class='{color_class}'>{change:+.2f}%</span>",
                    unsafe_allow_html=True
                )
    else:
        st.warning("Couldn't retrieve TAO data. Please try again later.")

    # Wait for 30 seconds before updating the data
    time.sleep(30)
