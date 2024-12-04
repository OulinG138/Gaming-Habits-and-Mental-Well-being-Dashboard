import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load data
file_path = "data/processed/processed_data.csv"
data = pd.read_csv(file_path)

# Define new anxiety score groups
anxiety_bins = [0, 3, 7, 11, 15, 21]
anxiety_labels = ["0-3", "4-7", "8-11", "12-15", "16-21"]
data["Anxiety_Group"] = pd.cut(
    data["GAD_T"], bins=anxiety_bins, labels=anxiety_labels, include_lowest=True
)

# Define age groups
age_bins = [18, 23, 28, 33, 38, 100]
age_labels = ["18-22", "23-27", "28-32", "33-37", "38+"]
data["Age_Group"] = pd.cut(
    data["Age"].astype(float), bins=age_bins, labels=age_labels, include_lowest=True
)

# Filter target countries
selected_countries = ["CAN", "USA", "DEU", "NLD", "GBR"]
data = data[data["Residence_ISO3"].isin(selected_countries)]

# Group data
grouped_data = (
    data.groupby(["Anxiety_Group", "Residence_ISO3", "Age_Group"])
    .size()
    .reset_index(name="Count")
)

# Calculate proportions
total_by_country = data.groupby("Residence_ISO3").size()
total_by_age = data.groupby("Age_Group").size()

grouped_data["Country_Proportion"] = grouped_data.apply(
    lambda row: row["Count"] / total_by_country[row["Residence_ISO3"]], axis=1
)
grouped_data["Age_Proportion"] = grouped_data.apply(
    lambda row: row["Count"] / total_by_age[row["Age_Group"]], axis=1
)

# Map country codes to full names
country_full_names = {
    "USA": "U.S.A",
    "CAN": "Canada",
    "DEU": "Germany",
    "NLD": "Netherlands",
    "GBR": "U.K",
}

# Update country coordinates to use full names
country_coords = {
    "U.S.A": {"x": -2.18, "y": 47.5},
    "Canada": {"x": -1.7, "y": 47},
    "Germany": {"x": -1.5, "y": 46},
    "Netherlands": {"x": -1.7, "y": 45},
    "U.K": {"x": -2, "y": 46},
}

anxiety_coords = {
    "0-3": {"x": 0, "y": 44},
    "4-7": {"x": 0.5, "y": 44},
    "8-11": {"x": 0, "y": 45},
    "12-15": {"x": 0.3, "y": 45},
    "16-21": {"x": 0.2, "y": 43},
}

age_coords = {
    "18-22": {"x": 2.3, "y": 48.5},
    "23-27": {"x": 1.8, "y": 50},
    "28-32": {"x": 2.1, "y": 49.5},
    "33-37": {"x": 1.9, "y": 48.5},
    "38+": {"x": 2, "y": 47.5},
}

# Preset bubble sizes
preset_sizes = [30, 50, 70, 90, 110]


def assign_preset_sizes(df, column, sizes):
    """
    Assign preset sizes based on Count.
    """
    sorted_df = df.sort_values(by="Count", ascending=True).reset_index(drop=True)
    quantiles = pd.qcut(sorted_df["Count"], q=5, duplicates="drop")
    quantile_groups = sorted_df.groupby(quantiles)

    size_map = {}
    for i, (quantile, group) in enumerate(quantile_groups, start=1):
        size = sizes[i - 1] if i - 1 < len(sizes) else sizes[-1]
        for _, row in group.iterrows():
            size_map[row[column]] = size

    return size_map


# Assign sizes
country_size_map = assign_preset_sizes(
    grouped_data.groupby("Residence_ISO3").agg({"Count": "sum"}).reset_index(),
    "Residence_ISO3",
    preset_sizes,
)

anxiety_size_map = assign_preset_sizes(
    grouped_data.groupby("Anxiety_Group").agg({"Count": "sum"}).reset_index(),
    "Anxiety_Group",
    preset_sizes,
)

age_size_map = assign_preset_sizes(
    grouped_data.groupby("Age_Group").agg({"Count": "sum"}).reset_index(),
    "Age_Group",
    preset_sizes,
)

# Create Dash app
app = Dash(__name__)


