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
    return (column - column.min()) / (column.max() - column.min()) * 100


def invert_column(column):
    return 100 - normalize_column(column)


def render_score_radar(df, game=None):
    if game and game != "All":
        df = df[df["Game"] == game]

    df['Grouped_Playstyle'] = df['Playstyle'].apply(group_playstyles)
    unique_playstyles = list(df['Grouped_Playstyle'].unique())
    selected_playstyles = st.multiselect(
        "Select Playstyles", unique_playstyles, default=unique_playstyles)

    df = df[df["Grouped_Playstyle"].isin(selected_playstyles)]

    scores = [
        "Social Anxiety Score",
        "Life Satisfaction",
        "Narcissism",
        "Anxiety Score",
    ]

    df['Social Anxiety Score'] = df['SPIN_T']
    df['Life Satisfaction'] = invert_column(df['SWL_T'])
    df['Anxiety Score'] = df['GAD_T']

    for score in ["Social Anxiety Score", "Narcissism", "Anxiety Score"]:
        df[score] = normalize_column(df[score])

    grouped = df.groupby('Grouped_Playstyle')[scores].mean()

    fig = go.Figure()

    for playstyle, values in grouped.iterrows():
        fig.add_trace(
            go.Scatterpolar(
                r=values.tolist(),
                theta=scores,
                name=playstyle,
                fill="toself",
                hovertemplate="<b>%{theta}</b><br>" +
                "<b>Value</b>: %{r:.1f}<br>" +
                "<b>Playstyle</b>: " + playstyle + "<extra></extra>"
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=14)
            ),
            angularaxis=dict(
                tickfont=dict(size=16)
            )
        ),
        showlegend=True,
        height=800,
        width=1000,
        polar_bgcolor='#151517',
        legend=dict(
            title=dict(
                text="Playstyles",
                font=dict(size=18)
            ),
            font=dict(size=16),
            itemclick="toggleothers",
            itemdoubleclick="toggle"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
