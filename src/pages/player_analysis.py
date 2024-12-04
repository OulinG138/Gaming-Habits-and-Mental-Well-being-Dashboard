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

    st.divider()

    age_container = st.container()
    with age_container:
        st.subheader("Age Group Analysis")
        render_age_analysis(filtered_df)

    st.divider()

    motivation_container = st.container()
    with motivation_container:
        st.subheader("Player Motivation")
        render_motivation_analysis(filtered_df)

    st.divider()

    bubble_container = st.container()
    with bubble_container:
        st.subheader("Relationship between Age, Country and Anxiety Score")
        pass
