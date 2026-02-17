"""
Roster configuration for ESPN fantasy baseball league.
Defines position slots, league size, and replacement level settings.
"""

# League settings
LEAGUE_SIZE = 12  # number of teams in the league

# Roster slots per team
# Maps position -> number of roster slots
ROSTER_SLOTS = {
    "C": 1,
    "1B": 1,
    "2B": 1,
    "3B": 1,
    "SS": 1,
    "OF": 3,
    "DH": 1,  # UTIL slot - can be filled by any hitter
    "P": 3,   # Pitcher slots (no SP/RP distinction)
    "Bench": 3,
}

# Position groups for analysis
HITTER_POSITIONS = ["C", "1B", "2B", "3B", "SS", "OF"]
PITCHER_POSITIONS = ["SP", "RP"]  # For categorization, not roster slots

# Positions that can fill the UTIL slot (all hitters)
UTIL_ELIGIBLE = ["C", "1B", "2B", "3B", "SS", "OF"]

# Outfield position normalization (LF/CF/RF all fill OF slots)
OUTFIELD_POSITIONS = ["LF", "CF", "RF", "OF"]

# Position priority for scarcity (scarcest first)
# DH is NOT included - UTIL slot can be filled by any hitter
# so pure DH players have no positional advantage
POSITION_PRIORITY = ["C", "SS", "2B", "3B", "1B", "OF"]

# Replacement level settings
# How many players around the threshold to average for stable replacement value
REPLACEMENT_COMPOSITE_SIZE = 5  # average 5 players around replacement threshold

# Replacement level team adjustment
# Use (league_size - REPLACEMENT_TEAM_ADJUSTMENT) as effective teams
# Accounts for multi-position eligibility and bench flexibility
REPLACEMENT_TEAM_ADJUSTMENT = 3
