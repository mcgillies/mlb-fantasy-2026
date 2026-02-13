"""
Streamlit app for interactive fantasy point predictions.

Features:
- Select a player from dropdown
- View predicted fantasy points (rate and total)
- View SHAP waterfall plot showing feature contributions
- Compare with external projections
"""

import streamlit as st
import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt


def load_data():
    """Load prediction data and trained models."""
    # TODO: load predictions, feature data, and models
    pass


def get_shap_explanation(model, X, player_idx):
    """Generate SHAP values for a single player."""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X)
    return shap_values[player_idx]


def main():
    st.title("MLB Fantasy 2026 Predictions")
    st.sidebar.header("Player Selection")

    # TODO: implement player selection, prediction display, and SHAP plot
    # Skeleton:
    # 1. Load data and models
    # 2. Sidebar: select batter/pitcher, then select player
    # 3. Main area: show prediction details
    # 4. Show SHAP waterfall plot

    st.info("App under construction. Train models first, then update this app.")


if __name__ == "__main__":
    main()
