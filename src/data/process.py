"""
Data processing and feature engineering.

Calculates fantasy points, selects key features based on predictive correlation,
creates lag features, rolling averages, and merges data sources.
"""

import os
import pandas as pd
import numpy as np

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR
from config.scoring import BATTER_SCORING, PITCHER_SCORING_SKILL

# Feature selections: skill-based descriptive metrics only
# Excludes traditional outcome stats (AVG, OBP, SLG, wOBA, etc.) which are
# derived from the same counting stats as fantasy points and don't add
# predictive power for identifying breakouts/declines.

# =============================================================================
# EXPANDED FEATURE SETS (balanced interpretability and coverage)
# Selected based on multicollinearity analysis in notebook 07
# Some correlation is acceptable - different measurements of related skills
# =============================================================================

BATTER_FEATURES = [
    # Expected stats - both provide nuance
    'xwOBA', 'xBA',
    # Batted ball quality - fuller coverage
    'EV', 'maxEV', 'Barrel%', 'HardHit%',
    # Plate discipline - complete picture
    'K%', 'BB%', 'SwStr%',
    'O-Contact%', 'Z-Contact%',  # Contact in/outside zone
    'O-Swing%',  # Chase rate
    # Batted ball profile
    'FB%', 'HR/FB', 'Pull%',
    # Speed
    'Spd',
    # Age (NOTE: excluded from trend - always increases by 1)
    'Age',
]

# Features to EXCLUDE from trend calculation (Age trend is useless - always ~1)
EXCLUDE_FROM_TREND = ['Age']

PITCHER_FEATURES = [
    # K/BB skills
    'K%', 'BB%',
    # Whiff/Contact metrics
    'SwStr%', 'O-Swing%', 'O-Contact%',
    # Run prevention estimators (xERA + SIERA for different approaches)
    'xERA', 'SIERA',
    # Batted ball quality/profile
    'Barrel%', 'GB%',
    # Stuff quality composite
    'Stuff+',
    # Age (NOTE: excluded from trend)
    'Age',
]

# =============================================================================
# FULL FEATURE SETS (original - commented out for reference)
# Uncomment these and comment out the reduced sets above to use full features
# =============================================================================

# BATTER_FEATURES_FULL = [
#     # Expected stats (Statcast) - what contact quality SHOULD produce
#     'xBA', 'xSLG', 'xwOBA',
#     # Batted ball quality - raw skill indicators
#     'EV', 'maxEV', 'Barrel%', 'HardHit%', 'Hard%',
#     # Plate discipline - approach and contact skills
#     'K%', 'BB%', 'BB/K', 'SwStr%', 'Contact%', 'O-Contact%', 'Z-Contact%',
#     'O-Swing%', 'Z-Swing%', 'Zone%',
#     # Batted ball distribution - batted ball tendencies
#     'GB%', 'FB%', 'LD%', 'HR/FB', 'Pull%',
#     # Speed
#     'Spd',
#     # Age
#     'Age',
# ]

