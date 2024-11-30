import streamlit as st

from components.age_groups import render_age_analysis
from components.player_motivation import render_motivation_analysis
from components.world_map import render_world_map


def render(df):
    """Render the Kind of Player analysis page"""

    # Create containers first
    map_container = st.container()
    age_container = st.container()
    motivation_container = st.container()

    # Create two columns for layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        with map_container:
            # World map section
            st.subheader("Global Gaming Anxiety Levels")
            selected_country = render_world_map(df)

        # Update data based on country selection
        if selected_country:
            filtered_df = df[df["Residence_ISO3"] == selected_country]
        else:
            filtered_df = df

        with age_container:
            # Age group analysis below map
            st.subheader("Age Group Analysis")
            render_age_analysis(filtered_df)

    with right_col:
        with motivation_container:
            # Player motivation analysis
            st.subheader("Player Motivation")
            render_motivation_analysis(filtered_df)

    # Bottom section - Network visualization
    st.subheader("Relationships Between Variables")
    country_circles = df["Residence_ISO3"].unique()
    age_circles = df["AgeGroup"].unique()
    anxiety_circles = ["0-20", "20-40", "40-60", "60-80", "80-100"]

    # Create clickable circles
    st.write("Click circles to explore relationships:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Countries")
        selected_country = st.selectbox("Select country", country_circles)

    with col2:
        st.write("Anxiety Levels")
        selected_anxiety = st.selectbox("Select anxiety range", anxiety_circles)

    with col3:
        st.write("Age Groups")
        selected_age = st.selectbox("Select age group", age_circles)
