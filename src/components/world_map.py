import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

from utils.data_processing import get_country_stats


def render_world_map(df):
    """Render interactive world map visualization"""

    # Create fixed-size container
    map_container = st.empty()

    # Get country statistics
    country_stats = get_country_stats(df)

    # Create choropleth map
    fig = px.choropleth(
        country_stats,
        locations="Residence_ISO3",
        color="GAD_T",
        color_continuous_scale="Reds",
        range_color=(0, country_stats["GAD_T"].max()),
        labels={"GAD_T": "Anxiety"},
    )

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,  # Fixed height
        width=800,  # Fixed width
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            showland=True,
            showcountries=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Anxiety", side="right"),
            thicknessmode="pixels",
            thickness=15,
            lenmode="pixels",
            len=200,
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=0.98,
            ticks="outside",
            tickwidth=1,
            ticklen=5,
            tickformat=".1f",
            orientation="v",
        ),
    )

    # Display the map and get click events
    with map_container:
        clicked_point = plotly_events(
            fig, click_event=True, override_height=300)

    # Handle click events
    if clicked_point:
        # Print the click data to debug
        st.write("Debug - Click data:", clicked_point)

        # Extract the country code from the clicked point
        try:
            if "points" in clicked_point[0]:
                return clicked_point[0]["points"][0]["location"]
            elif "customdata" in clicked_point[0]:
                return clicked_point[0]["customdata"][0]
            elif "locationdata" in clicked_point[0]:
                return clicked_point[0]["locationdata"]
            else:
                st.warning(
                    "Could not detect country from click. Click data structure:",
                    clicked_point,
                )
                return None
        except Exception as e:
            st.warning(f"Error processing click: {str(e)}")
            return None

    return None