# PITCHER_FEATURES_FULL = [
#     # Strikeout/walk skills - core pitching skills
#     'K%', 'K/9', 'K-BB%', 'K/BB', 'BB%', 'BB/9',
#     # Whiff/contact - pitch quality indicators
#     'SwStr%', 'Contact%', 'Z-Contact%', 'O-Contact%', 'O-Swing%',
#     # Expected/estimator stats - skill-based run prevention estimators
#     'xERA', 'xFIP', 'SIERA', 'FIP',
#     # Batted ball quality allowed - contact quality against
#     'EV', 'Barrel%', 'HardHit%',
#     # Batted ball distribution - batted ball tendencies allowed
#     'GB%', 'FB%', 'LD%', 'HR/FB',
#     # Rate stats (descriptive, not outcome-based)
#     'H/9', 'HR/9',
#     # Pitch velocity by type (using pitch info format where available)
#     'FBv',        # Fastball (old format)
#     'vSI (pi)',   # Sinker
#     'vFC (pi)',   # Cutter
#     'SLv',        # Slider (old format)
#     'CHv',        # Changeup (old format)
#     'vCU (pi)',   # Curveball
#     'vFS (pi)',   # Splitter
#     # Pitch usage
#     'FA% (pi)',   # Fastball
#     'SI% (pi)',   # Sinker
#     'FC% (pi)',   # Cutter
#     'SL%',        # Slider (old format)
#     'CH%',        # Changeup (old format)
#     'CU% (pi)',   # Curveball
#     'FS% (pi)',   # Splitter
#     # Pitch movement (horizontal X, vertical Z) - all main pitch types
#     'FA-X (pi)', 'FA-Z (pi)',  # Fastball
#     'SI-X (pi)', 'SI-Z (pi)',  # Sinker
#     'FC-X (pi)', 'FC-Z (pi)',  # Cutter
#     'SL-X (pi)', 'SL-Z (pi)',  # Slider
#     'CH-X (pi)', 'CH-Z (pi)',  # Changeup
#     'CU-X (pi)', 'CU-Z (pi)',  # Curveball
#     'FS-X (pi)', 'FS-Z (pi)',  # Splitter
#     # Stuff+ metrics (pitch quality grades)
#     'Stuff+', 'Pitching+',
#     # Age
#     'Age',
# ]


def ensure_processed_dir():
    """Create processed data directory if it doesn't exist."""
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def calculate_batter_fpoints(df):
    """
    Calculate fantasy points for batters.

    TB = 1B + 2*2B + 3*3B + 4*HR
    Fpoints = TB + R + RBI + BB + SB - K
    Fpoints_PA = Fpoints / PA
    """
    df = df.copy()

    # Calculate TB if not present
    if 'TB' not in df.columns:
        df['TB'] = df['1B'] + 2*df['2B'] + 3*df['3B'] + 4*df['HR']

    # Calculate fantasy points using scoring config
    df['Fpoints'] = (
        df['TB'] * BATTER_SCORING['TB'] +
        df['R'] * BATTER_SCORING['R'] +
        df['RBI'] * BATTER_SCORING['RBI'] +
        df['BB'] * BATTER_SCORING['BB'] +
        df['SB'] * BATTER_SCORING['SB'] +
        df['SO'] * BATTER_SCORING['K']  # Note: K maps to SO in FanGraphs
    )

    df['Fpoints_PA'] = df['Fpoints'] / df['PA']

    return df


def calculate_pitcher_fpoints(df):
    """
    Calculate skill-based fantasy points for pitchers.
    Excludes W/L/Hold/Save (team-dependent).

    Fpoints_skill = 3*IP + K - BB - H - 2*ER
    Fpoints_IP = Fpoints_skill / IP
    """
    df = df.copy()

    df['Fpoints_skill'] = (
        df['IP'] * PITCHER_SCORING_SKILL['IP'] +
        df['SO'] * PITCHER_SCORING_SKILL['K'] +
        df['BB'] * PITCHER_SCORING_SKILL['BB'] +
        df['H'] * PITCHER_SCORING_SKILL['H'] +
        df['ER'] * PITCHER_SCORING_SKILL['ER']
    )

    df['Fpoints_IP'] = df['Fpoints_skill'] / df['IP']

    return df


