import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def group_playstyles(playstyle):
    if "Singleplayer" in playstyle:
        return "Single Player"
    elif "Multiplayer - offline" in playstyle:
        return "Multiplayer - offline (same room)"
    elif "Multiplayer - online - with strangers" in playstyle:
        return "Multiplayer - online (with strangers)"
    elif "Multiplayer - online - with online acquaintances" in playstyle:
        return "Multiplayer - online (with online acquaintances/teammates)"
    elif "Multiplayer - online - with real life friends" in playstyle:
        return "Multiplayer - online (with real-life friends)"
    else:
        return "Others"


def normalize_column(column):
    """Normalize a column to the range 0-100."""
    return (column - column.min()) / (column.max() - column.min()) * 100


def invert_column(column):
    """Invert a column to make higher values represent worse cases."""
    return 100 - normalize_column(column)


def render_score_radar(df, game=None):
    """Render radar chart with normalized scores on the same scale and clickable legend."""

    # Filter by platform if specified
    if game and game != "All":
        df = df[df["Game"] == game]
    # Group playstyles
    df['Grouped_Playstyle'] = df['Playstyle'].apply(group_playstyles)

    # Add multiselect for playstyles
    unique_playstyles = list(df['Grouped_Playstyle'].unique())
    selected_playstyles = st.multiselect(
        "Select Playstyles", unique_playstyles, default=unique_playstyles)

    # Filter by selected playstyles
    df = df[df["Grouped_Playstyle"].isin(selected_playstyles)]

    # Define scores to display
    scores = [
        "Social Anxiety Score",
        "Life Satisfaction",
        "Narcissism",
        "Anxiety Score",
    ]
    # Ensure required columns exist
    df['Social Anxiety Score'] = df['SPIN_T']
    df['Life Satisfaction'] = invert_column(
        df['SWL_T'])  # Invert Life Satisfaction
    df['Anxiety Score'] = df['GAD_T']
    # Normalize all other scores
    for score in ["Social Anxiety Score", "Narcissism", "Anxiety Score"]:
        df[score] = normalize_column(df[score])

    # Calculate average normalized scores for each grouped playstyle
    grouped = df.groupby('Grouped_Playstyle')[
        ['Social Anxiety Score', 'Life Satisfaction', 'Narcissism', 'Anxiety Score']
    ].mean()
    # Create radar chart
    fig = go.Figure()
    for playstyle, values in grouped.iterrows():
        fig.add_trace(
            go.Scatterpolar(
                r=values.tolist(),
                theta=scores,
                name=playstyle,
                fill="toself"
            )
        )
    # Update layout for interactivity and scale adjustment
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=14)  # Increased radial axis tick font size
            ),
            angularaxis=dict(
                tickfont=dict(size=16)  # Increased angular axis tick font size
            )
        ),
        showlegend=True,
        height=800,
        width=1000,
        polar_bgcolor='#151517',
        legend=dict(
            title=dict(
                text="Playstyles",
                font=dict(size=18)  # Increased legend title font size
            ),
            font=dict(size=16)  # Increased legend item font size
        )
    )
    # Configure legend interaction to isolate traces
    fig.update_layout(
        legend=dict(
            itemclick="toggleothers",
            itemdoubleclick="toggle",
        )
    )
    # Render chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
