from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import json
from PIL import Image
import base64
from io import BytesIO

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
CSV_FILE_PATH = ROOT_DIR / "data" / "processed" / "processed_data.csv"
GEO_JSON_PATH = ROOT_DIR / "data" / "raw" / "world-countries.json"
GAME_LOGO_PATH = ROOT_DIR / "assets" / "game_logos"


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

    return df


def get_country_stats(df):
    """Calculate country-level statistics"""
    return (
        df.groupby("Residence_ISO3")
        .agg(
            {
                "GAD_T": "mean",
                "SWL_T": "mean",
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
        .agg({"Hours": "mean", "GAD_T": "mean", "SWL_T": "mean"})
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


@st.cache_data
def load_geojson():
    """Load and cache the world GeoJSON data"""
    try:
        with open(GEO_JSON_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading GeoJSON data: {str(e)}")
        return None


def get_country_names():
    """Get a mapping of country codes to names from the world GeoJSON"""
    world_geo = load_geojson()

    if world_geo:
        country_names = {
            feature["id"]: feature["properties"]["name"]
            for feature in world_geo["features"]
        }
        return country_names
    return {}


@st.cache_data
def get_game_logo(game_name):
    """
    Return the base64 encoded image for a given game.

    Args:
        game_name (str): Name of the game

    Returns:
        str: Base64 encoded image URL or None if logo not found
    """
    try:
        # Convert game name to filename format
        logo_path = GAME_LOGO_PATH / f"{game_name}.png"

        # Debug print
        print(f"Attempting to load logo from: {logo_path}")

        # Check if file exists
        if not logo_path.exists():
            print(f"Logo not found: {logo_path}")
            return None

        # Open and process image
        img = Image.open(str(logo_path))  # Convert Path to string for PIL

        # Convert to RGBA to ensure transparency support
        img = img.convert('RGBA')

        # Resize while maintaining aspect ratio
        img.thumbnail((150, 150))  # Adjusted size for better display

        # Save to buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")

        # Encode to base64
        img_str = base64.b64encode(buffered.getvalue()).decode()

        print(f"Successfully processed logo for {game_name}")  # Debug print
        return f"data:image/png;base64,{img_str}"

    except Exception as e:
        print(f"Error processing logo for {game_name}: {str(e)}")
        # Print the full path for debugging
        print(f"Full path attempted: {GAME_LOGO_PATH.absolute()}")
        return None
