"""
Data processing and cleaning.

Merges base stats with advanced metrics, handles name normalization,
and creates the combined dataset for modeling.
"""

import pandas as pd
import unidecode
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR


def normalize_names(df, name_col="Name"):
    """Standardize player names (unicode, formatting)."""
    df[name_col] = df[name_col].apply(unidecode.unidecode)
    return df


def merge_stats_and_metrics(stats_df, metrics_df, on=["player_id", "year"]):
    """
    Merge base stats with advanced metrics.
    Metrics are lagged by 1 year (previous year metrics predict current year).
    """
    # TODO: implement merge with year lag
    pass


def combine_batter_data():
    """Load and combine all batter data sources."""
    # TODO: load raw data, merge, save to PROCESSED_DATA_DIR
    pass


def combine_pitcher_data():
    """Load and combine all pitcher data sources."""
    # TODO: load raw data, merge, save to PROCESSED_DATA_DIR
    pass
