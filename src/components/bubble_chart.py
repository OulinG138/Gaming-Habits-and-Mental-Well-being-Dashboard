import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_relationship_analysis(df):
    # Define bins and groups
    anxiety_bins = [0, 3, 7, 11, 15, 21]
    anxiety_labels = ["0-3", "4-7", "8-11", "12-15", "16-21"]
    df["Anxiety_Group"] = pd.cut(
        df["GAD_T"], bins=anxiety_bins, labels=anxiety_labels, include_lowest=True)

    age_bins = [18, 23, 28, 33, 38, 100]
    age_labels = ["18-22", "23-27", "28-32", "33-37", "38+"]
    df["Age_Group"] = pd.cut(df["Age"].astype(
        float), bins=age_bins, labels=age_labels, include_lowest=True)

    # Filter and group data
    selected_countries = ["CAN", "USA", "DEU", "NLD", "GBR"]
    filtered_df = df[df["Residence_ISO3"].isin(selected_countries)]
    grouped_data = filtered_df.groupby(
        ["Anxiety_Group", "Residence_ISO3", "Age_Group"]).size().reset_index(name="Count")

    # Calculate proportions
    total_by_country = filtered_df.groupby("Residence_ISO3").size()
    total_by_age = filtered_df.groupby("Age_Group").size()
    grouped_data["Country_Proportion"] = grouped_data.apply(
        lambda row: row["Count"] / total_by_country[row["Residence_ISO3"]], axis=1
    )
    grouped_data["Age_Proportion"] = grouped_data.apply(
        lambda row: row["Count"] / total_by_age[row["Age_Group"]], axis=1
    )

    # Mappings
    country_full_names = {
        "USA": "U.S.A", "CAN": "Canada", "DEU": "Germany",
        "NLD": "Netherlands", "GBR": "U.K"
    }

    country_coords = {
        "U.S.A": {"x": -2.18, "y": 47.5}, "Canada": {"x": -1.7, "y": 47},
        "Germany": {"x": -1.5, "y": 46}, "Netherlands": {"x": -1.7, "y": 45},
        "U.K": {"x": -2, "y": 46}
    }

    anxiety_coords = {
        "0-3": {"x": 0, "y": 44}, "4-7": {"x": 0.5, "y": 44},
        "8-11": {"x": 0, "y": 45}, "12-15": {"x": 0.3, "y": 45},
        "16-21": {"x": 0.2, "y": 43}
    }

    age_coords = {
        "18-22": {"x": 2.3, "y": 48.5}, "23-27": {"x": 1.8, "y": 50},
        "28-32": {"x": 2.1, "y": 49.5}, "33-37": {"x": 1.9, "y": 48.5},
        "38+": {"x": 2, "y": 47.5}
    }

    def assign_sizes(counts, sizes=[30, 50, 70, 90, 110]):
        if len(counts) <= 1:
            return {counts.index[0]: sizes[-1]}
        bins = pd.qcut(counts, min(5, len(counts)), duplicates='drop')
        size_map = {}
        for i, (_, grp) in enumerate(counts.groupby(bins)):
            for idx in grp.index:
                size_map[idx] = sizes[min(i, len(sizes)-1)]
        return size_map

    country_sizes = assign_sizes(
        grouped_data.groupby("Residence_ISO3")["Count"].sum())
    anxiety_sizes = assign_sizes(
        grouped_data.groupby("Anxiety_Group")["Count"].sum())
    age_sizes = assign_sizes(grouped_data.groupby("Age_Group")["Count"].sum())

    # Visualization
    selected_anxiety = st.selectbox(
        'Select Anxiety Group to Highlight Connections:',
        ['None'] + list(anxiety_coords.keys()),
        key='anxiety_select'
    )

    fig = go.Figure()

    # Add bubbles
    for country_code in country_sizes.keys():
        country = country_full_names[country_code]
        fig.add_trace(go.Scatter(
            x=[country_coords[country]["x"]],
            y=[country_coords[country]["y"]],
            mode="markers+text",
            marker=dict(
                size=country_sizes[country_code], color="blue", opacity=0.6),
            text=[country],
            textposition="middle center",
            name=country
        ))

    for group in anxiety_sizes.keys():
        fig.add_trace(go.Scatter(
            x=[anxiety_coords[group]["x"]],
            y=[anxiety_coords[group]["y"]],
            mode="markers+text",
            marker=dict(size=anxiety_sizes[group], color="red", opacity=0.6),
            text=[group],
            textposition="middle center",
            name=group
        ))

    for age_group in age_sizes.keys():
        fig.add_trace(go.Scatter(
            x=[age_coords[age_group]["x"]],
            y=[age_coords[age_group]["y"]],
            mode="markers+text",
            marker=dict(size=age_sizes[age_group],
                        color="yellow", opacity=0.6),
            text=[age_group],
            textposition="middle center",
            name=age_group
        ))

    # Add connections
    if selected_anxiety != 'None':
        filtered = grouped_data[grouped_data["Anxiety_Group"]
                                == selected_anxiety]
        if not filtered.empty:
            top_country = country_full_names[filtered.loc[filtered["Country_Proportion"].idxmax(
            ), "Residence_ISO3"]]
            top_age = filtered.loc[filtered["Age_Proportion"].idxmax(
            ), "Age_Group"]

            fig.add_trace(go.Scatter(
                x=[country_coords[top_country]["x"],
                    anxiety_coords[selected_anxiety]["x"]],
                y=[country_coords[top_country]["y"],
                    anxiety_coords[selected_anxiety]["y"]],
                mode="lines",
                line=dict(color="gray", width=2),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[anxiety_coords[selected_anxiety]
                    ["x"], age_coords[top_age]["x"]],
                y=[anxiety_coords[selected_anxiety]
                    ["y"], age_coords[top_age]["y"]],
                mode="lines",
                line=dict(color="gray", width=2),
                showlegend=False
            ))

    # Layout
    fig.update_layout(
        title="Anxiety Levels by Country and Age",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False,
                   showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False,
                   showticklabels=False, visible=False),
        height=800,
        width=1200,
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=100, b=50)
    )

    fig.add_annotation(x=-2, y=49, text="Country",
                       showarrow=False, font=dict(size=16))
    fig.add_annotation(x=0, y=46, text="Anxiety Score",
                       showarrow=False, font=dict(size=16))
    fig.add_annotation(x=2, y=52, text="Age",
                       showarrow=False, font=dict(size=16))

    st.plotly_chart(fig, use_container_width=True)
