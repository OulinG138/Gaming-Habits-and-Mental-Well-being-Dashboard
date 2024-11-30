from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
CSV_FILE_PATH = ROOT_DIR / "data" / "processed" / "processed_data.csv"


@st.cache_data
def load_data():
    """Load and process the gaming survey data"""
    df = pd.read_csv(CSV_FILE_PATH)

    # Basic processing
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    # Create age groups
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 22, 26, 30, 35, float("inf")],
        labels=["18-22", "22-26", "26-30", "30-35", "35+"],
    )

    # Process gaming platforms
    df["Platform"] = df["Platform"].fillna("Other")
    df["Platform"] = df["Platform"].apply(
        lambda x: (
            "PC"
            if "PC" in str(x)
            else (
                "Console"
                if "Console" in str(x)
                else ("Mobile" if "Mobile" in str(x) else "Other")
            )
        )
    )

    # Calculate anxiety scores
    df["GAD_Total"] = df[["GAD1", "GAD2", "GAD3", "GAD4", "GAD5", "GAD6", "GAD7"]].sum(
        axis=1
    )
    df["SWL_Total"] = df[["SWL1", "SWL2", "SWL3", "SWL4", "SWL5"]].sum(axis=1)

    return df


def get_country_stats(df):
    """Calculate country-level statistics"""
    return (
        df.groupby("Residence_ISO3")
        .agg(
            {
                "GAD_Total": "mean",
                "SWL_Total": "mean",
                "SPIN_T": "mean",
                "Hours": "mean",
            }
        )
        .reset_index()
    )


def get_age_stats(df):
    """Calculate age group statistics"""
    return (
        df.groupby("AgeGroup")
        .agg({"Hours": "mean", "GAD_Total": "mean", "SWL_Total": "mean"})
        .reset_index()
    )


def get_platform_stats(df):
    """Calculate gaming platform statistics"""
    platform_stats = (
        df.groupby(["Platform", "Playstyle"]).size().reset_index(name="count")
    )
    platform_stats["percentage"] = platform_stats.groupby("Platform")[
        "count"
    ].transform(lambda x: x / x.sum() * 100)
    return platform_stats
