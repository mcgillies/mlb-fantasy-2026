"""
Positional adjustments using Points Above Replacement (PAR).

Calculates replacement level for each position based on league roster settings,
then computes PAR = Projected Points - Replacement Level Points.

This surfaces positional scarcity (e.g., elite catchers have high PAR even with
moderate raw points, while replacement-level 1B have low/negative PAR).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

# Import roster config
import sys
sys.path.insert(0, '.')
from config.roster import (
    LEAGUE_SIZE,
    ROSTER_SLOTS,
    POSITION_PRIORITY,
    REPLACEMENT_COMPOSITE_SIZE,
    REPLACEMENT_TEAM_ADJUSTMENT,
    OUTFIELD_POSITIONS,
)


def normalize_position(pos: str) -> str:
    """
    Normalize a single position string.

    - LF/CF/RF -> OF (all fill OF slots)
    - DH stays as DH (will be handled specially for UTIL)
    """
    pos = pos.strip().upper()
    if pos in OUTFIELD_POSITIONS:
        return "OF"
    return pos


def normalize_position_string(position_str: str) -> str:
    """
    Normalize a full position string (may contain multiple positions).

    E.g., "LF/DH" -> "OF/DH", "CF" -> "OF", "RF/CF" -> "OF"

    Args:
        position_str: Position string like "LF/DH", "CF", "2B/SS"

    Returns:
        Normalized position string with OF instead of LF/CF/RF
    """
    if pd.isna(position_str) or position_str == "":
        return ""

    positions = [normalize_position(p) for p in str(position_str).split("/")]
    # Remove duplicates while preserving order
    seen = set()
    unique_positions = []
    for p in positions:
        if p not in seen:
            seen.add(p)
            unique_positions.append(p)

    return "/".join(unique_positions)


def get_primary_position(position_str: str) -> str:
    """
    Extract primary position from multi-position string.

    Uses POSITION_PRIORITY to select the scarcest position.
    E.g., "2B/SS" -> "SS" (SS is scarcer), "LF/DH" -> "OF"

    Normalizes outfield positions (LF/CF/RF -> OF) first.

    Args:
        position_str: Position string like "2B/SS", "LF", "SP"

    Returns:
        Primary position string
    """
    if pd.isna(position_str) or position_str == "" or position_str == "Unknown":
        return "UTIL"  # No position = no positional advantage

    # Normalize positions (LF/CF/RF -> OF)
    normalized = normalize_position_string(position_str)
    positions = [p.strip() for p in normalized.split("/")]

    # Return highest priority (scarcest) position
    for priority_pos in POSITION_PRIORITY:
        if priority_pos in positions:
            return priority_pos

    # Handle pitchers
    if "SP" in positions:
        return "SP"
    if "RP" in positions:
        return "RP"

    # DH-only or unknown players get "UTIL" designation
    # They compete with the deepest pool for the UTIL slot
    if "DH" in positions:
        return "UTIL"

    # Fallback - treat as UTIL (no positional advantage)
    return "UTIL"


def get_all_positions(position_str: str) -> List[str]:
    """
    Get all eligible positions from a position string.

    Normalizes outfield positions (LF/CF/RF -> OF).
    Returns empty list for unknown/missing positions.

    Args:
        position_str: Position string like "2B/SS", "LF/DH"

    Returns:
        List of normalized position strings (no duplicates)
    """
    if pd.isna(position_str) or position_str == "" or position_str == "Unknown":
        return []

    # Normalize and deduplicate
    normalized = normalize_position_string(position_str)
    positions = [p.strip() for p in normalized.split("/") if p.strip()]

    # Filter out "Unknown" if it somehow got through
    return [p for p in positions if p != "Unknown"]


def calculate_replacement_levels(
    df: pd.DataFrame,
    points_col: str = "Projected_Points",
    position_col: str = "Primary_Position",
    league_size: int = LEAGUE_SIZE,
    roster_slots: Dict[str, int] = ROSTER_SLOTS,
    composite_size: int = REPLACEMENT_COMPOSITE_SIZE,
    team_adjustment: int = REPLACEMENT_TEAM_ADJUSTMENT,
) -> Dict[str, float]:
    """
    Calculate replacement level points for each position.

    Replacement level = average of players around the replacement threshold.
    Uses (league_size - team_adjustment) as effective teams to account for
    multi-position eligibility and bench flexibility.

    Args:
        df: DataFrame with projected points and position
        points_col: Column name for projected points
        position_col: Column name for position
        league_size: Number of teams in league
        roster_slots: Dict mapping position -> slots per team
        composite_size: Number of players to average around threshold
        team_adjustment: Reduce effective teams by this amount (default 3)

    Returns:
        Dict mapping position -> replacement level points
    """
    replacement_levels = {}
    effective_teams = league_size - team_adjustment

    for position in POSITION_PRIORITY:
        # Get players at this position
        pos_players = df[df[position_col] == position].copy()

        if len(pos_players) == 0:
            replacement_levels[position] = 0.0
            continue

        # Sort by projected points descending
        pos_players = pos_players.sort_values(points_col, ascending=False).reset_index(drop=True)

        # Calculate total starters drafted at this position
        # Use effective_teams to account for multi-position eligibility
        slots = roster_slots.get(position, 1)
        total_starters = effective_teams * slots

        # Replacement level is just after starters
        replacement_idx = total_starters

        # Composite: average players around the threshold
        start_idx = max(0, replacement_idx - composite_size // 2)
        end_idx = min(len(pos_players), replacement_idx + composite_size // 2 + 1)

        if start_idx < len(pos_players):
            composite_players = pos_players.iloc[start_idx:end_idx]
            replacement_levels[position] = composite_players[points_col].mean()
        else:
            # Not enough players, use last available
            replacement_levels[position] = pos_players[points_col].iloc[-1] if len(pos_players) > 0 else 0.0

    # UTIL replacement = highest replacement level (deepest/most competitive pool)
    # Since UTIL can be filled by any hitter, pure DH competes with overflow
    # from the deepest position pools (1B, OF typically)
    non_zero_levels = [v for v in replacement_levels.values() if v > 0]
    if non_zero_levels:
        replacement_levels["UTIL"] = max(non_zero_levels)
    else:
        replacement_levels["UTIL"] = 0.0

    return replacement_levels


def calculate_pitcher_replacement_levels(
    df: pd.DataFrame,
    points_col: str = "Projected_Points",
    type_col: str = "Type",
    league_size: int = LEAGUE_SIZE,
    rp_per_team: float = 1.5,
    composite_size: int = REPLACEMENT_COMPOSITE_SIZE,
) -> Dict[str, float]:
    """
    Calculate replacement levels for SP and RP.

    SP uses the combined pitcher pool (all pitchers compete together),
    while RP uses a separate smaller pool to capture scarcity value.

    Roster construction assumptions:
    - 8 P slots + 2-3 bench pitchers = 10-11 pitchers per team
    - 12 GS/week cap means teams need 1-2 RP
    - RP are scarce but have lower raw points

    Args:
        df: DataFrame with pitcher projections (must have Type column)
        points_col: Column for projected points
        type_col: Column indicating SP or RP
        league_size: Number of teams
        rp_per_team: Average RP rostered per team (default 1.5)
        composite_size: Players to average for replacement level

    Returns:
        Dict with 'SP' and 'RP' replacement levels
    """
    replacement_levels = {}

    # SP: Use combined pitcher pool (old approach)
    # This keeps SP PAR at the original levels
    all_pitchers = df.sort_values(points_col, ascending=False).reset_index(drop=True)
    pitcher_slots = 3  # Base P slots per team
    total_pitchers = league_size * pitcher_slots + league_size  # + bench

    replacement_idx = total_pitchers
    start_idx = max(0, replacement_idx - composite_size // 2)
    end_idx = min(len(all_pitchers), replacement_idx + composite_size // 2 + 1)

    if start_idx < len(all_pitchers):
        replacement_levels["SP"] = all_pitchers.iloc[start_idx:end_idx][points_col].mean()
    elif len(all_pitchers) > 0:
        replacement_levels["SP"] = all_pitchers[points_col].iloc[-1]
    else:
        replacement_levels["SP"] = 0.0

    # RP: Use separate RP-only pool for scarcity boost
    rp_df = df[df[type_col] == "RP"].copy()

    if len(rp_df) == 0:
        replacement_levels["RP"] = replacement_levels["SP"]  # Fallback
    else:
        rp_df = rp_df.sort_values(points_col, ascending=False).reset_index(drop=True)
        total_rp = int(league_size * rp_per_team)

        replacement_idx = total_rp
        start_idx = max(0, replacement_idx - composite_size // 2)
        end_idx = min(len(rp_df), replacement_idx + composite_size // 2 + 1)

        if start_idx < len(rp_df):
            replacement_levels["RP"] = rp_df.iloc[start_idx:end_idx][points_col].mean()
        elif len(rp_df) > 0:
            replacement_levels["RP"] = rp_df[points_col].iloc[-1]
        else:
            replacement_levels["RP"] = replacement_levels["SP"]

    return replacement_levels


def calculate_pitcher_replacement_level(
    df: pd.DataFrame,
    points_col: str = "Projected_Points",
    league_size: int = LEAGUE_SIZE,
    pitcher_slots: int = 3,
    composite_size: int = REPLACEMENT_COMPOSITE_SIZE,
) -> float:
    """
    DEPRECATED: Use calculate_pitcher_replacement_levels() for separate SP/RP levels.

    Calculate replacement level for pitchers (single pool).
    Kept for backwards compatibility.
    """
    pitchers = df.sort_values(points_col, ascending=False).reset_index(drop=True)

    total_starters = league_size * pitcher_slots
    total_starters += league_size

    replacement_idx = total_starters

    start_idx = max(0, replacement_idx - composite_size // 2)
    end_idx = min(len(pitchers), replacement_idx + composite_size // 2 + 1)

    if start_idx < len(pitchers):
        return pitchers.iloc[start_idx:end_idx][points_col].mean()
    elif len(pitchers) > 0:
        return pitchers[points_col].iloc[-1]
    else:
        return 0.0


def calculate_par(
    df: pd.DataFrame,
    replacement_levels: Dict[str, float],
    points_col: str = "Projected_Points",
    position_col: str = "Primary_Position",
) -> pd.Series:
    """
    Calculate Points Above Replacement for each player.

    PAR = Projected Points - Replacement Level Points (for their position)

    Args:
        df: DataFrame with projections
        replacement_levels: Dict from calculate_replacement_levels
        points_col: Column for projected points
        position_col: Column for position

    Returns:
        Series of PAR values aligned with df index
    """
    def get_par(row):
        position = row[position_col]
        points = row[points_col]
        repl = replacement_levels.get(position, 0)
        return points - repl

    return df.apply(get_par, axis=1)


def calculate_par_best_position(
    df: pd.DataFrame,
    replacement_levels: Dict[str, float],
    points_col: str = "Projected_Points",
    position_col: str = "Position",  # Full position string with multi-eligibility
) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate PAR using each player's best eligible position.

    For multi-position players (e.g., "2B/SS"), calculates PAR at each
    position and returns the maximum (scarcest position = highest PAR).

    DH-only players use UTIL replacement level since they compete with
    all leftover hitters for the UTIL slot.

    Args:
        df: DataFrame with projections
        replacement_levels: Dict from calculate_replacement_levels
        points_col: Column for projected points
        position_col: Column for position string (can be multi-position)

    Returns:
        Tuple of (PAR Series, Best Position Series)
    """
    def get_best_par(row):
        positions = get_all_positions(row[position_col])
        points = row[points_col]

        # No positions = UTIL (no positional advantage)
        if not positions:
            util_repl = replacement_levels.get("UTIL", 0)
            return points - util_repl, "UTIL"

        best_par = float('-inf')
        best_pos = positions[0]

        for pos in positions:
            # Skip DH - it's not a real position, UTIL is filled by leftovers
            if pos == "DH":
                continue
            repl = replacement_levels.get(pos, 0)
            par = points - repl
            if par > best_par:
                best_par = par
                best_pos = pos

        # If only DH eligible (pure DH), use UTIL replacement level
        # UTIL replacement = worst among all positions (deepest pool)
        if best_par == float('-inf') and "DH" in positions:
            util_repl = replacement_levels.get("UTIL", 0)
            best_par = points - util_repl
            best_pos = "UTIL"

        return best_par if best_par != float('-inf') else 0, best_pos

    results = df.apply(get_best_par, axis=1)
    par_values = results.apply(lambda x: x[0])
    best_positions = results.apply(lambda x: x[1])

    return par_values, best_positions


