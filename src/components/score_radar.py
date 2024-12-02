import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_score_radar(df, platform=None):
    """Render radar chart for different scores based on playstyle"""

    # Filter by platform if specified
    if platform and platform != "All":
        df = df[df["Platform"] == platform]

    # Define scores to display
    scores = [
        "Social Anxiety Score",
        "Life Satisfaction",
        "Narcissist",
        "Anxiety Score",
    ]

    # Calculate average scores for each playstyle
    playstyles = df["Playstyle"].unique()
    fig = go.Figure()

    for style in playstyles:
        style_data = df[df["Playstyle"] == style]
        values = [
            style_data["SPIN_T"].mean(),
            style_data["SWL_T"].mean(),
            style_data["Narcissism"].mean(),
            style_data["GAD_T"].mean(),
        ]

        fig.add_trace(
            go.Scatterpolar(r=values, theta=scores, name=style, fill="toself")
        )

    # Update layout
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500,
        title="Score Distribution by Gaming Style",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Add playstyle filters
    st.write("Compare different playstyles:")
    selected_styles = st.multiselect(
        "Select playstyles to compare",
        options=list(playstyles),
        default=list(playstyles)[:2],
    )
