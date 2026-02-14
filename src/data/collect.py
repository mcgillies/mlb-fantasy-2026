"""
Data collection using pybaseball.

Pulls historical stats and advanced metrics from FanGraphs and Baseball Savant.

Data sources:
- FanGraphs: batting_stats(), pitching_stats() - comprehensive season stats (~300+ cols)
- Baseball Savant: expected stats, pitch arsenal, pitch movement

Player IDs:
- FanGraphs uses `IDfg`
- Savant uses MLBAM IDs (`player_id`)
- Use chadwick_register() to cross-reference
"""

import os
import pandas as pd
from tqdm import tqdm
from pybaseball import (
    batting_stats,
    pitching_stats,
    statcast_batter_expected_stats,
    statcast_pitcher_expected_stats,
    statcast_pitcher_pitch_arsenal,
    statcast_pitcher_arsenal_stats,
    chadwick_register,
    cache,
)

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import (
    TRAIN_START_YEAR,
    PREDICT_YEAR,
    RAW_DATA_DIR,
    MIN_PA_BATTER,
    MIN_IP_PITCHER,
)

# Enable pybaseball caching to avoid redundant API calls
cache.enable()


def ensure_raw_dir():
    """Create raw data directory if it doesn't exist."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)


def collect_fangraphs_batting(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, qual=MIN_PA_BATTER):
    """
    Collect batting stats from FanGraphs.

    Returns ~318 columns including:
    - Base stats: PA, AB, H, 1B, 2B, 3B, HR, R, RBI, BB, SO, SB, CS
    - Rate stats: AVG, OBP, SLG, wOBA, wRC+
    - Batted ball: GB%, FB%, LD%, Hard%, Pull%
    - Plate discipline: O-Swing%, Z-Contact%, SwStr%
    - Statcast-derived: EV, LA, Barrel%, xBA, xSLG, xwOBA, HardHit%

    Args:
        start_year: First season to collect
        end_year: Last season to collect
        qual: Minimum PA threshold (use 0 for all players)

    Returns:
        DataFrame with all batting stats, one row per player-season
    """
    ensure_raw_dir()
    print(f"Collecting FanGraphs batting stats {start_year}-{end_year} (min PA: {qual})...")

    try:
        df = batting_stats(start_year, end_year, qual=qual, ind=1)
        print(f"  Retrieved {len(df)} player-seasons, {len(df.columns)} columns")

        # Save to CSV
        path = os.path.join(RAW_DATA_DIR, "fangraphs_batting.csv")
        df.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return df
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def collect_fangraphs_pitching(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, qual=MIN_IP_PITCHER):
    """
    Collect pitching stats from FanGraphs.

    Returns ~391 columns including:
    - Base stats: W, L, ERA, G, GS, SV, IP, H, R, ER, HR, BB, SO
    - Rate stats: K/9, BB/9, K/BB, WHIP, FIP, xFIP, SIERA
    - Batted ball: GB%, FB%, HR/FB
    - Plate discipline induced: O-Swing%, SwStr%, K%, BB%
    - Statcast-derived: EV, Barrel%, xBA, xERA, HardHit%
    - Stuff+, Location+, Pitching+ (2020+)

    Args:
        start_year: First season to collect
        end_year: Last season to collect
        qual: Minimum IP threshold

    Returns:
        DataFrame with all pitching stats, one row per player-season
    """
    ensure_raw_dir()
    print(f"Collecting FanGraphs pitching stats {start_year}-{end_year} (min IP: {qual})...")

    try:
        df = pitching_stats(start_year, end_year, qual=qual, ind=1)
        print(f"  Retrieved {len(df)} player-seasons, {len(df.columns)} columns")

        path = os.path.join(RAW_DATA_DIR, "fangraphs_pitching.csv")
        df.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return df
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def collect_statcast_batter_expected(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_pa=MIN_PA_BATTER):
    """
    Collect Statcast expected stats for batters from Baseball Savant.

    Columns include:
    - est_ba (xBA), est_slg (xSLG), est_woba (xwOBA), est_wobacon
    - ev_avg, ev_max, launch_angle_avg, sweet_spot_percent
    - hard_hit_percent, barrel_pa, barrel_batted_ball

    Note: Some of these overlap with FanGraphs data, but Savant may have
    additional columns like sweet_spot_percent and est_wobacon.

    Args:
        start_year: First season
        end_year: Last season
        min_pa: Minimum plate appearances

    Returns:
        DataFrame with expected stats, one row per player-season
    """
    ensure_raw_dir()
    print(f"Collecting Statcast batter expected stats {start_year}-{end_year}...")

    dfs = []
    for year in tqdm(range(start_year, end_year + 1), desc="  Years"):
        try:
            df = statcast_batter_expected_stats(year, minPA=min_pa)
            if df is not None and len(df) > 0:
                df['year'] = year
                dfs.append(df)
        except Exception as e:
            print(f"  WARNING: {year} failed: {e}")
            continue

    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        print(f"  Retrieved {len(result)} player-seasons")

        path = os.path.join(RAW_DATA_DIR, "savant_batter_expected.csv")
        result.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return result
    else:
        print("  ERROR: No data retrieved")
        return None


def collect_statcast_pitcher_expected(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_pa=MIN_IP_PITCHER):
    """
    Collect Statcast expected stats for pitchers (stats allowed against).

    Same structure as batter expected stats but represents quality of contact allowed.
    """
    ensure_raw_dir()
    print(f"Collecting Statcast pitcher expected stats {start_year}-{end_year}...")

    dfs = []
    for year in tqdm(range(start_year, end_year + 1), desc="  Years"):
        try:
            # Note: minPA here refers to PA against the pitcher
            df = statcast_pitcher_expected_stats(year, minPA=min_pa)
            if df is not None and len(df) > 0:
                df['year'] = year
                dfs.append(df)
        except Exception as e:
            print(f"  WARNING: {year} failed: {e}")
            continue

    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        print(f"  Retrieved {len(result)} player-seasons")

        path = os.path.join(RAW_DATA_DIR, "savant_pitcher_expected.csv")
        result.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return result
    else:
        print("  ERROR: No data retrieved")
        return None


def collect_pitcher_arsenal(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_pitches=250):
    """
    Collect pitcher pitch arsenal data: velocity, spin rate, and usage by pitch type.

    Calls statcast_pitcher_pitch_arsenal() three times with different arsenal_type:
    - "avg_speed": Average velocity for each pitch type
    - "avg_spin": Average spin rate for each pitch type
    - "n_": Usage percentage for each pitch type

    Returns merged DataFrame with columns like:
    - ff_avg_speed, ff_avg_spin, ff_n_ (4-seam fastball)
    - sl_avg_speed, sl_avg_spin, sl_n_ (slider)
    - etc. for each pitch type
    """
    ensure_raw_dir()
    print(f"Collecting pitcher pitch arsenal {start_year}-{end_year}...")

    arsenal_types = ["avg_speed", "avg_spin", "n_"]
    all_data = {t: [] for t in arsenal_types}

    for year in tqdm(range(start_year, end_year + 1), desc="  Years"):
        for arsenal_type in arsenal_types:
            try:
                df = statcast_pitcher_pitch_arsenal(year, minP=min_pitches, arsenal_type=arsenal_type)
                if df is not None and len(df) > 0:
                    df['year'] = year
                    all_data[arsenal_type].append(df)
            except Exception as e:
                # Some years or arsenal types may not be available
                continue

    # Concatenate each arsenal type
    results = {}
    for arsenal_type in arsenal_types:
        if all_data[arsenal_type]:
            results[arsenal_type] = pd.concat(all_data[arsenal_type], ignore_index=True)

    if not results:
        print("  ERROR: No arsenal data retrieved")
        return None

    # Merge all three on player_id and year
    # Start with the first available type
    merged = None
    for arsenal_type, df in results.items():
        if merged is None:
            merged = df
        else:
            # Find common ID columns (usually player_id or pitcher)
            id_cols = [c for c in ['player_id', 'pitcher', 'year'] if c in merged.columns and c in df.columns]
            if id_cols:
                # Drop duplicate non-ID columns before merge
                df_cols_to_keep = id_cols + [c for c in df.columns if c not in merged.columns]
                merged = merged.merge(df[df_cols_to_keep], on=id_cols, how='outer')

    print(f"  Retrieved {len(merged)} player-seasons")

    path = os.path.join(RAW_DATA_DIR, "savant_pitcher_arsenal.csv")
    merged.to_csv(path, index=False)
    print(f"  Saved to {path}")

    return merged


def collect_pitcher_arsenal_stats(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR, min_pa=25):
    """
    Collect pitcher arsenal outcome stats: run values, whiff%, BA, SLG by pitch type.

    Returns one row per pitcher per pitch type with:
    - pitch_type, run_value, run_value_per100
    - whiff_percent, put_away
    - ba, slg, woba, hard_hit_percent
    """
    ensure_raw_dir()
    print(f"Collecting pitcher arsenal stats {start_year}-{end_year}...")

    dfs = []
    for year in tqdm(range(start_year, end_year + 1), desc="  Years"):
        try:
            df = statcast_pitcher_arsenal_stats(year, minPA=min_pa)
            if df is not None and len(df) > 0:
                df['year'] = year
                dfs.append(df)
        except Exception as e:
            print(f"  WARNING: {year} failed: {e}")
            continue

    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        print(f"  Retrieved {len(result)} pitcher-pitch_type-seasons")

        path = os.path.join(RAW_DATA_DIR, "savant_pitcher_arsenal_stats.csv")
        result.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return result
    else:
        print("  ERROR: No data retrieved")
        return None


# Note: statcast_pitcher_pitch_movement is not available in pybaseball 2.2.7
# Pitch movement data (horizontal/vertical break) can be extracted from raw
# statcast pitch-level data if needed: use statcast() or statcast_pitcher()
# and aggregate pfx_x, pfx_z columns by pitcher and pitch type.


def collect_id_mapping():
    """
    Collect the Chadwick Bureau player ID register.

    This provides the mapping between:
    - key_fangraphs (IDfg): Used in FanGraphs data
    - key_mlbam (player_id): Used in Statcast/Savant data
    - key_bbref: Used in Baseball Reference data

    Essential for joining FanGraphs and Savant datasets.
    """
    ensure_raw_dir()
    print("Collecting Chadwick player ID register...")

    try:
        df = chadwick_register()

        # Keep only relevant columns
        cols_to_keep = [
            'key_mlbam', 'key_fangraphs', 'key_bbref', 'key_retro',
            'name_first', 'name_last', 'name_given',
            'mlb_played_first', 'mlb_played_last'
        ]
        cols_available = [c for c in cols_to_keep if c in df.columns]
        df = df[cols_available].copy()

        # Drop rows without MLB IDs (we only need MLB players)
        df = df.dropna(subset=['key_mlbam'])

        print(f"  Retrieved {len(df)} players")

        path = os.path.join(RAW_DATA_DIR, "player_id_map.csv")
        df.to_csv(path, index=False)
        print(f"  Saved to {path}")

        return df
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def collect_all(start_year=TRAIN_START_YEAR, end_year=PREDICT_YEAR):
    """
    Run all data collection steps.

    Collects:
    1. FanGraphs batting stats (primary batter data source)
    2. FanGraphs pitching stats (primary pitcher data source)
    3. Statcast batter expected stats (supplementary)
    4. Statcast pitcher expected stats (supplementary)
    5. Pitcher pitch arsenal (velocity, spin, usage)
    6. Pitcher arsenal stats (whiff%, run values by pitch type)
    7. Player ID mapping (for joining FanGraphs + Savant)

    All data saved to data/raw/
    """
    print("=" * 60)
    print(f"MLB Fantasy 2026 - Data Collection")
    print(f"Years: {start_year} - {end_year}")
    print("=" * 60)
    print()

    results = {}

    # 1. FanGraphs batting (primary - includes Statcast-derived metrics)
    results['fg_batting'] = collect_fangraphs_batting(start_year, end_year)
    print()

    # 2. FanGraphs pitching (primary)
    results['fg_pitching'] = collect_fangraphs_pitching(start_year, end_year)
    print()

    # 3. Statcast batter expected (supplementary - sweet_spot%, wobacon)
    results['savant_batter'] = collect_statcast_batter_expected(start_year, end_year)
    print()

    # 4. Statcast pitcher expected (supplementary)
    results['savant_pitcher'] = collect_statcast_pitcher_expected(start_year, end_year)
    print()

    # 5. Pitcher arsenal (velocity, spin, usage by pitch type)
    results['arsenal'] = collect_pitcher_arsenal(start_year, end_year)
    print()

    # 6. Pitcher arsenal stats (whiff%, run values by pitch type)
    results['arsenal_stats'] = collect_pitcher_arsenal_stats(start_year, end_year)
    print()

    # 7. Player ID mapping
    results['id_map'] = collect_id_mapping()
    print()

    # Summary
    print("=" * 60)
    print("Collection Summary:")
    print("=" * 60)
    for name, df in results.items():
        if df is not None:
            print(f"  {name}: {len(df)} rows, {len(df.columns)} cols")
        else:
            print(f"  {name}: FAILED")

    print()
    print(f"All data saved to {RAW_DATA_DIR}/")
    print("=" * 60)

    return results


if __name__ == "__main__":
    collect_all()
