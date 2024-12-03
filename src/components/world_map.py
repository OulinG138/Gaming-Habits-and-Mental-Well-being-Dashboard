import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd
from utils.data_processing import get_country_stats, load_geojson


# FIXME: Right now it has two color scales
def render_world_map(df):
    """Render interactive world map visualization of gaming anxiety levels"""
    # Get country statistics and GeoJSON data
    country_stats = get_country_stats(df)
    world_geo = load_geojson()

    if world_geo is None:
        st.error("Unable to load map data. Please check if the GeoJSON file exists.")
        return None

    # Create base map
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        min_zoom=2,
        max_zoom=6,
        tiles='cartodbpositron',
        prefer_canvas=True,
        world_copy_jump=True  # Enable proper wrapping
    )

    # Create color scale with red tones
    vmin = country_stats['GAD_T'].min()
    vmax = country_stats['GAD_T'].max()

    colormap = cm.LinearColormap(
        colors=['#ffcdd2', '#ef9a9a', '#e57373',
                '#ef5350', '#e53935', '#c62828'],
        vmin=vmin,
        vmax=vmax,
        caption='Anxiety Level'
    )

    # Create a dictionary for quick country data lookup
    country_data_dict = country_stats.set_index(
        'Residence_ISO3').to_dict('index')

    # Add custom JavaScript to handle map wrapping
    m.get_root().html.add_child(folium.Element("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var map = document.querySelector('#map');
                if (map) {
                    map._fadeDuration = 0;
                    map.options.fadeAnimation = false;
                }
            });
        </script>
    """))

    # Create choropleth layer for consistent wrapping
    choropleth = folium.Choropleth(
        geo_data=world_geo,
        name='base_choropleth',
        data=country_stats,
        columns=['Residence_ISO3', 'GAD_T'],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0,
        line_opacity=0,
        highlight=False,
        smooth_factor=0
    ).add_to(m)

    # Add individual layers for each country
    for feature in world_geo['features']:
        country_code = feature['id']
        if country_code in country_data_dict:
            data = country_data_dict[country_code]
            anxiety_score = data['GAD_T']

            tooltip = f"""
                <div style='font-family: Arial; font-size: 12px; width: 200px'>
                    <b>{feature['properties']['name']}</b><br>
                    Anxiety Score: {anxiety_score:.1f}<br>
                    Life Satisfaction: {data['SWL_T']:.1f}<br>
                    Gaming Hours/Week: {data['Hours']:.1f}
                </div>
            """

            # Create style function that captures the current anxiety score
            def get_style_function(score):
                return lambda x: {
                    'fillColor': colormap(score),
                    'fillOpacity': 0.7,
                    'weight': 1,
                    'color': '#666'
                }

            folium.GeoJson(
                feature,
                name=country_code,
                style_function=get_style_function(anxiety_score),
                tooltip=tooltip,
                highlight_function=lambda x: {
                    'weight': 3,
                    'color': '#fff',
                    'fillOpacity': 0.9
                }
            ).add_to(m)
        else:
            # Add white base for countries without data
            folium.GeoJson(
                feature,
                style_function=lambda x: {
                    'fillColor': '#ffffff',
                    'fillOpacity': 0.1,
                    'weight': 1,
                    'color': '#666'
                }
            ).add_to(m)

    # Add the colormap to the map
    colormap.add_to(m)

    # Add minimap
    minimap = plugins.MiniMap(toggle_display=True)
    m.add_child(minimap)

    # Custom CSS for smooth wrapping
    st.markdown("""
        <style>
            .folium-map {
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .leaflet-tile-container {
                will-change: transform;
                transform-style: preserve-3d;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display map
    map_data = st_folium(
        m,
        width="100%",
        height=500,
        returned_objects=["last_clicked"]
    )

    # Handle click events
    if map_data["last_clicked"] and "id" in map_data["last_clicked"]:
        clicked_country = map_data["last_clicked"]["id"]
        if clicked_country in country_data_dict:
            return clicked_country

    return None
