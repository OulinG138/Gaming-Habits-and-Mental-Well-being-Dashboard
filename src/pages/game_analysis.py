import streamlit as st

from components.platform_chart import render_game_bubble_chart
from components.score_radar import render_score_radar
from components.playstyle_rose_chart import render_playstyle_anxiety_sunburst_chart

def render(df):
    """Render the Kind of Game analysis page"""

    # Create the main container
    main_container = st.container()

    with main_container:
        st.header("Gaming Platform Analysis")

        # Use columns for layout
        charts_col, filters_col = st.columns([3, 1])

        with charts_col:
            # Container for the bubble chart
            platform_container = st.container()
            with platform_container:
                # Get the selected game from the bubble chart
                selected_game = render_game_bubble_chart(df)

            # Add some space
            st.write("")

        # Create a new set of columns for the sunburst and radar charts
        sunburst_col, radar_col = st.columns([1, 1])

        with sunburst_col:
            # Container for the sunburst chart
            sunburst_container = st.container()
            with sunburst_container:
                st.subheader("Playstyle and Anxiety Level Distribution")
                # Render the sunburst chart based on the selected game
                render_playstyle_anxiety_sunburst_chart(df, selected_game)

        with radar_col:
            # Container for the radar chart
            radar_container = st.container()
            with radar_container:
                st.subheader("Score Distribution by Gaming Style")
                # Filter data based on the selected game
                filtered_df = (
                    df[df["Game"] == selected_game]
                    if selected_game and selected_game != "All"
                    else df
                )
                render_score_radar(filtered_df, selected_game)
