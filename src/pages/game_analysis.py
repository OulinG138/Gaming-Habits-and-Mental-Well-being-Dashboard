import streamlit as st

from components.game_chart import render_game_bubble_chart
from components.score_radar import render_score_radar
from components.sunburst_chart import render_playstyle_anxiety_sunburst_chart


def render(df):
    """Render the Kind of Game analysis page"""

    game_container = st.container()
    with game_container:
        st.header("Game Popularity and Engagement Visualization")
        selected_game = render_game_bubble_chart(df)

    st.empty()

    sunburst_container = st.container()
    with sunburst_container:
        st.subheader("Playstyle and Anxiety Level Distribution")
        render_playstyle_anxiety_sunburst_chart(df, selected_game)

    st.empty()

    radar_container = st.container()
    with radar_container:
        st.subheader("Score Distribution by Gaming Style")
        filtered_df = (
            df[df["Game"] == selected_game]
            if selected_game and selected_game != "All"
            else df
        )
        render_score_radar(filtered_df, selected_game)
