import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from .constants import *


def create_color_scale(values, color_range=ANXIETY_COLORS):
    """Create a color scale based on value ranges"""
    normalized = (values - values.min()) / (values.max() - values.min())
    return [color_range[get_intensity(v)] for v in normalized]


def get_intensity(value):
    """Get color intensity category based on value"""
    if value < 0.33:
        return "low"
    elif value < 0.66:
        return "medium"
    return "high"


def create_base_layout(title, height=CHART_HEIGHT):
    """Create a base layout for plotly charts"""
    return dict(
        title=title,
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="closest",
    )


def add_hover_template(fig, data_dict, suffix=""):
    """Add hover template to figure"""
    hover_template = "<br>".join(
        [f"{k}: {v:,.1f}{suffix}" for k, v in data_dict.items()]
    )
    fig.update_traces(hovertemplate=hover_template + "<extra></extra>")
    return fig


def create_trend_line(x, y):
    """Create trend line data"""
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_range = np.linspace(x.min(), x.max(), 100)
    return x_range, p(x_range)


def update_chart_axes(fig, x_title, y_title, x_range=None, y_range=None):
    """Update chart axes with titles and ranges"""
    updates = dict(xaxis_title=x_title, yaxis_title=y_title)
    if x_range:
        updates["xaxis_range"] = x_range
    if y_range:
        updates["yaxis_range"] = y_range
    fig.update_layout(**updates)
    return fig


def format_metric_value(value, precision=1):
    """Format metric values with appropriate precision"""
    return f"{value:,.{precision}f}"


def calculate_delta(value, baseline):
    """Calculate and format delta for metrics"""
    delta = value - baseline
    return f"{delta:+.1f}"
