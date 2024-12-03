import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd
from utils.data_processing import get_country_stats, load_geojson
from shapely.geometry import shape


def get_country_bounds(feature):
    """Get the bounding box coordinates for a country"""
    polygon = shape(feature["geometry"])
    bounds = polygon.bounds
    return [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]


def get_country_centroid(feature):
    """Get the centroid coordinates for a country"""
    polygon = shape(feature["geometry"])
    centroid = polygon.centroid
    return [centroid.y, centroid.x]


def render_world_map(df, selected_country=None):
    """Render interactive world map visualization of gaming anxiety levels"""
    country_stats = get_country_stats(df)
    world_geo = load_geojson()

    if world_geo is None:
        st.error("Unable to load map data. Please check if the GeoJSON file exists.")
        return

    map_center = [20, 0]
    zoom_start = 2

    if selected_country:
        for feature in world_geo["features"]:
            if feature["id"] == selected_country:
                bounds = get_country_bounds(feature)
                map_center = [
                    (bounds[0][0] + bounds[1][0]) / 2,
                    (bounds[0][1] + bounds[1][1]) / 2
                ]
                zoom_start = 4

    m = folium.Map(
        location=map_center,
        zoom_start=zoom_start,
        min_zoom=2,
        max_zoom=6,
        tiles="cartodbpositron",
        prefer_canvas=True,
        world_copy_jump=True,
    )

    if selected_country:
        for feature in world_geo["features"]:
            if feature["id"] == selected_country:
                bounds = get_country_bounds(feature)
                m.fit_bounds(bounds, padding=[20, 20])

    vmin = country_stats["GAD_T"].min()
    vmax = country_stats["GAD_T"].max()
    colormap = cm.LinearColormap(
        colors=["#FFF7BC", "#FED976", "#FEB24C", "#FD8D3C",
                "#FC4E2A", "#E31A1C", "#BD0026", "#800026"],
        vmin=vmin,
        vmax=vmax,
        caption="Anxiety Level",
    )

    country_data_dict = {}
    for feature in world_geo["features"]:
        country_code = feature["id"]
        country_name = feature["properties"]["name"]
        if country_code in country_stats.set_index("Residence_ISO3").index:
            country_data = country_stats[country_stats["Residence_ISO3"]
                                         == country_code].iloc[0].to_dict()
            country_data["name"] = country_name
            country_data_dict[country_code] = country_data

    country_features = folium.FeatureGroup(name="Countries")

    for feature in world_geo["features"]:
        country_code = feature["id"]
        if country_code in country_data_dict:
            data = country_data_dict[country_code]
            anxiety_score = data["GAD_T"]

            tooltip = f"""
                <div style='font-family: Arial; font-size: 13px; width: 220px;
                     background-color: rgba(255,255,255,0.9); padding: 10px;
                     border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2)'>
                    <div style='border-bottom: 2px solid #ddd; margin-bottom: 5px;
                         padding-bottom: 5px; font-weight: bold; color: #333'>
                        {data['name']}
                    </div>
                    <div style='color: #666; line-height: 1.5'>
                        <b>Anxiety Score:</b> {anxiety_score:.2f}<br>
                        <b>Life Satisfaction:</b> {data['SWL_T']:.2f}<br>
                        <b>Gaming Hours/Week:</b> {data['Hours']:.1f}
                    </div>
                </div>
            """

            def style_function(x, score=anxiety_score, selected=country_code == selected_country):
                return {
                    "fillColor": colormap(score),
                    "fillOpacity": 0.9 if selected else 0.75,
                    "weight": 2 if selected else 1,
                    "color": "#fff" if selected else "#666",
                    "dashArray": "" if selected else "3",
                }

            geo_json = folium.GeoJson(
                feature,
                style_function=style_function,
                highlight_function=lambda x: {
                    "weight": 3,
                    "color": "#fff",
                    "dashArray": "",
                    "fillOpacity": 0.9
                },
                tooltip=tooltip,
            )

            folium.Popup(data['name']).add_to(geo_json)
            geo_json.add_to(country_features)

            # Add standard map marker for selected country
            if country_code == selected_country:
                centroid = get_country_centroid(feature)
                folium.Marker(
                    location=centroid,
                    popup=data['name'],
                    icon=folium.Icon(color='red', icon='info-sign'),
                ).add_to(m)

        else:
            folium.GeoJson(
                feature,
                style_function=lambda x: {
                    "fillColor": "#f0f0f0",
                    "fillOpacity": 0.15,
                    "weight": 1,
                    "color": "#999",
                    "dashArray": "3",
                },
            ).add_to(country_features)

    country_features.add_to(m)
    colormap.add_to(m)

    st_folium(
        m,
        width="100%",
        height=500
    )
