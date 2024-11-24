import streamlit as st
from bittensor_metrics import bittensor_metrics
from price_change import price_change
from tao_data_fetcher import get_tao_data
from rank_chart import plot_rank_chart
import threading
import time
import subprocess

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='TBD Dashboard',
    page_icon=':pick:',
)

# Function to run `csv_45_rank.py` and `tao_data_fetcher.py`
def run_scripts():
    while True:
        try:
            # Run csv_45_rank.py
            subprocess.run(["python", "csv_45_rank.py"], check=True)
            
            # Run tao_data_fetcher.py
            subprocess.run(["python", "tao_data_fetcher.py"], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running scripts: {e}")

        # Sleep for 18 minutes (1080 seconds)
        time.sleep(1080)

# Start the script runner in a background thread
thread = threading.Thread(target=run_scripts, daemon=True)
thread.start()

# Set the title that appears at the top of the page.
st.title('TBD :pick:')

# Auto-update data every 30 seconds
placeholder = st.empty()

# Fetch and display TAO data
tao_data = get_tao_data()

if tao_data:
    with placeholder.container():
        # Display metrics for TAO
        st.header('Tao Price Metrics', divider='gray')
        bittensor_metrics(tao_data)
else:
    st.warning("Couldn't retrieve TAO data. Please try again later.")

# Set up the file path for the CSV file
file_path = 'taostats_metrics.csv'

# Display the line chart
st.header("SN45 - Rank Metrics", divider='gray')
plot_rank_chart(file_path)
