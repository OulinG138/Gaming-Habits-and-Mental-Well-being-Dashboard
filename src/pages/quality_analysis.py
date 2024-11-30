import streamlit as st

from components.life_quality import render_life_quality_analysis


def render(df):
    """Render the Quality of Life analysis page"""

    st.header("Quality of Life Analysis")

    # Create sidebar filters
    st.sidebar.header("Demographic Filters")

    # Gender filter
    gender = st.sidebar.radio(
        "Gender:", ["All"] + sorted(df["Gender"].unique().tolist())
    )

    # Education level filter
    education = st.sidebar.radio(
        "Education Level:",
        ["All", "High School", "Bachelor", "Master", "Ph.D.", "Others"],
    )

    # Age range slider
    age_range = st.sidebar.slider(
        "Age Range:",
        min_value=int(df["Age"].min()),
        max_value=int(df["Age"].max()),
        value=(18, 35),
    )

    # Apply filters
    filtered_df = df.copy()
    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    if education != "All":
        filtered_df = filtered_df[
            filtered_df["Degree"].str.contains(education, case=False)
        ]
    filtered_df = filtered_df[
        (filtered_df["Age"] >= age_range[0]) & (filtered_df["Age"] <= age_range[1])
    ]

    # Main content area
    col1, col2 = st.columns([1, 3])

    with col1:
        # Anxiety type selector
        anxiety_type = st.radio(
            "Analysis Type:", ["General Anxiety", "Social Anxiety"], key="anxiety_type"
        )

    with col2:
        # Render main visualization
        render_life_quality_analysis(
            filtered_df, "general" if anxiety_type == "General Anxiety" else "social"
        )

    # Additional statistics
    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Life Satisfaction",
            f"{filtered_df['SWL_T'].mean():.1f}",
            f"{filtered_df['SWL_T'].mean() - df['SWL_T'].mean()
                                         :.1f} vs overall",
        )

    with col2:
        st.metric(
            "Average Gaming Hours",
            f"{filtered_df['Hours'].mean():.1f}",
            f"{filtered_df['Hours'].mean() - df['Hours'].mean()
                                         :.1f} vs overall",
        )

    with col3:
        st.metric(
            "Sample Size", len(filtered_df), f"{len(filtered_df) - len(df)} vs total"
        )