def add_positional_adjustments(
    df: pd.DataFrame,
    points_col: str = "Projected_Points",
    position_col: str = "Position",
    league_size: int = LEAGUE_SIZE,
) -> pd.DataFrame:
    """
    Add positional adjustment columns to a DataFrame.

    Adds:
    - Primary_Position: Scarcest eligible position
    - Replacement_Level: Points at replacement level for position
    - PAR: Points Above Replacement
    - PAR_Rank: Rank by PAR (higher = better)

    Args:
        df: DataFrame with projections (must have points_col and position_col)
        points_col: Column name for projected points
        position_col: Column name for position
        league_size: Number of teams in league

    Returns:
        DataFrame with added columns
    """
    result = df.copy()

    # Extract primary position
    result["Primary_Position"] = result[position_col].apply(get_primary_position)

    # Calculate replacement levels
    replacement_levels = calculate_replacement_levels(
        result,
        points_col=points_col,
        position_col="Primary_Position",
        league_size=league_size,
    )

    # Add replacement level column
    result["Replacement_Level"] = result["Primary_Position"].map(replacement_levels)

    # Calculate PAR using best position
    par_values, best_positions = calculate_par_best_position(
        result,
        replacement_levels,
        points_col=points_col,
        position_col=position_col,
    )

    result["PAR"] = par_values
    result["PAR_Position"] = best_positions

    # Rank by PAR
    result["PAR_Rank"] = result["PAR"].rank(ascending=False, method="min").astype(int)

    return result