# Generate figure
def create_figure(selected_group=None):
    fig = go.Figure()

    # Add country bubbles
    countries = grouped_data.groupby("Residence_ISO3")["Count"].sum().reset_index()
    for _, row in countries.iterrows():
        country_code = row["Residence_ISO3"]
        country = country_full_names[country_code]
        x = country_coords[country]["x"]
        y = country_coords[country]["y"]
        size = country_size_map.get(country_code, preset_sizes[0])
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=size, color="blue", opacity=0.6),
                name=country,
                text=country,
                textposition="middle center",
                hoverinfo="text",
                customdata=[country_code],
            )
        )

    # Add anxiety bubbles
    anxiety_groups = grouped_data.groupby("Anxiety_Group")["Count"].sum().reset_index()
    for _, row in anxiety_groups.iterrows():
        group = row["Anxiety_Group"]
        x = anxiety_coords[group]["x"]
        y = anxiety_coords[group]["y"]
        size = anxiety_size_map.get(group, preset_sizes[0])
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=size, color="red", opacity=0.6),
                name=group,
                text=group,
                textposition="middle center",
                hoverinfo="text",
                customdata=[group],
            )
        )

    # Add age bubbles
    age_groups = grouped_data.groupby("Age_Group")["Count"].sum().reset_index()
    for _, row in age_groups.iterrows():
        age_group = row["Age_Group"]
        x = age_coords[age_group]["x"]
        y = age_coords[age_group]["y"]
        size = age_size_map.get(age_group, preset_sizes[0])
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=size, color="yellow", opacity=0.6),
                name=age_group,
                text=age_group,
                textposition="middle center",
                hoverinfo="text",
            )
        )

    # Add section labels
    fig.add_annotation(
        x=-2, y=49, text="Country", showarrow=False, font=dict(size=16), align="center"
    )
    fig.add_annotation(
        x=0,
        y=46,
        text="Anxiety Score",
        showarrow=False,
        font=dict(size=16),
        align="center",
    )
    fig.add_annotation(
        x=2, y=52, text="Age", showarrow=False, font=dict(size=16), align="center"
    )

    # Add connecting lines
    if selected_group and selected_group in anxiety_coords:
        filtered_data = grouped_data[grouped_data["Anxiety_Group"] == selected_group]

        if not filtered_data.empty:
            # Get top country and age group based on proportions
            top_country_code = filtered_data.loc[
                filtered_data["Country_Proportion"].idxmax(), "Residence_ISO3"
            ]
            top_country = country_full_names[top_country_code]
            top_age_group = filtered_data.loc[
                filtered_data["Age_Proportion"].idxmax(), "Age_Group"
            ]

        # Get coordinates for connecting lines
        country_x = country_coords[top_country]["x"]
        country_y = country_coords[top_country]["y"]

        anxiety_x = anxiety_coords[selected_group]["x"]
        anxiety_y = anxiety_coords[selected_group]["y"]

        age_x = age_coords[top_age_group]["x"]
        age_y = age_coords[top_age_group]["y"]

        # Add line to the top country
        fig.add_trace(
            go.Scatter(
                x=[country_x, anxiety_x],
                y=[country_y, anxiety_y],
                mode="lines",
                line=dict(color="gray", width=2),
                showlegend=False,
            )
        )

        # Add line to the top age group
        fig.add_trace(
            go.Scatter(
                x=[anxiety_x, age_x],
                y=[anxiety_y, age_y],
                mode="lines",
                line=dict(color="gray", width=2),
                showlegend=False,
            )
        )

    # Update layout
    fig.update_layout(
        title="Anxiety levels by Country and Age",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            visible=False,  # Hide X-axis
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            visible=False,  # Hide Y-axis
        ),
        showlegend=False,
        height=800,
        width=1200,
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=100, b=50),
    )
    return fig


# Dash app layout
app.layout = html.Div(
    [
        html.H1("Anxiety by Country and Age"),
        dcc.Graph(id="bubble-chart", figure=create_figure()),
    ],
    style={"textAlign": "center"},
)


# Callback function
@app.callback(Output("bubble-chart", "figure"), [Input("bubble-chart", "clickData")])
def update_chart(click_data):
    if click_data and "points" in click_data:
        selected_group = click_data["points"][0]["customdata"]
        return create_figure(selected_group)
    return create_figure()


# Run Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
