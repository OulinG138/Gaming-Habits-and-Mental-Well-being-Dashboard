import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.data_processing import get_game_logo


def render_game_bubble_chart(df):
    """Render a bubble chart where the logos are ordered in decreasing order by count."""
    # Group data by game and count the number of players
    game_stats = df.groupby("Game").size().reset_index(name="count")

    # Sort the games in decreasing order by count
    game_stats = game_stats.sort_values(
        by='count', ascending=False).reset_index(drop=True)

    # Create a dropdown for selecting a game
    game_options = ["All"] + game_stats["Game"].tolist()
    selected_game = st.selectbox("Select a game to focus on:", game_options)

    # Determine data to display and dynamically adjust sizes
    if selected_game == "All":
        filtered_stats = game_stats
        scaled_sizes = game_stats["count"]
        sizeref = 2.0 * max(game_stats["count"]) / 100**2
        padding_games = pd.DataFrame({
            'Game': ['PAD_LEFT', 'PAD_RIGHT'],
            'count': [0, 0]
        })
        filtered_stats = pd.concat([padding_games.iloc[[
                                   0]], filtered_stats, padding_games.iloc[[1]]]).reset_index(drop=True)
    else:
        clicked_index = game_stats[game_stats["Game"]
                                   == selected_game].index[0]
        total_games = len(game_stats)
        zoom_padding = 1

        # Modified filtering logic to handle edge cases
        if clicked_index <= zoom_padding:
            # Left edge case
            x_start = 0
            x_end = min(2 * zoom_padding, total_games - 1)
        elif clicked_index >= total_games - zoom_padding - 1:
            # Right edge case
            x_start = max(total_games - 2 * zoom_padding - 1, 0)
            x_end = total_games - 1
        else:
            # Middle case
            x_start = clicked_index - zoom_padding
            x_end = clicked_index + zoom_padding

        filtered_stats = game_stats.iloc[x_start:x_end + 1].copy()

        # Add padding games on both sides
        padding_games = pd.DataFrame({
            'Game': ['PAD_LEFT', 'PAD_RIGHT'],
            'count': [0, 0]
        })
        filtered_stats = pd.concat([padding_games.iloc[[
                                   0]], filtered_stats, padding_games.iloc[[1]]]).reset_index(drop=True)

        selected_game_count = game_stats.loc[clicked_index, "count"]
        scaled_sizes = filtered_stats["count"] / selected_game_count * 100
        sizeref = 2.0 / 10**2

    # Create figure
    fig = go.Figure()

    # Add base trace
    fig.add_trace(go.Scatter(
        x=filtered_stats["Game"],
        y=[0] * len(filtered_stats),
        mode="markers",
        marker=dict(size=1, opacity=0),
        hoverinfo="none",
        showlegend=False
    ))

    # Add images and text for each game
    max_count = filtered_stats["count"].max()
    for idx, row in filtered_stats.iterrows():
        game_name = row["Game"]
        if game_name not in ['PAD_LEFT', 'PAD_RIGHT']:  # Skip padding games
            logo_url = get_game_logo(game_name)

            if logo_url:
                relative_size = row["count"] / max_count
                base_size = 1.5
                size = base_size * np.sqrt(relative_size)

                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        x=game_name,
                        y=0,
                        xref="x",
                        yref="y",
                        sizex=size,
                        sizey=size,
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        layer="above",
                        opacity=1
                    )
                )

                fig.add_trace(go.Scatter(
                    x=[game_name],
                    y=[size/2 + 0.15],
                    text=f"{row['count']} players",
                    mode="text",
                    textposition="top center",
                    showlegend=False,
                    hoverinfo="none",
                    textfont=dict(
                        color='white',
                        size=14
                    )
                ))

    # Update layout
    fig.update_layout(
        template="plotly_dark",
        height=600,
        width=1400,
        plot_bgcolor='rgba(17,17,17,1)',
        paper_bgcolor='rgba(17,17,17,1)',
        xaxis=dict(
            title="Game Names",
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            tickangle=45,
            tickfont=dict(
                color='white',
                size=12
            ),
            ticktext=filtered_stats[~filtered_stats["Game"].isin(
                ['PAD_LEFT', 'PAD_RIGHT'])]["Game"],
            tickvals=filtered_stats[~filtered_stats["Game"].isin(
                ['PAD_LEFT', 'PAD_RIGHT'])]["Game"],
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=[-0.8, 1.5]
        ),
        margin=dict(l=50, r=50, t=0, b=100),
        showlegend=False
    )

    # Display the chart
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

    return selected_game