def add_pitcher_adjustments(
    df: pd.DataFrame,
    points_col: str = "Projected_Points",
    type_col: str = "Type",
    league_size: int = LEAGUE_SIZE,
    rp_per_team: float = 1.5,
) -> pd.DataFrame:
    """
    Add positional adjustment columns for pitchers.

    SP uses the combined pitcher pool for replacement (keeps original PAR).
    RP uses a separate smaller pool to capture scarcity value (~1.5 per team).

    Args:
        df: DataFrame with pitcher projections (must have Type column)
        points_col: Column name for projected points
        type_col: Column indicating SP or RP
        league_size: Number of teams in league
        rp_per_team: Average RP rostered per team (for scarcity calc)

    Returns:
        DataFrame with added columns (Replacement_Level, PAR, PAR_Rank)
    """
    result = df.copy()

    # Calculate replacement levels (SP=combined pool, RP=separate pool)
    replacement_levels = calculate_pitcher_replacement_levels(
        result,
        points_col=points_col,
        type_col=type_col,
        league_size=league_size,
        rp_per_team=rp_per_team,
    )

    # Map replacement level based on pitcher type
    result["Replacement_Level"] = result[type_col].map(replacement_levels)

    # Calculate PAR
    result["PAR"] = result[points_col] - result["Replacement_Level"]

    # Rank all pitchers together by PAR
    result["PAR_Rank"] = result["PAR"].rank(ascending=False, method="min").astype(int)

    return result


def print_pitcher_replacement_summary(
    replacement_levels: Dict[str, float],
    title: str = "Pitcher Replacement Levels",
) -> None:
    """Print formatted pitcher replacement level summary."""
    print(f"\n{title}")
    print("=" * 40)
    for ptype in ["SP", "RP"]:
        if ptype in replacement_levels:
            print(f"  {ptype}: {replacement_levels[ptype]:7.1f} points")
    print()


def print_replacement_summary(
    replacement_levels: Dict[str, float],
    title: str = "Replacement Level Summary",
) -> None:
    """Print formatted replacement level summary."""
    print(f"\n{title}")
    print("=" * 40)
    for pos in POSITION_PRIORITY:
        if pos in replacement_levels:
            print(f"  {pos:4s}: {replacement_levels[pos]:7.1f} points")
    # Also print UTIL if present
    if "UTIL" in replacement_levels:
        print(f"  UTIL: {replacement_levels['UTIL']:7.1f} points (=deepest position)")
    print()
