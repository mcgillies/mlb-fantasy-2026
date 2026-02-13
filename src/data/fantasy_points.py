"""
Fantasy points calculation.

Applies the league scoring rules to raw stats to compute
total and rate-based fantasy points.

Note on pitcher scoring: W/L/Hold/Save are intentionally excluded from the
model training target. These are team-dependent outcomes that don't correlate
well with individual pitcher skill. The model predicts skill-based Fpoints/IP,
and W/L/Hold/Save contributions are added separately using external projections.
"""

import pandas as pd
from config.scoring import BATTER_SCORING, PITCHER_SCORING_SKILL, PITCHER_SCORING_TEAM


def calc_fpoints_batter(df):
    """
    Calculate fantasy points for batters.

    Args:
        df: DataFrame with columns matching BATTER_SCORING keys + PA column.

    Returns:
        DataFrame with added Fpoints and Fpoints_PA columns.
    """
    df = df.copy()
    df["Fpoints"] = sum(df[stat] * weight for stat, weight in BATTER_SCORING.items())
    df["Fpoints_PA"] = df["Fpoints"] / df["PA"]
    return df


def calc_fpoints_pitcher_skill(df):
    """
    Calculate skill-based fantasy points for pitchers (excludes W/L/Hold/Save).
    This is the target for model training.

    Args:
        df: DataFrame with columns matching PITCHER_SCORING_SKILL keys.

    Returns:
        DataFrame with added Fpoints_skill and Fpoints_IP columns.
    """
    df = df.copy()
    df["Fpoints_skill"] = sum(df[stat] * weight for stat, weight in PITCHER_SCORING_SKILL.items())
    df["Fpoints_IP"] = df["Fpoints_skill"] / df["IP"]
    return df


def calc_fpoints_pitcher_team(df):
    """
    Calculate team-dependent fantasy point contributions (W/L/Hold/Save).
    Applied at prediction time using external projections.

    Args:
        df: DataFrame with projected W, L, Hold, S columns.

    Returns:
        DataFrame with added Fpoints_team column.
    """
    df = df.copy()
    df["Fpoints_team"] = sum(df[stat] * weight for stat, weight in PITCHER_SCORING_TEAM.items())
    return df


def calc_fpoints_pitcher_total(df):
    """
    Combine skill-based and team-based pitcher fantasy points.
    Used at the final prediction stage.

    Args:
        df: DataFrame with Fpoints_skill and Fpoints_team columns.

    Returns:
        DataFrame with added Fpoints_total column.
    """
    df = df.copy()
    df["Fpoints_total"] = df["Fpoints_skill"] + df["Fpoints_team"]
    return df
