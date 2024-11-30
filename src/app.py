import streamlit as st

from pages import game_analysis, player_analysis, quality_analysis
from utils.data_processing import load_data

# Page configuration
st.set_page_config(
    page_title="Gaming Habits and Mental Well-being", page_icon="🎮", layout="wide"
)


def main():
    # Load data
    df = load_data()

    # Set title
    st.title("Gaming Habits and Mental Well-being")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(
        ["Kind of Player", "Kind of Game", "Quality of Life"])

    # Render each tab
    with tab1:
        player_analysis.render(df)

    with tab2:
        game_analysis.render(df)

    with tab3:
        quality_analysis.render(df)


if __name__ == "__main__":
    
    main()
