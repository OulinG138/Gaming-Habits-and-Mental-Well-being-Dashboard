import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 加载数据
data = pd.read_csv("data/processed/processed_data.csv")

# 定义焦虑分数和年龄分组
anxiety_bins = [0, 5, 10, 15, 21]
anxiety_labels = ["0-5", "6-10", "11-15", "16-21"]
data["Anxiety_Group"] = pd.cut(
    data["GAD_T"].astype(float),
    bins=anxiety_bins,
    labels=anxiety_labels,
    include_lowest=True,
)

age_bins = [18, 25, 35, 45, 56]
age_labels = ["18-25", "26-35", "36-45", "46-56"]
data["Age_Group"] = pd.cut(
    data["Age"].astype(float), bins=age_bins, labels=age_labels, include_lowest=True
)

# 筛选主要国家（数量最多的前 5 个）
top_countries = data["Residence_ISO3"].value_counts().head(5).index
data = data[data["Residence_ISO3"].isin(top_countries)]

# 统计分组数据
grouped_data = (
    data.groupby(["Anxiety_Group", "Residence_ISO3", "Age_Group"])
    .size()
    .reset_index(name="Count")
)

# 初始化 session state 来记录用户点击的焦虑分组
if "selected_group" not in st.session_state:
    st.session_state["selected_group"] = None


# 函数：生成图表
def create_figure(selected_group=None):
    fig = go.Figure()

    # 焦虑分数气泡（中间）
    anxiety_groups = grouped_data.groupby("Anxiety_Group")["Count"].sum().reset_index()
    for i, row in anxiety_groups.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[0],
                y=[i],  # 中间位置
                mode="markers+text",
                marker=dict(
                    size=max(10, min(row["Count"] * 2, 50)), color="red", opacity=0.8
                ),
                name=row["Anxiety_Group"],
                text=row["Anxiety_Group"],
                textposition="top center",
                hoverinfo="text",
                customdata=[row["Anxiety_Group"]],  # 自定义数据用于点击事件
            )
        )

    # 国家气泡（左侧）
    countries = grouped_data.groupby("Residence_ISO3")["Count"].sum().reset_index()
    for i, row in countries.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[-1],
                y=[i],  # 左侧位置
                mode="markers+text",
                marker=dict(
                    size=max(10, min(row["Count"] * 2, 50)), color="blue", opacity=0.8
                ),
                name=row["Residence_ISO3"],
                text=row["Residence_ISO3"],
                textposition="middle right",
                hoverinfo="text",
            )
        )

    # 年龄组气泡（右侧）
    age_groups = grouped_data.groupby("Age_Group")["Count"].sum().reset_index()
    for i, row in age_groups.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[i],  # 右侧位置
                mode="markers+text",
                marker=dict(
                    size=max(10, min(row["Count"] * 2, 50)), color="yellow", opacity=0.8
                ),
                name=row["Age_Group"],
                text=row["Age_Group"],
                textposition="middle left",
                hoverinfo="text",
            )
        )

    # 添加连接线（如果选择了焦虑分组）
    if selected_group:
        filtered_data = grouped_data[grouped_data["Anxiety_Group"] == selected_group]
        for _, row in filtered_data.iterrows():
            # 连接到国家
            country_index = list(countries["Residence_ISO3"]).index(
                row["Residence_ISO3"]
            )
            fig.add_trace(
                go.Scatter(
                    x=[0, -1],
                    y=[
                        anxiety_groups[
                            anxiety_groups["Anxiety_Group"] == selected_group
                        ].index[0],
                        country_index,
                    ],
                    mode="lines",
                    line=dict(color="gray", width=1),
                    showlegend=False,
                )
            )
            # 连接到年龄组
            age_index = list(age_groups["Age_Group"]).index(row["Age_Group"])
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[
                        anxiety_groups[
                            anxiety_groups["Anxiety_Group"] == selected_group
                        ].index[0],
                        age_index,
                    ],
                    mode="lines",
                    line=dict(color="gray", width=1),
                    showlegend=False,
                )
            )

    # 更新布局
    fig.update_layout(
        title="Interactive Bubble Chart: Anxiety Levels by Country and Age",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        height=600,
        width=900,
    )
    return fig


# 创建图表并显示
st.plotly_chart(create_figure(st.session_state["selected_group"]))

# 捕获点击事件
clicked_point = st.session_state.get("selected_group")

# 更新 session state（用于捕获点击的焦虑分组）
if clicked_point:
    st.session_state["selected_group"] = clicked_point
