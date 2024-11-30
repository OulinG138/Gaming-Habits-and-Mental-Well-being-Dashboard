import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render_life_quality_analysis(df, anxiety_type="general"):
    """Render quality of life analysis visualizations"""

    # Create layout with two plots
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Anxiety vs Life Satisfaction", "Score Distributions"),
    )

    # Determine which anxiety score to use
    anxiety_col = "GAD_Total" if anxiety_type == "general" else "SPIN_T"
    anxiety_label = "General Anxiety" if anxiety_type == "general" else "Social Anxiety"

    # Add scatter plot
    fig.add_trace(
        go.Scatter(
            x=df["SWL_Total"],
            y=df[anxiety_col],
            mode="markers",
            marker=dict(
                color=df["Hours"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Gaming Hours"),
            ),
            name="Individual Players",
        ),
        row=1,
        col=1,
    )

    # Add trend line
    z = np.polyfit(df["SWL_Total"], df[anxiety_col], 1)
    p = np.poly1d(z)
    fig.add_trace(
        go.Scatter(
            x=df["SWL_Total"],
            y=p(df["SWL_Total"]),
            mode="lines",
            name="Trend",
            line=dict(color="red", dash="dash"),
        ),
        row=1,
        col=1,
    )

    # Add distribution plots
    fig.add_trace(
        go.Histogram(
            x=df[anxiety_col], name=anxiety_label, marker_color="blue", opacity=0.7
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Histogram(
            x=df["SWL_Total"],
            name="Life Satisfaction",
            marker_color="green",
            opacity=0.7,
        ),
        row=2,
        col=1,
    )

    # Update layout
    fig.update_layout(
        height=800,
        title_text="Quality of Life Analysis",
        showlegend=True,
        barmode="overlay",
    )

    fig.update_xaxes(title_text="Life Satisfaction Score", row=1, col=1)
    fig.update_yaxes(title_text=f"{anxiety_label} Score", row=1, col=1)
    fig.update_xaxes(title_text="Score", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

    # Add average scores
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(f"{anxiety_label} Score", f"{df[anxiety_col].mean():.1f}", delta=None)

    with col2:
        st.metric(
            "Life Satisfaction Score", f"{df['SWL_Total'].mean():.1f}", delta=None
        )

    with col3:
        st.metric("Average Gaming Hours", f"{df['Hours'].mean():.1f}", delta=None)
