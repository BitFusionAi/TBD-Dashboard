import streamlit as st

def price_change(tao_data):
    # Styling for positive and negative values
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

    # Columns for sample metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", float(70), round(float(tao_data['percent_change_1h']),2))
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

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
