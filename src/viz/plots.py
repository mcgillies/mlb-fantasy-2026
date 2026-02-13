"""
Visualization utilities for model analysis and predictions.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import shap


def plot_feature_importance(model, feature_names, top_n=20):
    """Plot top N feature importances from a tree-based model."""
    # TODO: implement feature importance bar chart
    pass


def plot_shap_summary(shap_values, X, max_display=20):
    """Plot SHAP summary (beeswarm) for the full dataset."""
    shap.summary_plot(shap_values, X, max_display=max_display)


def plot_shap_waterfall(shap_values, idx, feature_names=None):
    """Plot SHAP waterfall for a single player prediction."""
    shap.plots.waterfall(shap_values[idx])


def plot_prediction_vs_actual(y_true, y_pred, title="Predicted vs Actual"):
    """Scatter plot of predicted vs actual values."""
    # TODO: implement scatter with diagonal reference line
    pass


def plot_residuals(y_true, y_pred, title="Residuals"):
    """Plot residual distribution."""
    # TODO: implement residual histogram/scatter
    pass
