import requests
import streamlit as st

def get_tao_data():
    """Fetch TAO data from the TaoStats API."""
    api_url = "https://api.taostats.io/api/price/latest/v1?asset=tao"
    headers = {
        'Authorization': "oMsSsdmi9ILQpk3Cokql3C0VPsutpKoy4O2y3RrhNn2qOxJcha7E1RbR2LTnI4E0",
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
