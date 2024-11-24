import pandas as pd
import altair as alt
import streamlit as st

def plot_rank_chart(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Convert the MAX_timestamp column to a datetime format
    data['MAX_timestamp'] = pd.to_datetime(data['MAX_timestamp'], format='%Y %m %d %H %M')

    # Melt the data for Altair (long format for multiple lines)
    melted_data = data.melt(
        id_vars=[
            'MAX_timestamp',
            'COUNT_NON_IMMUNE_daily_reward_less_UID_152',
            'COUNT_NON_VALI_daily_reward_greater_UID_152',
            'COUNT_NON_IMMUNE_daily_reward_less_UID_155',
            'COUNT_NON_VALI_daily_reward_greater_UID_155'
        ],
        value_vars=[
            'MIN_daily_reward',
            'MIN_NON_IMMUNE_daily_reward',
            'UID_152_daily_reward',
            'UID_155_daily_reward',
            'MAX_NON_VALI_daily_reward'
        ],
        var_name='Metric',
        value_name='Value'
    )

    # Base line chart for all metrics
    base_chart = alt.Chart(melted_data).mark_line(point=True).encode(
        x=alt.X('MAX_timestamp:T', title='Timestamp'),
        y=alt.Y('Value:Q', title='Rewards'),
        color='Metric:N',
        tooltip=[
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Reward Value')
        ]
    )

    # Tooltip for UID_152_daily_reward
    uid_152_chart = alt.Chart(melted_data).mark_point().encode(
        x=alt.X('MAX_timestamp:T'),
        y=alt.Y('Value:Q'),
        tooltip=[
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Reward Value'),
            alt.Tooltip('COUNT_NON_IMMUNE_daily_reward_less_UID_152:Q', title='COUNT NON IMMUNE < UID_152'),
            alt.Tooltip('COUNT_NON_VALI_daily_reward_greater_UID_152:Q', title='COUNT NON VALI > UID_152')
        ]
    ).transform_filter(
        alt.datum.Metric == 'UID_152_daily_reward'
    )

    # Tooltip for UID_155_daily_reward
    uid_155_chart = alt.Chart(melted_data).mark_point().encode(
        x=alt.X('MAX_timestamp:T'),
        y=alt.Y('Value:Q'),
        tooltip=[
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Reward Value'),
            alt.Tooltip('COUNT_NON_IMMUNE_daily_reward_less_UID_155:Q', title='COUNT NON IMMUNE < UID_155'),
            alt.Tooltip('COUNT_NON_VALI_daily_reward_greater_UID_155:Q', title='COUNT NON VALI > UID_155')
        ]
    ).transform_filter(
        alt.datum.Metric == 'UID_155_daily_reward'
    )

    # Combine the charts
    combined_chart = base_chart + uid_152_chart + uid_155_chart

    # Render the chart in Streamlit
    st.altair_chart(combined_chart.properties(width=800, height=400).interactive(), use_container_width=True)
