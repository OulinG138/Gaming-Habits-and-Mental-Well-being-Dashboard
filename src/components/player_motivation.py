import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_motivation_analysis(df):
    """Render player motivation analysis visualization"""

    # Process motivation data - using agg to get both mean and size
    motivation_data = (
        df.groupby(["whyplay", "Work"])
        .agg(anxiety_level=("GAD_T", "mean"), count=("GAD_T", "size"))
        .reset_index()
    )

    # Create scatter plot
    fig = go.Figure()

    # Add traces for each employment status
    employment_statuses = motivation_data["Work"].unique()

    for status in employment_statuses:
        mask = motivation_data["Work"] == status
        data = motivation_data[mask]

        fig.add_trace(
            go.Scatter(
                x=data["whyplay"],
                y=[status] * len(data),
                mode="markers",
                name=status,
                marker=dict(
                    size=data["count"],  # Size based on count
                    sizeref=2.0 * max(data["count"]) / (40.0**2),  # Scale the sizes
                    sizemin=4,
                    color=data["anxiety_level"],
                    colorscale="Reds",
                    showscale=True,
                    colorbar=dict(title="Anxiety Level"),
                ),
                text=data["anxiety_level"].round(1),
                hovertemplate="<br>".join(
                    [
                        "Motivation: %{x}",
                        "Status: %{y}",
                        "Anxiety Level: %{text}",
                        "Count: %{marker.size}",
                        "<extra></extra>",
                    ]
                ),
            )
        )

    # Update layout
    fig.update_layout(
        height=400,
        title="Gaming Motivation by Employment Status",
        xaxis_title="Motivation",
        yaxis_title="Employment Status",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Add filters for specific analysis
    col1, col2 = st.columns(2)

    with col1:
        # Filter by employment
        employment_status = st.radio(
            "Employment Status", ["All"] + list(employment_statuses)
        )

    with col2:
        # Filter by motivation
        motivation_types = motivation_data["whyplay"].unique()
        motivation_type = st.radio(
            "Gaming Motivation", ["All"] + list(motivation_types)
        )
