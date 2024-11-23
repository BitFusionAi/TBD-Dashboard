import streamlit as st

def bittensor_metrics(tao_data):
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

    # Additional metrics columns (commented out in original code)
    # col4, col5 = st.columns(2)
    # with col4:
    #     st.metric(
    #         label="Market Cap (USD)",
    #         value=f"${float(tao_data['market_cap']):,.2f}"
    #     )
    # with col5:
    #     st.metric(
    #         label="Volume (24h)",
    #         value=f"${float(tao_data['volume_24h']):,.2f}"
    #     )
