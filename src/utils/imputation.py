"""
Missing data imputation strategies.

Handles rookies, injured players, and other cases where
previous-year data is unavailable.
"""

import pandas as pd
import numpy as np


def impute_rookies(df, feature_cols, strategy="league_mean"):
    """
    Impute missing features for rookies (no MLB history).

    Strategies:
        - 'league_mean': Use league average for the feature.
        - 'position_mean': Use position-specific average.
        - 'minor_league': Map from minor league stats (if available).
        - 'projections': Use external projection systems.

    Args:
        df: DataFrame with potential NaN rows for rookies.
        feature_cols: Columns to impute.
        strategy: Imputation strategy.

    Returns:
        DataFrame with imputed values.
    """
    # TODO: implement imputation strategies
    pass


def impute_injured(df, feature_cols, min_games=20):
    """
    Impute stats for players with limited playing time due to injury.

    Uses the most recent full season, or a weighted average of
    available seasons if none meet the threshold.

    Args:
        df: DataFrame with player histories.
        feature_cols: Columns to impute.
        min_games: Minimum games to consider a "full" season.

    Returns:
        DataFrame with imputed values for injured players.
    """
    # TODO: implement injured player imputation
    pass


def flag_data_quality(df, min_pa=None, min_ip=None):
    """
    Add flags indicating data quality/reliability for each player-year.

    Flags: is_rookie, is_injured_season, small_sample, has_imputed_data.
    """
    # TODO: implement quality flags
    pass
