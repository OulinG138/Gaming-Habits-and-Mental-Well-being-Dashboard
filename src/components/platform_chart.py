import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_game_bubble_chart(df):
    """Render a bubble chart where the circles are ordered in decreasing order by count."""

    # Group data by game and count the number of players
    game_stats = df.groupby("Game").size().reset_index(name="count")
    
    # Sort the games in decreasing order by count
    game_stats = game_stats.sort_values(by='count', ascending=False).reset_index(drop=True)

    # Create a dropdown for selecting a game
    game_options = ["All"] + game_stats["Game"].tolist()  # Include "All" to show the full chart
    selected_game = st.selectbox("Select a game to focus on:", game_options)

    # Determine data to display and dynamically adjust sizes
    if selected_game == "All":
        filtered_stats = game_stats  # Show all games
        scaled_sizes = game_stats["count"]  # Use the original counts
        sizeref = 2.0 * max(game_stats["count"]) / 100**2  # Calculate sizeref for all games
    else:
        # Find the index of the selected game in the sorted game_stats
        clicked_index = game_stats[game_stats["Game"] == selected_game].index[0]

        # Include neighbors around the selected game
        zoom_padding = 1  # Number of neighboring games to show
        x_start = max(0, clicked_index - zoom_padding)
        x_end = min(len(game_stats) - 1, clicked_index + zoom_padding)

        filtered_stats = game_stats.iloc[x_start:x_end + 1]

        # Scale sizes such that the selected game has a size of 100
        selected_game_count = game_stats.loc[clicked_index, "count"]
        scaled_sizes = filtered_stats["count"] / selected_game_count * 100

        # Recalculate sizeref to ensure the selected game always has size 100
        sizeref = 2.0 / 10**2  # Fixed sizeref for scaling based on size 100

    # Create the bubble chart
    fig = go.Figure()

    # Add bubbles for each filtered game
    fig.add_trace(
        go.Scatter(
            x=filtered_stats["Game"],           # Game names on the x-axis
            y=[0] * len(filtered_stats),        # Align all bubbles horizontally
            mode="markers+text",
            marker=dict(
                size=scaled_sizes,              # Dynamically adjusted size
                sizemode="area",                # Use area to represent size
                sizeref=sizeref,                # Dynamically calculated sizeref
                color=filtered_stats["count"],  # Optional: color based on count
                showscale=False,                # Disable the color scale
            ),
            text=filtered_stats["Game"],         # Add game names as text
            textposition="top center",
            hoverinfo="x+text",                  # Display x (game name) and text on hover
        )
    )

    # Customize layout
    fig.update_layout(
        title="Select a Game to Focus",
        title_x=0.5,
        height=500,
        xaxis=dict(
            title="Game Names",
            showgrid=False,
            zeroline=False,
            showline=False,
            tickangle=45,  # Rotate game names for better readability
        ),
        yaxis=dict(
            visible=False,  # Hide the y-axis
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    return selected_game
