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

BATTER_FEATURES = [
    # Expected stats (Statcast) - what contact quality SHOULD produce
    'xBA', 'xSLG', 'xwOBA',
    # Batted ball quality - raw skill indicators
    'EV', 'maxEV', 'Barrel%', 'HardHit%', 'Hard%',
    # Plate discipline - approach and contact skills
    'K%', 'BB%', 'BB/K', 'SwStr%', 'Contact%', 'O-Contact%', 'Z-Contact%',
    'O-Swing%', 'Z-Swing%', 'Zone%',
    # Batted ball distribution - batted ball tendencies
    'GB%', 'FB%', 'LD%', 'HR/FB', 'Pull%',
    # Speed
    'Spd',
    # Age
    'Age',
]

PITCHER_FEATURES = [
    # Strikeout/walk skills - core pitching skills
    'K%', 'K/9', 'K-BB%', 'K/BB', 'BB%', 'BB/9',
    # Whiff/contact - pitch quality indicators
    'SwStr%', 'Contact%', 'Z-Contact%', 'O-Contact%', 'O-Swing%',
    # Expected/estimator stats - skill-based run prevention estimators
    'xERA', 'xFIP', 'SIERA', 'FIP',
    # Batted ball quality allowed - contact quality against
    'EV', 'Barrel%', 'HardHit%',
    # Batted ball distribution - batted ball tendencies allowed
    'GB%', 'FB%', 'LD%', 'HR/FB',
    # Rate stats (descriptive, not outcome-based)
    'H/9', 'HR/9',
    # Pitch velocity by type (using pitch info format where available)
    'FBv',        # Fastball (old format)
    'vSI (pi)',   # Sinker
    'vFC (pi)',   # Cutter
    'SLv',        # Slider (old format)
    'CHv',        # Changeup (old format)
    'vCU (pi)',   # Curveball
    'vFS (pi)',   # Splitter
    # Pitch usage
    'FA% (pi)',   # Fastball
    'SI% (pi)',   # Sinker
    'FC% (pi)',   # Cutter
    'SL%',        # Slider (old format)
    'CH%',        # Changeup (old format)
    'CU% (pi)',   # Curveball
    'FS% (pi)',   # Splitter
    # Pitch movement (horizontal X, vertical Z) - all main pitch types
    'FA-X (pi)', 'FA-Z (pi)',  # Fastball
    'SI-X (pi)', 'SI-Z (pi)',  # Sinker
    'FC-X (pi)', 'FC-Z (pi)',  # Cutter
    'SL-X (pi)', 'SL-Z (pi)',  # Slider
    'CH-X (pi)', 'CH-Z (pi)',  # Changeup
    'CU-X (pi)', 'CU-Z (pi)',  # Curveball
    'FS-X (pi)', 'FS-Z (pi)',  # Splitter
    # Stuff+ metrics (pitch quality grades)
    'Stuff+', 'Pitching+',
    # Age
    'Age',
]


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


def create_lag_features(df, id_col, year_col, feature_cols, lags=[1, 2]):
    """
    Create lagged features (previous 1-2 seasons).

    Year N-1 metrics are used to predict year N fantasy points.
    """
    df = df.sort_values([id_col, year_col]).copy()

    lagged_dfs = [df]

    for lag in lags:
        lagged = df.groupby(id_col)[feature_cols].shift(lag)
        lagged.columns = [f'{c}_lag{lag}' for c in feature_cols]
        lagged_dfs.append(lagged)

    result = pd.concat(lagged_dfs, axis=1)
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

    # Create lag features
    print("  Creating lag features...")
    lag_df = create_lag_features(batting, 'IDfg', 'Season', feature_cols, lags=[1, 2])

    # Create rolling averages for Fpoints_PA
    print("  Creating rolling averages...")
    rolling_df = create_rolling_features(batting, 'IDfg', 'Season', ['Fpoints_PA'], windows=[2, 3])

    # Combine
    batting_processed = pd.concat([
        batting[id_cols + target_cols + feature_cols],
        lag_df[[c for c in lag_df.columns if '_lag' in c]],
        rolling_df
    ], axis=1)

    # Only keep rows with at least 1-year lag data (for training)
    lag1_cols = [c for c in batting_processed.columns if '_lag1' in c]
    batting_train = batting_processed.dropna(subset=lag1_cols[:5])  # Check first 5 lag columns
    print(f"  Rows with lag data: {len(batting_train)}")

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

    # Create lag features
    print("  Creating lag features...")
    lag_df = create_lag_features(pitching, 'IDfg', 'Season', feature_cols, lags=[1, 2])

    # Rolling averages for Fpoints_IP
    print("  Creating rolling averages...")
    rolling_df = create_rolling_features(pitching, 'IDfg', 'Season', ['Fpoints_IP'], windows=[2, 3])

    # Combine
    pitching_processed = pd.concat([
        pitching[id_cols + target_cols + feature_cols],
        lag_df[[c for c in lag_df.columns if '_lag' in c]],
        rolling_df
    ], axis=1)

    # Keep rows with lag data
    lag1_cols = [c for c in pitching_processed.columns if '_lag1' in c]
    pitching_train = pitching_processed.dropna(subset=lag1_cols[:5])
    print(f"  Rows with lag data: {len(pitching_train)}")

    # Merge pitch arsenal data
    try:
        arsenal = pd.read_csv(os.path.join(RAW_DATA_DIR, 'savant_pitcher_arsenal.csv'))
        id_map = pd.read_csv(os.path.join(RAW_DATA_DIR, 'player_id_map.csv'))
        id_map = id_map[['key_mlbam', 'key_fangraphs']].dropna()
        id_map.columns = ['pitcher', 'IDfg']  # Arsenal uses 'pitcher' column for MLBAM ID
        id_map['IDfg'] = id_map['IDfg'].astype(int)

        arsenal = arsenal.merge(id_map, on='pitcher', how='left')
        arsenal = arsenal.rename(columns={'year': 'Season'})

        # Key arsenal features: fastball velo and primary pitch velocities/spin
        arsenal_cols = ['ff_avg_speed', 'si_avg_speed', 'sl_avg_speed', 'ch_avg_speed',
                       'ff_avg_spin', 'sl_avg_spin', 'ch_avg_spin']
        arsenal_cols = [c for c in arsenal_cols if c in arsenal.columns]

        if arsenal_cols:
            arsenal_subset = arsenal[['IDfg', 'Season'] + arsenal_cols].dropna(subset=['IDfg'])
            pitching_train = pitching_train.merge(arsenal_subset, on=['IDfg', 'Season'], how='left')
            print(f"  Merged arsenal data: added {len(arsenal_cols)} columns")
    except Exception as e:
        print(f"  Warning: Could not merge arsenal data: {e}")

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
