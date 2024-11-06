import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Set up the main app layout and title
st.title("Sample Data Dashboard")

# Sidebar for user inputs
st.sidebar.header("Filter Options")
st.sidebar.subheader("Adjust data view")

# File upload (optional)
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Sample data for demonstration if no file is uploaded
    df = pd.DataFrame(
        {
            "Category": ["A", "B", "C", "D", "E"],
            "Value": np.random.randint(1, 100, 5),
            "Quantity": np.random.randint(10, 50, 5),
        }
    )

# Display raw data table
st.subheader("Data Table")
st.write("Data used for visualization:")
st.dataframe(df)

# Sidebar filter for category selection
category = st.sidebar.multiselect(
    "Select Categories",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)
filtered_df = df[df["Category"].isin(category)]

# Display filtered data table
st.subheader("Filtered Data Table")
st.write("Data after applying filters:")
st.dataframe(filtered_df)

# Plotting section
st.subheader("Bar Chart of Values by Category")
fig, ax = plt.subplots()
ax.bar(filtered_df["Category"], filtered_df["Value"], color="skyblue")
ax.set_xlabel("Category")
ax.set_ylabel("Value")
st.pyplot(fig)

# Display summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())
