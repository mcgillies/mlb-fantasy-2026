"""
Feature engineering for model training.

Creates lagged features, historical fantasy point averages,
and other derived features including sub-season splits.
"""

import pandas as pd
import numpy as np
from config.settings import RANDOM_STATE


def create_lag_features(df, group_col="player_id", value_cols=None, lags=[1, 2]):
    """
    Create lagged versions of features (previous 1-2 seasons).

    Each row already has metrics from year N-1 predicting year N fpoints.
    This adds year N-2 metrics as additional features for multi-year context.

    Args:
        df: DataFrame sorted by player and year.
        group_col: Column to group by (player identifier).
        value_cols: Columns to create lags for.
        lags: List of lag periods (1 = already present via the merge,
              2 = two seasons back).

    Returns:
        DataFrame with lag columns added (e.g., xBA_lag2).
    """
    # TODO: implement lag feature creation
    pass


def create_historical_fpoints(df, group_col="player_id", fpoints_col="Fpoints_PA", windows=[2, 3]):
    """
    Create rolling average of historical fantasy points per PA/IP.

    Provides a smoothed view of a player's recent production,
    more robust than a single season.

    Args:
        df: DataFrame with fpoints_col column, sorted by player and year.
        group_col: Column to group by.
        fpoints_col: Fantasy points rate column.
        windows: Rolling window sizes (in years).

    Returns:
        DataFrame with rolling avg columns (e.g., Fpoints_PA_avg2, Fpoints_PA_avg3).
    """
    # TODO: implement rolling historical fpoints
    pass


def create_second_half_features(df, second_half_df, group_col="player_id", value_cols=None):
    """
    Add second-half-of-season metrics as features.

    Captures late-season breakouts, mechanical changes, and trends
    that full-season averages may dilute.

    Args:
        df: Main DataFrame (full-season data).
        second_half_df: DataFrame with post-ASB stats/metrics.
        group_col: Player identifier column.
        value_cols: Metric columns to include from second half.

    Returns:
        DataFrame with second-half features added (e.g., xBA_2H).
    """
    # TODO: implement second-half feature merging
    pass


def create_delta_features(df, group_col="player_id", value_cols=None):
    """
    Create year-over-year change features for key metrics.

    Captures improvement/decline trends (e.g., a pitcher gaining
    2 mph on their fastball year-over-year).

    Args:
        df: DataFrame sorted by player and year with lag features present.
        group_col: Player identifier.
        value_cols: Metrics to compute deltas for.

    Returns:
        DataFrame with delta columns added (e.g., xBA_delta).
    """
    # TODO: implement delta features
    pass


def build_feature_matrix(df, target_col, feature_cols=None, drop_cols=None):
    """
    Build the final feature matrix for model training.

    Args:
        df: Combined DataFrame with all features.
        target_col: Name of the target variable.
        feature_cols: Explicit list of features to use (optional).
        drop_cols: Columns to drop from features (optional).

    Returns:
        X (features DataFrame), y (target Series)
    """
    # TODO: implement feature matrix construction
    pass
