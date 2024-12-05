import pandas as pd
import plotly.express as px
import streamlit as st

def group_playstyles(playstyle):
    if "Singleplayer" in playstyle:
        return "Single Player"
    elif "Multiplayer - offline" in playstyle:
        return "Multiplayer - offline (same room)"
    elif "Multiplayer - online - with strangers" in playstyle:
        return "Multiplayer - online (with strangers)"
    elif "Multiplayer - online - with online acquaintances" in playstyle:
        return "Multiplayer - online (with online acquaintances/teammates)"
    elif "Multiplayer - online - with real life friends" in playstyle:
        return "Multiplayer - online (with real-life friends)"
    else:
        return "Others"

def categorize_anxiety(score):
    if score <= 7:
        return "Low Anxiety"
    elif score <= 14:
        return "Moderate Anxiety"
    else:
        return "High Anxiety"

def render_playstyle_anxiety_sunburst_chart(df, game=None):
    """Render a sunburst chart of playstyles and anxiety levels."""
    # Apply the playstyle grouping
    df['Grouped_Playstyle'] = df['Playstyle'].apply(group_playstyles)
    
    # Filter by game if specified
    if game and game != "All":
        df = df[df["Game"] == game]
    
    # Check if DataFrame is empty after filtering
    if df.empty:
        st.write("No data available for the selected game.")
        return
    
    # Ensure the anxiety score column exists
    if 'GAD_T' not in df.columns:
        st.write("Anxiety Score column 'GAD_T' not found in the DataFrame.")
        return
    
    # Categorize anxiety levels
    df['Anxiety_Level'] = df['GAD_T'].apply(categorize_anxiety)
    
    # Count occurrences for each combination of playstyle and anxiety level
    counts = df.groupby(['Grouped_Playstyle', 'Anxiety_Level']).size().reset_index(name='Count')
    
    # Define custom colors for playstyles
    playstyle_colors = {
        "Single Player": '#6ee7b7',  # Light blue
        "Multiplayer - offline (same room)": '#60a5fa',  # Blue
        "Multiplayer - online (with online acquaintances/teammates)": '#2563eb',  # Dark blue
        "Multiplayer - online (with real-life friends)": '#fca5a5',  # Red
        "Multiplayer - online (with strangers)": '#ef4444',  # Dark red
        "Others": '#10b981'  # Green
    }
    
    anxiety_colors = {
        'Low Anxiety': '#60a5fa',  # Light blue
        'Moderate Anxiety': '#f77676',  # Light red
        'High Anxiety': '#a855f7'  # Purple
    }
    
    # Create the sunburst chart
    fig = px.sunburst(
        counts,
        path=['Grouped_Playstyle', 'Anxiety_Level'],
        values='Count',
        color='Grouped_Playstyle',
        color_discrete_map=playstyle_colors,
        title=f"Playstyle and Anxiety Level Distribution{' for ' + game if game and game != 'All' else ''}",
    )
    
    # Update the layout for a dark theme
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        height=500,
        font=dict(color='white'),   # White text
    )
    
    # Adjust the hover information
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent:.2%}',
    )
    
    # Render the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