def create_lag_features(df, id_col, year_col, feature_cols, lags=[1, 2], exclude_from_trend=None):
    """
    Create lagged features using level + trend approach.

    Instead of multiple correlated lag features (lag1, lag2), this creates:
    - _lag1: Recent level (year N-1 metrics)
    - _trend: Direction of change (lag1 - lag2), capturing improvement/decline
    - has_trend: Indicator (1 if trend data exists, 0 if not)

    This makes features more orthogonal - one captures current state,
    one captures whether the player is improving or declining.

    Args:
        df: DataFrame with player data
        id_col: Column identifying players (e.g., 'IDfg')
        year_col: Column identifying seasons (e.g., 'Season')
        feature_cols: List of metric columns to create lag/trend features for
        lags: List of lag periods (default [1, 2] for level + trend)
        exclude_from_trend: List of features to exclude from trend calculation
                           (e.g., Age - always increases by 1, useless as trend)

    Returns:
        DataFrame with _lag1 (level), _trend (direction), and has_trend indicator
    """
    if exclude_from_trend is None:
        exclude_from_trend = []

    df = df.sort_values([id_col, year_col]).copy()

    # Create lag1 (level - most recent season)
    lag1 = df.groupby(id_col)[feature_cols].shift(1)
    lag1.columns = [f'{c}_lag1' for c in feature_cols]

    # Create lag2 (needed to compute trend)
    lag2 = df.groupby(id_col)[feature_cols].shift(2)

    # Features to include in trend calculation
    trend_features = [c for c in feature_cols if c not in exclude_from_trend]

    # Create trend features (lag1 - lag2 = direction of change)
    # Positive trend = improving, negative trend = declining
    trend_data = {}
    for c in trend_features:
        trend_data[f'{c}_trend'] = lag1[f'{c}_lag1'].values - lag2[c].values
    trend_df = pd.DataFrame(trend_data, index=df.index)

    # Create has_trend indicator (1 if player has 2+ years of data, 0 otherwise)
    # This helps the model know if trend values are real or will be imputed
    has_trend = (~lag2[feature_cols[0]].isna()).astype(int)
    has_trend_df = pd.DataFrame({'has_trend': has_trend}, index=df.index)

    result = pd.concat([df, lag1, trend_df, has_trend_df], axis=1)
    return result


def create_rolling_features(df, id_col, year_col, feature_cols, windows=[2, 3]):
    """
    Create rolling average features (2-3 year windows).

    Uses shift(1) so we only use data available before the prediction year.
    """
    df = df.sort_values([id_col, year_col]).copy()

    rolling_dfs = []

    for window in windows:
        # Use min_periods=1 to handle players with fewer seasons
        rolled = df.groupby(id_col)[feature_cols].apply(
            lambda x: x.shift(1).rolling(window=window, min_periods=1).mean()
        )
        if isinstance(rolled, pd.DataFrame):
            rolled.columns = [f'{c}_avg{window}' for c in feature_cols]
        else:
            # Handle single column case
            rolled = rolled.to_frame()
            rolled.columns = [f'{feature_cols[0]}_avg{window}']
        rolled = rolled.reset_index(level=0, drop=True)
        rolling_dfs.append(rolled)

    result = pd.concat(rolling_dfs, axis=1)
    return result


def select_and_filter_features(df, feature_list):
    """Select features that exist in the dataframe."""
    available = [c for c in feature_list if c in df.columns]
    missing = [c for c in feature_list if c not in df.columns]
    if missing:
        print(f"  Warning: Missing features: {missing}")
    return available


