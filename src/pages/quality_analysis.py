import streamlit as st

from components.life_quality import render_life_quality_analysis


def render(df):
    """Render the Quality of Life analysis page"""
    render_life_quality_analysis(df)
