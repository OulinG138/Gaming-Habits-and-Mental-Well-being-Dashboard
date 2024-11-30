import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_processing import get_age_stats


def render_age_analysis(df):
    """Render age group analysis visualization"""

    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Get age group statistics
    age_stats = get_age_stats(df)

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add time spent bars
    fig.add_trace(
        go.Bar(
            name="Time Spent",
            x=age_stats["AgeGroup"],
            y=age_stats["Hours"],
            marker_color="lightblue",
            text=age_stats["Hours"].round(1),
            textposition="auto",
        )
    )

    # Add anxiety score bars
    fig.add_trace(
        go.Bar(
            name="Anxiety Score",
            x=age_stats["AgeGroup"],
            y=age_stats["GAD_Total"],
            marker_color="salmon",
            text=age_stats["GAD_Total"].round(1),
            textposition="auto",
        )
    )

    # Update layout
    fig.update_layout(
        barmode="group",
        height=400,
        title="Gaming Hours and Anxiety Score by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Hours / Score",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Use the placeholder to display the chart
    with chart_placeholder:
        st.plotly_chart(fig, use_container_width=True)

    # Create a separate container for filters
    with st.container():
        # Add time ranges selector
        st.write("Select time range to filter:")
        time_ranges = ["0-5", "5-15", "15-25", "Over 25"]
        selected_range = st.selectbox(
            "Hours per week", time_ranges, key="age_time_range"
        )