def process_batters():
    """
    Full processing pipeline for batters.

    1. Load FanGraphs batting data
    2. Calculate fantasy points
    3. Select key features
    4. Create lag features (1-year, 2-year)
    5. Create rolling averages (2-year, 3-year)
    6. Merge with Savant supplementary data
    7. Create final training dataset
    """
    ensure_processed_dir()
    print("Processing batters...")

    # Load data
    batting = pd.read_csv(os.path.join(RAW_DATA_DIR, 'fangraphs_batting.csv'))
    print(f"  Loaded {len(batting)} batter-seasons")

    # Calculate fantasy points
    batting = calculate_batter_fpoints(batting)
    print(f"  Fpoints_PA: mean={batting['Fpoints_PA'].mean():.3f}, std={batting['Fpoints_PA'].std():.3f}")

    # Select features
    feature_cols = select_and_filter_features(batting, BATTER_FEATURES)
    print(f"  Using {len(feature_cols)} features")

    # ID columns to keep
    id_cols = ['IDfg', 'Season', 'Name', 'Team', 'Age', 'PA', 'G']
    target_cols = ['Fpoints', 'Fpoints_PA', 'TB', 'R', 'RBI', 'BB', 'SB', 'SO']

    # Create lag features (exclude Age from trend - always increases by 1)
    print("  Creating lag features...")
    lag_df = create_lag_features(
        batting, 'IDfg', 'Season', feature_cols, lags=[1, 2],
        exclude_from_trend=EXCLUDE_FROM_TREND
    )

    # Note: Removed Fpoints rolling averages - they dominated feature importance
    # and made the model less useful for identifying skill-based breakouts/declines

    # Combine (include lag1 level, trend features, and has_trend indicator)
    lag_trend_cols = [c for c in lag_df.columns if '_lag1' in c or '_trend' in c or c == 'has_trend']
    batting_processed = pd.concat([
        batting[id_cols + target_cols + feature_cols],
        lag_df[lag_trend_cols]
    ], axis=1)

    # For training: keep rows with at least 1-year lag data
    lag1_cols = [c for c in batting_processed.columns if '_lag1' in c]
    batting_train = batting_processed.dropna(subset=lag1_cols[:5])  # Check first 5 lag columns
    print(f"  Rows with lag data (for training): {len(batting_train)}")

    # For prediction: keep ALL rows from latest year (including rookies)
    # These players can be used for next-year predictions even without lag data
    latest_year = batting_processed['Season'].max()
    batting_latest = batting_processed[batting_processed['Season'] == latest_year]
    rookies_added = len(batting_latest) - len(batting_train[batting_train['Season'] == latest_year])
    print(f"  {latest_year} players (including {rookies_added} rookies): {len(batting_latest)}")

    # Combine: training data + any latest-year rookies not already included
    batting_train = pd.concat([
        batting_train,
        batting_latest[~batting_latest['IDfg'].isin(batting_train[batting_train['Season'] == latest_year]['IDfg'])]
    ]).sort_values(['IDfg', 'Season']).reset_index(drop=True)

    # Load and merge Savant supplementary data (sweet_spot%, etc.)
    try:
        savant = pd.read_csv(os.path.join(RAW_DATA_DIR, 'savant_batter_expected.csv'))
        # Savant uses MLBAM IDs, need to map via player_id_map
        id_map = pd.read_csv(os.path.join(RAW_DATA_DIR, 'player_id_map.csv'))
        id_map = id_map[['key_mlbam', 'key_fangraphs']].dropna()
        id_map.columns = ['player_id', 'IDfg']
        id_map['IDfg'] = id_map['IDfg'].astype(int)

        savant = savant.merge(id_map, on='player_id', how='left')
        savant = savant.rename(columns={'year': 'Season'})

        # Select unique Savant columns (not in FG data)
        savant_cols = ['sweet_spot_percent', 'ev_max']
        savant_cols = [c for c in savant_cols if c in savant.columns]

        if savant_cols:
            savant_subset = savant[['IDfg', 'Season'] + savant_cols].dropna(subset=['IDfg'])
            batting_train = batting_train.merge(savant_subset, on=['IDfg', 'Season'], how='left')
            print(f"  Merged Savant data: added {savant_cols}")
    except Exception as e:
        print(f"  Warning: Could not merge Savant data: {e}")

    # Save
    path = os.path.join(PROCESSED_DATA_DIR, 'batters_processed.csv')
    batting_train.to_csv(path, index=False)
    print(f"  Saved to {path}")
    print(f"  Final shape: {batting_train.shape}")

    return batting_train


