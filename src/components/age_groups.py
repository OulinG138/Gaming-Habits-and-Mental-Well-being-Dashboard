import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_age_analysis(df):
    """Render age group analysis visualization"""
    # Create time spent categories
    df["TimeSpent"] = pd.cut(
        df["Hours"],
        bins=[0, 5, 15, 25, float("inf")],
        labels=["0-5", "5-15", "15-25", "Over 25"]
    )
    # Group data and calculate anxiety score
    grouped = df.groupby(["AgeGroup", "TimeSpent"])[
        "GAD_T"].mean().reset_index()
    # Create the figure
    fig = go.Figure()
    # Define colors for each time spent category
    colors = {
        "0-5": "rgba(220, 235, 255, 0.8)",
        "5-15": "rgba(180, 200, 255, 0.8)",
        "15-25": "rgba(140, 165, 255, 0.8)",
        "Over 25": "rgba(100, 130, 255, 0.8)"
    }
    # Add bars for each time spent category within age groups
    for time_spent in ["0-5", "5-15", "15-25", "Over 25"]:
        time_data = grouped[grouped["TimeSpent"] == time_spent]
        fig.add_trace(go.Bar(
            name=time_spent,
            x=time_data["AgeGroup"],
            y=time_data["GAD_T"],
            marker_color=colors[time_spent],
            text=time_data["GAD_T"].round(1),
            textposition="outside",
            hovertemplate="<b>Age Group:</b> %{x}<br>" +
                         "<b>Hours per Week:</b> " + time_spent + "<br>" +
                         "<b>Anxiety Score:</b> %{y:.1f}<extra></extra>"
        ))
    # Update layout
    fig.update_layout(
        title={
            'text': "Anxiety Scores by Age Group and Time Spent Gaming",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'white'}
        },
        xaxis_title={
            'text': "Age Group",
            'font': {'color': 'white'}
        },
        yaxis_title={
            'text': "Anxiety Score",
            'font': {'color': 'white'}
        },
        xaxis={
            'gridcolor': 'rgba(128, 128, 128, 0.2)',
            'tickfont': {'color': 'white'},
            'showgrid': False  # Hide vertical grid lines
        },
        yaxis={
            # More visible horizontal grid lines
            'gridcolor': 'rgba(255, 255, 255, 0.15)',
            'tickfont': {'color': 'white'},
            'gridwidth': 1,
            'showgrid': True,
            'dtick': 1  # Show grid line for each whole number
        },
        barmode="group",
        height=600,
        showlegend=True,
        legend_title={
            'text': "Hours per Week",
            'font': {'color': 'white'}
        },
        legend={
            'font': {'color': 'white'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'rgba(255,255,255,0.3)'
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=100)
    )
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
