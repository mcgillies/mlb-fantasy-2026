"""
Fantasy scoring rules for ESPN points league.
Update these if your league uses different scoring.
"""

# Batter scoring
BATTER_SCORING = {
    "TB": 1,
    "R": 1,
    "RBI": 1,
    "BB": 1,
    "SB": 1,
    "K": -1,
}

# Pitcher scoring — skill-based component only.
# W/L/Hold/Save are team-dependent and modeled separately
# using external projections at the prediction stage.
PITCHER_SCORING_SKILL = {
    "IP": 3,
    "K": 1,
    "BB": -1,
    "H": -1,
    "ER": -2,
}

# Team-dependent scoring — applied via external projections, not the ML model.
# Uses FanGraphs column names (SV, HLD)
PITCHER_SCORING_TEAM = {
    "W": 2,
    "L": -2,
    "SV": 5,
    "HLD": 2,
}

# Combined (for final total calculation after adding projected W/L/Hold/S)
PITCHER_SCORING_FULL = {**PITCHER_SCORING_SKILL, **PITCHER_SCORING_TEAM}

# Rate stat denominators
BATTER_RATE_DENOM = "PA"   # fantasy points per plate appearance
PITCHER_RATE_DENOM = "IP"  # fantasy points per inning pitched
