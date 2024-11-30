import streamlit as st

from components.platform_chart import render_platform_chart
from components.score_radar import render_score_radar


def render(df):
    """Render the Kind of Game analysis page"""

    # Create main container
    main_container = st.container()

    with main_container:
        st.header("Gaming Platform Analysis")

        # Use columns for layout
        charts_col, filters_col = st.columns([3, 1])

        with charts_col:
            # Fixed size container for sunburst
            platform_container = st.container()
            with platform_container:
                selected_platform = render_platform_chart(df)

            # Add some space
            st.write("")

            # Container for radar chart
            radar_container = st.container()
            with radar_container:
                st.subheader("Score Distribution by Gaming Style")
                # Filter data based on platform selection
                filtered_df = (
                    df[df["Platform"] == selected_platform]
                    if selected_platform and selected_platform != "All"
                    else df
                )
                render_score_radar(filtered_df, selected_platform)

        with filters_col:
            st.subheader("Filters")
            # Platform selector
            platforms = ["All"] + sorted(df["Platform"].unique().tolist())
            selected_platform = st.selectbox(
                "Select Platform", platforms, key="platform_selector"
            )

            # Playstyle selector
            st.write("")
            playstyles = sorted(df["Playstyle"].unique().tolist())
            selected_playstyles = st.multiselect(
                "Select Playstyles",
                playstyles,
                default=playstyles[:2],
                key="playstyle_selector",
            )

            # Show some metrics
            st.write("")
            st.subheader("Key Metrics")
            if selected_platform != "All":
                platform_data = df[df["Platform"] == selected_platform]
                st.metric(
                    "Average Gaming Hours",
                    f"{platform_data['Hours'].mean():.1f}",
                    f"{platform_data['Hours'].mean(
                    ) - df['Hours'].mean():.1f} vs overall",
                )
                st.metric(
                    "Average Anxiety Score",
                    f"{platform_data['GAD_T'].mean():.1f}",
                    f"{platform_data['GAD_T'].mean(
                    ) - df['GAD_T'].mean():.1f} vs overall",
                )