def process_pitchers():
    """
    Full processing pipeline for pitchers.

    Similar to batters but with pitcher-specific features and
    additional pitch arsenal data.
    """
    ensure_processed_dir()
    print("Processing pitchers...")

    # Load data
    pitching = pd.read_csv(os.path.join(RAW_DATA_DIR, 'fangraphs_pitching.csv'))
    print(f"  Loaded {len(pitching)} pitcher-seasons")

    # Calculate fantasy points
    pitching = calculate_pitcher_fpoints(pitching)
    print(f"  Fpoints_IP: mean={pitching['Fpoints_IP'].mean():.3f}, std={pitching['Fpoints_IP'].std():.3f}")

    # Select features
    feature_cols = select_and_filter_features(pitching, PITCHER_FEATURES)
    print(f"  Using {len(feature_cols)} features")

    # ID columns
    id_cols = ['IDfg', 'Season', 'Name', 'Team', 'Age', 'IP', 'G', 'GS']
    target_cols = ['Fpoints_skill', 'Fpoints_IP', 'SO', 'BB', 'H', 'ER', 'W', 'L', 'SV', 'HLD']

    # Create SP/RP indicator (GS > 0 = SP tendency)
    pitching['SP_pct'] = pitching['GS'] / pitching['G']
    feature_cols.append('SP_pct')

    # Create lag features (exclude Age from trend - always increases by 1)
    print("  Creating lag features...")
    lag_df = create_lag_features(
        pitching, 'IDfg', 'Season', feature_cols, lags=[1, 2],
        exclude_from_trend=EXCLUDE_FROM_TREND
    )

    # Note: Removed Fpoints rolling averages - they dominated feature importance
    # and made the model less useful for identifying skill-based breakouts/declines

    # Combine (include lag1 level, trend features, and has_trend indicator)
    lag_trend_cols = [c for c in lag_df.columns if '_lag1' in c or '_trend' in c or c == 'has_trend']
    pitching_processed = pd.concat([
        pitching[id_cols + target_cols + feature_cols],
        lag_df[lag_trend_cols]
    ], axis=1)

    # For training: keep rows with at least 1-year lag data
    lag1_cols = [c for c in pitching_processed.columns if '_lag1' in c]
    pitching_train = pitching_processed.dropna(subset=lag1_cols[:5])
    print(f"  Rows with lag data (for training): {len(pitching_train)}")

    # For prediction: keep ALL rows from latest year (including rookies)
    latest_year = pitching_processed['Season'].max()
    pitching_latest = pitching_processed[pitching_processed['Season'] == latest_year]
    rookies_added = len(pitching_latest) - len(pitching_train[pitching_train['Season'] == latest_year])
    print(f"  {latest_year} players (including {rookies_added} rookies): {len(pitching_latest)}")

    # Combine: training data + any latest-year rookies not already included
    pitching_train = pd.concat([
        pitching_train,
        pitching_latest[~pitching_latest['IDfg'].isin(pitching_train[pitching_train['Season'] == latest_year]['IDfg'])]
    ]).sort_values(['IDfg', 'Season']).reset_index(drop=True)

    # Arsenal features removed - Stuff+ already captures pitch quality holistically
    # (velocity, movement, spin efficiency) without introducing velocity bias
    # See: https://library.fangraphs.com/pitching/stuff-plus/
    #
    # Previously merged: ff_avg_speed, si_avg_speed, sl_avg_speed, ch_avg_speed,
    #                    ff_avg_spin, sl_avg_spin, ch_avg_spin

    # Save
    path = os.path.join(PROCESSED_DATA_DIR, 'pitchers_processed.csv')
    pitching_train.to_csv(path, index=False)
    print(f"  Saved to {path}")
    print(f"  Final shape: {pitching_train.shape}")

    return pitching_train


def process_all():
    """Run full processing for batters and pitchers."""
    print("=" * 60)
    print("MLB Fantasy 2026 - Data Processing")
    print("=" * 60)
    print()

    batters = process_batters()
    print()
    pitchers = process_pitchers()

    print()
    print("=" * 60)
    print("Processing Summary:")
    print("=" * 60)
    print(f"  Batters: {batters.shape[0]} rows, {batters.shape[1]} columns")
    print(f"  Pitchers: {pitchers.shape[0]} rows, {pitchers.shape[1]} columns")
    print(f"  Saved to {PROCESSED_DATA_DIR}/")
    print("=" * 60)

    return batters, pitchers


if __name__ == "__main__":
    process_all()
