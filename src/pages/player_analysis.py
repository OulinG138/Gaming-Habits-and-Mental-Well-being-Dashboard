import streamlit as st
from components.age_groups import render_age_analysis
from components.player_motivation import render_motivation_analysis
from components.world_map import render_world_map
from utils.data_processing import get_country_names


def render(df):
    """Render the Kind of Player analysis page"""
    country_circles = sorted(df["Residence_ISO3"].unique())

    # Get the mapping of country codes to names
    country_names = get_country_names()

    # Place the select box at the top
    st.subheader("Global Gaming Anxiety Levels")
    named_countries = [(name, code) for code in country_circles
                       if (name := country_names.get(code, code))]
    named_countries.sort(key=lambda x: x[0])  # Sort by country name
    all_options = [("All Countries", "All Countries")] + named_countries

    selected_name, selected_code = st.selectbox(
        "Filter by Country",
        options=all_options,
        format_func=lambda x: x[0],
        index=0
    )

    map_container = st.container()
    with map_container:
        render_world_map(df, selected_country=selected_code)

    filtered_df = (
        df[df["Residence_ISO3"] == selected_code]
        if selected_code != "All Countries"
        else df
    )

    age_container = st.container()
    with age_container:
        st.subheader("Age Group Analysis")
        render_age_analysis(filtered_df)

    motivation_container = st.container()
    with motivation_container:
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
        selected_anxiety = st.selectbox(
            "Select anxiety range", anxiety_circles)

    with col3:
        st.write("Age Groups")
        selected_age = st.selectbox("Select age group", age_circles)
