"""
Data collection using pybaseball.

Pulls historical stats and advanced metrics from Baseball Savant / FanGraphs.
"""

import pandas as pd
from pybaseball import (
    batting_stats,
    pitching_stats,
    statcast_batter_expected_stats,
    statcast_pitcher_expected_stats,
    cache,
)
from config.settings import (
    TRAIN_START_YEAR,
    TRAIN_END_YEAR,
    PREDICT_YEAR,
    RAW_DATA_DIR,
    PYBASEBALL_CACHE_DIR,
    MIN_PA_BATTER,
    MIN_IP_PITCHER,
)

# Enable pybaseball caching to avoid redundant API calls
cache.enable()


def collect_batting_stats(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, qual=MIN_PA_BATTER):
    """Collect batting stats from FanGraphs for the given year range."""
    # TODO: pull batting stats, save to RAW_DATA_DIR
    pass


def collect_pitching_stats(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, qual=MIN_IP_PITCHER):
    """Collect pitching stats from FanGraphs for the given year range."""
    # TODO: pull pitching stats, save to RAW_DATA_DIR
    pass


def collect_statcast_batter_metrics(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_pa=MIN_PA_BATTER):
    """Collect Statcast expected stats and advanced metrics for batters."""
    # TODO: pull expected stats (xBA, xSLG, xwOBA, barrel%, etc.)
    pass


def collect_statcast_pitcher_metrics(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_ip=MIN_IP_PITCHER):
    """Collect Statcast expected stats and advanced metrics for pitchers."""
    # TODO: pull expected stats, pitch characteristics, etc.
    pass


def collect_all():
    """Run all data collection steps."""
    print("Collecting batting stats...")
    collect_batting_stats()
    print("Collecting pitching stats...")
    collect_pitching_stats()
    print("Collecting Statcast batter metrics...")
    collect_statcast_batter_metrics()
    print("Collecting Statcast pitcher metrics...")
    collect_statcast_pitcher_metrics()
    print("Data collection complete.")


if __name__ == "__main__":
    collect_all()
