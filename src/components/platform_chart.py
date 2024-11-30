import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_plotly_events import plotly_events

from utils.data_processing import get_platform_stats


def render_platform_chart(df):
    """Render gaming platform distribution sunburst chart"""

    # Create fixed container
    chart_container = st.empty()

    # Get platform statistics
    platform_stats = get_platform_stats(df)

    # Create sunburst chart
    fig = px.sunburst(
        platform_stats,
        path=["Platform", "Playstyle"],
        values="count",
        color="Platform",
        color_discrete_map={"PC": "#1f77b4", "Console": "#ff7f0e", "Mobile": "#2ca02c"},
    )

    # Update layout with more compact dimensions
    fig.update_layout(
        autosize=False,
        height=350,  # Reduced height
        margin=dict(l=0, r=0, t=30, b=0, pad=0),
        # Move title to top margin
        title=dict(
            text="Gaming Platform Distribution",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
        ),
    )

    # Add hover information
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "%{label}",
                "Count: %{value}",
                "Percentage: %{customdata[0]:.1f}%",
                "<extra></extra>",
            ]
        ),
        customdata=platform_stats[["percentage"]],
    )

    # Display chart in container
    with chart_container:
        clicked_points = plotly_events(
            fig, click_event=True, override_height=350  # Match figure height
        )

    if clicked_points:
        try:
            # Try to get the platform name from click event
            return clicked_points[0].get("label") or clicked_points[0].get("pointLabel")
        except:
            return None

    return None
