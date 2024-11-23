import streamlit as st
from bittensor_metrics import bittensor_metrics
from price_change import price_change
from tao_data_fetcher import get_tao_data

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='TBD Dashboard',
    page_icon=':pick:',
)

# Set the title that appears at the top of the page.
st.title('🫡 TBD Dashboard :pick:')

# Auto-update data every 30 seconds
placeholder = st.empty()

tao_data = get_tao_data()

if tao_data:
    with placeholder.container():
        # Display metrics for TAO
        st.header('Bittensor Metrics', divider='gray')
        bittensor_metrics(tao_data)
        st.subheader('Price Changes Over Different Timeframes', divider='gray')
        price_change(tao_data)
else:
    st.warning("Couldn't retrieve TAO data. Please try again later.")
