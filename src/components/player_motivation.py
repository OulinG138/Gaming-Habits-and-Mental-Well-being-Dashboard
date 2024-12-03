import pandas as pd
import plotly.graph_objects as go
import numpy as np
import streamlit as st


def categorize_earnings(value):
    """Categorize earnings responses"""
    main_categories = [
        "I play for fun",
        "I play mostly for fun but earn a little on the side (tournament winnings, streaming, etc)",
        "I earn a living by playing this game"
    ]
    return value if value in main_categories else "Other"


def categorize_anxiety(gad_score):
    """Categorize GAD scores into anxiety levels"""
    if gad_score <= 5:
        return 0  # Low anxiety
    elif gad_score <= 10:
        return 1  # Mild anxiety
    elif gad_score <= 15:
        return 2  # Moderate anxiety
    else:
        return 3  # High anxiety


def generate_random_circle_positions(count, radius=1, center_x=0, center_y=0):
    """Generate random positions for circles within a given radius"""
    if count == 0:
        return [], []
    radii = np.sqrt(np.random.uniform(0, 1, count)) * radius
    angles = np.random.uniform(0, 2 * np.pi, count)
    x = center_x + radii * np.cos(angles)
    y = center_y + radii * np.sin(angles)
    return x, y


def get_marker_symbol(status):
    """Get the appropriate marker symbol for each employment status"""
    symbols = {
        'Employed': 'circle',
        'Student at college / university': 'star',
        'Student at school': 'diamond',
        'Unemployed / between jobs': 'triangle-up'
    }
    return symbols.get(status, 'circle')


def render_motivation_analysis(df):
    """Render the motivation analysis visualization"""

    # Create filters in columns
    col1, col2 = st.columns(2)

    with col1:
        # Multi-select for employment status
        all_employment = sorted(df['Work'].unique())
        selected_employment = st.multiselect(
            'Select Employment Status',
            options=all_employment,
            default=all_employment,
            key='employment_filter'
        )

    with col2:
        # Multi-select for anxiety levels
        anxiety_options = {
            'Low anxiety (0-5)': 0,
            'Mild anxiety (6-10)': 1,
            'Moderate anxiety (11-15)': 2,
            'High anxiety (>15)': 3
        }
        selected_anxiety = st.multiselect(
            'Select Anxiety Levels',
            options=list(anxiety_options.keys()),
            default=list(anxiety_options.keys()),
            key='anxiety_filter'
        )
        selected_anxiety_values = [anxiety_options[level]
                                   for level in selected_anxiety]

    # Create a copy and categorize data
    df = df.copy()
    df['earnings'] = df['earnings'].apply(categorize_earnings)
    df['anxiety_level'] = df['GAD_T'].apply(categorize_anxiety)

    # Apply filters
    df_filtered = df[
        (df['Work'].isin(selected_employment)) &
        (df['anxiety_level'].isin(selected_anxiety_values))
    ]

    # Get the counts for each combination
    motivation_data = (
        df_filtered.groupby(['earnings', 'Work', 'anxiety_level'])
        .size()
        .reset_index(name='count')
    )

    # Create figure
    fig = go.Figure()

    # Define categories and colors
    categories = [
        "I play for fun",
        "I play mostly for fun but earn a little on the side (tournament winnings, streaming, etc)",
        "I earn a living by playing this game",
        "Other"
    ]

    colors = ['rgb(173, 216, 235)', 'rgb(135, 206, 235)',
              'rgb(255, 160, 122)', 'rgb(255, 99, 71)']

    PEOPLE_PER_MARKER = 5  # Number of people represented by each marker

    # Track legend entries
    legend_entries = set()

    # Plot each category
    for idx, earnings in enumerate(categories):
        for employment in selected_employment:
            for anxiety_level in selected_anxiety_values:
                data = motivation_data[
                    (motivation_data['earnings'] == earnings) &
                    (motivation_data['Work'] == employment) &
                    (motivation_data['anxiety_level'] == anxiety_level)
                ]

                if len(data) > 0:
                    total_count = data['count'].iloc[0]

                    if total_count > 0:
                        # Calculate number of markers needed
                        full_markers = total_count // PEOPLE_PER_MARKER
                        remainder = total_count % PEOPLE_PER_MARKER
                        total_markers = full_markers + \
                            (1 if remainder > 0 else 0)

                        if total_markers > 0:
                            x_positions, y_positions = generate_random_circle_positions(
                                total_markers, radius=0.4, center_x=idx, center_y=0
                            )

                            marker_symbol = get_marker_symbol(employment)

                            # Create legend key
                            legend_key = f"{employment}-{anxiety_level}"
                            show_in_legend = legend_key not in legend_entries

                            # Add markers for groups of 5
                            if full_markers > 0:
                                fig.add_trace(go.Scatter(
                                    x=x_positions[:full_markers],
                                    y=y_positions[:full_markers],
                                    mode='markers',
                                    name=f"{
                                        employment} - Anxiety Level {anxiety_level}",
                                    marker=dict(
                                        size=15,  # Larger markers for full groups
                                        symbol=marker_symbol,
                                        color=colors[anxiety_level],
                                        line=dict(color='white', width=1)
                                    ),
                                    showlegend=bool(show_in_legend),
                                    hovertemplate=(
                                        f'Category: {earnings}<br>'
                                        f'Employment: {employment}<br>'
                                        f'Anxiety Level: {anxiety_level}<br>'
                                        f'Number of People: {
                                            PEOPLE_PER_MARKER}'
                                        '<extra></extra>'
                                    )
                                ))
                                legend_entries.add(legend_key)

                            # Add marker for remainder (if any)
                            if remainder > 0:
                                show_remainder_legend = bool(
                                    show_in_legend and full_markers == 0)
                                fig.add_trace(go.Scatter(
                                    x=x_positions[full_markers:],
                                    y=y_positions[full_markers:],
                                    mode='markers',
                                    name=f"{
                                        employment} - Anxiety Level {anxiety_level}",
                                    marker=dict(
                                        size=12,  # Smaller markers for remainder
                                        symbol=marker_symbol,
                                        color=colors[anxiety_level],
                                        line=dict(color='white', width=1)
                                    ),
                                    showlegend=show_remainder_legend,
                                    hovertemplate=(
                                        f'Category: {earnings}<br>'
                                        f'Employment: {employment}<br>'
                                        f'Anxiety Level: {anxiety_level}<br>'
                                        f'Number of People: {remainder}'
                                        '<extra></extra>'
                                    )
                                ))
                                if show_remainder_legend:
                                    legend_entries.add(legend_key)

    # Update layout
    fig.update_layout(
        title={
            'text': 'Gaming Motivation by Employment Status and Anxiety Level',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            ticktext=categories,
            tickvals=list(range(len(categories))),
            title='Why Play',
            showgrid=False,
            color='white',
            title_font_color='white'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        showlegend=True,
        legend=dict(
            title=dict(
                text='Employment Status & Anxiety Level',
                font=dict(color='white')
            ),
            font=dict(color='white'),
            itemsizing='constant',
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        font=dict(color='white'),
        title_font_color='white',
        margin=dict(t=100, l=50, r=50, b=50)
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
