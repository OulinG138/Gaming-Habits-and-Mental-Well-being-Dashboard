import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def normalize_score(series):
    """Normalize scores to 0-100 scale"""
    return ((series - series.min()) / (series.max() - series.min())) * 100


def render_life_quality_analysis(df):
    """Render the Quality of Life analysis page with interactive controls and visualizations"""
    st.title("Quality of Life Analysis")

    # Normalize scores first
    df['GAD_T_norm'] = normalize_score(df['GAD_T'])
    df['SPIN_T_norm'] = normalize_score(df['SPIN_T'])
    df['SWL_T_norm'] = normalize_score(df['SWL_T'])

    # Create two columns for the top section
    top_left, top_right = st.columns([1, 2])

    # Top Left Column - Filters
    with top_left:
        st.markdown("### Player Type")

        # Gender selection
        gender = st.radio("Gender:", ["All", "Male", "Female"])

        # Work status selection
        work = st.radio(
            "Work Status:",
            ["All",
             "Unemployed / between jobs",
             "Employed",
             "Student at college / university",
             "Student at school"]
        )

        # Education Level with correct degrees
        education = st.radio(
            "Education Level:",
            ["All",
             "Bachelor\xa0(or equivalent)",
             "High school diploma (or equivalent)",
             "Ph.D., Psy. D., MD (or equivalent)",
             "Master\xa0(or equivalent)",
             "Other"]
        )

        # Age range slider
        age_range = st.slider(
            "Age:",
            min_value=18,
            max_value=56,
            value=(18, 56)
        )

    # Filter data based on selections
    filtered_df = df.copy()
    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    if education != "All":
        if education == "Other":
            filtered_df = filtered_df[df["Degree"].isna()]
        else:
            filtered_df = filtered_df[filtered_df["Degree"] == education]
    if work != "All":
        filtered_df = filtered_df[filtered_df["Work"] == work]

    filtered_df = filtered_df[
        (filtered_df["Age"] >= age_range[0]) &
        (filtered_df["Age"] <= age_range[1])
    ]

    # Top Right Column - Scatter Plot
    with top_right:
        st.markdown("### Quality of life")

        # Add row selection for time type
        time_type = st.radio(
            "Time Type:",
            ["Gaming Hours", "Non-Gameplay Gaming Hours"],
            horizontal=True
        )

        # Toggle between different scores
        score_type = st.radio(
            "Score Type:",
            ["General Anxiety", "Social Anxiety", "Life Satisfaction"],
            horizontal=True
        )

        # Select appropriate column based on type
        if score_type == "General Anxiety":
            score_col = 'GAD_T_norm'
            color = 'rgb(99, 110, 250)'
        elif score_type == "Social Anxiety":
            score_col = 'SPIN_T_norm'
            color = 'rgb(239, 85, 59)'
        else:  # Life Satisfaction
            score_col = 'SWL_T_norm'
            color = 'rgb(0, 204, 150)'

        # Select time column
        time_col = 'Hours' if time_type == "Gaming Hours" else 'streams'

        # Scatter plot
        fig_scatter = go.Figure()

        # Add scatter points
        fig_scatter.add_trace(
            go.Scatter(
                x=filtered_df[time_col],
                y=filtered_df[score_col],
                mode='markers',
                marker=dict(
                    color=color,
                    opacity=0.6
                ),
                name='Data points'
            )
        )

        # Add trend line
        z = np.polyfit(filtered_df[time_col], filtered_df[score_col], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(
            filtered_df[time_col].min(), filtered_df[time_col].max(), 100)
        fig_scatter.add_trace(
            go.Scatter(
                x=x_trend,
                y=p(x_trend),
                mode='lines',
                line=dict(color='#FFD700', width=2),  # Gold color
                name='Trend'
            )
        )

        fig_scatter.update_layout(
            title='Quality of Life Analysis (Normalized Scores)',
            xaxis_title=time_type,
            yaxis_title=f'{score_type} Score (0-100)',
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

    # Create two columns for the middle section
    middle_left, middle_right = st.columns([1, 1])

    # Middle Left - Distribution Plot
    with middle_left:
        # Distribution plot
        fig_dist = go.Figure()

        # Add traces for each score type
        score_columns = {
            'GAD_T_norm': ('General Anxiety', 'rgb(99, 110, 250)'),
            'SPIN_T_norm': ('Social Anxiety', 'rgb(239, 85, 59)'),
            'SWL_T_norm': ('Life Satisfaction', 'rgb(0, 204, 150)')
        }

        for col, (name, color) in score_columns.items():
            fig_dist.add_trace(
                go.Histogram(
                    x=filtered_df[col],
                    name=name,
                    nbinsx=30,
                    histnorm='percent',
                    marker_color=color,
                    opacity=0.6,
                    hovertemplate='<span style="color: ' + color + '"><b>' + name + '</b></span><br>' +
                    'Score: %{x:.1f}<br>' +
                    'Percentage: %{y:.1f}%<extra></extra>'
                )
            )

        fig_dist.update_layout(
            title="Score Distributions (Normalized)",
            xaxis_title="Score (0-100)",
            yaxis_title="Percentage of Players (%)",
            showlegend=True,
            height=500,
            bargap=0.1
        )

        st.plotly_chart(fig_dist, use_container_width=True)

    # Middle Right - Average Scores
    with middle_right:
        # Average scores bar chart
        avg_scores = {
            'General Anxiety': filtered_df['GAD_T_norm'].mean(),
            'Social Anxiety': filtered_df['SPIN_T_norm'].mean(),
            'Life Satisfaction': filtered_df['SWL_T_norm'].mean()
        }

        fig_bar = go.Figure(data=[
            go.Bar(
                x=list(avg_scores.keys()),
                y=list(avg_scores.values()),
                marker_color=['rgb(99, 110, 250)',
                              'rgb(239, 85, 59)', 'rgb(0, 204, 150)'],
                hovertemplate='<span style="color: %{marker.color}"><b>%{x}</b></span><br>' +
                'Average Score: %{y:.1f}<extra></extra>'
            )
        ])

        fig_bar.update_layout(
            title='Average Scores (Normalized)',
            xaxis_title='Score Type',
            yaxis_title='Average Score (0-100)',
            height=500,
            showlegend=False,
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # Bottom Section - Summary Statistics with Deltas
    st.markdown("### Summary Statistics")
    if gender != "All" or education != "All" or work != "All" or age_range != (18, 80):
        st.caption("↑↓ shows the difference from overall average")

    # Calculate employment percentage
    def get_employment_percentage(data):
        return (data['Work'] == 'Employed').mean() * 100

    # Calculate full dataset statistics (before filtering)
    full_stats = {
        "Players": len(df),
        "Age": df['Age'].mean(),
        "Gaming Hours": df['Hours'].mean(),
        "Non-Gameplay Gaming Hours": df['streams'].mean(),
        "General Anxiety": df['GAD_T_norm'].mean(),
        "Social Anxiety": df['SPIN_T_norm'].mean(),
        "Life Satisfaction": df['SWL_T_norm'].mean(),
        "Employment": get_employment_percentage(df)
    }

    # Calculate filtered dataset statistics
    filtered_stats = {
        "Players": len(filtered_df),
        "Age": filtered_df['Age'].mean(),
        "Gaming Hours": filtered_df['Hours'].mean(),
        "Non-Gameplay Gaming Hours": filtered_df['streams'].mean(),
        "General Anxiety": filtered_df['GAD_T_norm'].mean(),
        "Social Anxiety": filtered_df['SPIN_T_norm'].mean(),
        "Life Satisfaction": filtered_df['SWL_T_norm'].mean(),
        "Employment": get_employment_percentage(filtered_df)
    }

    # Check if any filter is applied
    is_filtered = (gender != "All" or education != "All" or
                   work != "All" or age_range != (18, 56))

    # First row of metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Number of Players",
            f"{filtered_stats['Players']:,}",
            f"{filtered_stats['Players'] -
                full_stats['Players']:,}" if is_filtered else None
        )

    with col2:
        st.metric(
            "Average Age",
            f"{filtered_stats['Age']:.1f}",
            f"{filtered_stats['Age'] - full_stats['Age']:.1f}" if is_filtered else None
        )

    with col3:
        st.metric(
            "Gaming Hours",
            f"{filtered_stats['Gaming Hours']:.1f}",
            f"{filtered_stats['Gaming Hours'] -
                full_stats['Gaming Hours']:.1f}" if is_filtered else None
        )

    with col4:
        st.metric(
            "Non-Gameplay Gaming Hours",
            f"{filtered_stats['Non-Gameplay Gaming Hours']:.1f}",
            f"{filtered_stats['Non-Gameplay Gaming Hours'] -
                full_stats['Non-Gameplay Gaming Hours']:.1f}" if is_filtered else None
        )

    # Second row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "General Anxiety",
            f"{filtered_stats['General Anxiety']:.1f}",
            f"{filtered_stats['General Anxiety'] -
                full_stats['General Anxiety']:.1f}" if is_filtered else None
        )

    with col2:
        st.metric(
            "Social Anxiety",
            f"{filtered_stats['Social Anxiety']:.1f}",
            f"{filtered_stats['Social Anxiety'] -
                full_stats['Social Anxiety']:.1f}" if is_filtered else None
        )

    with col3:
        st.metric(
            "Life Satisfaction",
            f"{filtered_stats['Life Satisfaction']:.1f}",
            f"{filtered_stats['Life Satisfaction'] -
                full_stats['Life Satisfaction']:.1f}" if is_filtered else None
        )

    with col4:
        st.metric(
            "Employment Rate",
            f"{filtered_stats['Employment']:.1f}%",
            f"{filtered_stats['Employment'] -
                full_stats['Employment']:.1f}" if is_filtered else None
        )
