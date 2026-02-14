# pybaseball Library Reference

> Comprehensive reference for the `pybaseball` Python package.
> Repository: https://github.com/jldbc/pybaseball
> PyPI: https://pypi.org/project/pybaseball/

---

## Table of Contents

1. [FanGraphs Season-Level Stats](#1-fangraphs-season-level-stats)
2. [Statcast Expected Stats](#2-statcast-expected-stats)
3. [Pitch-Level and Pitch-Type Data](#3-pitch-level-and-pitch-type-data)
4. [Baseball Savant Leaderboard Data](#4-baseball-savant-leaderboard-data)
5. [Caching System](#5-caching-system)
6. [Player ID Systems and Cross-Referencing](#6-player-id-systems-and-cross-referencing)
7. [Split Stats](#7-split-stats)
8. [Additional Useful Functions](#8-additional-useful-functions)
9. [Complete Function Index](#9-complete-function-index)

---

## 1. FanGraphs Season-Level Stats

### `batting_stats()`

Pulls season-level batting data from FanGraphs. Returns ~318 columns per player per season.

```python
from pybaseball import batting_stats

batting_stats(
    start_season: int,          # Required. First season (e.g. 2023)
    end_season: int = None,     # Optional. Last season. Omit for single season.
    league: str = 'all',        # 'all', 'al', 'nl', 'mnl' (Negro League)
    qual: int = 1,              # Min plate appearances. Use qual=0 for no minimum.
    ind: int = 1                # 1 = one row per player-season; 0 = aggregate across seasons
) -> pd.DataFrame
```

**Usage Examples:**
```python
# All qualified batters in 2024
data = batting_stats(2024)

# All batters with 100+ PA in 2024
data = batting_stats(2024, qual=100)

# Individual seasons 2020-2024
data = batting_stats(2020, 2024, ind=1)

# Aggregate 2020-2024
data = batting_stats(2020, 2024, ind=0)
```

**Key Columns Returned (subset of ~318 total):**

| Column | Description |
|--------|-------------|
| `IDfg` | FanGraphs player ID (use for joins) |
| `Name` | Player name |
| `Team` | Team abbreviation |
| `Season` | Year |
| `Age` | Player age |
| `G` | Games played |
| `AB` | At bats |
| `PA` | Plate appearances |
| `H` | Hits |
| `1B` | Singles |
| `2B` | Doubles |
| `3B` | Triples |
| `HR` | Home runs |
| `R` | Runs scored |
| `RBI` | Runs batted in |
| `BB` | Walks |
| `IBB` | Intentional walks |
| `SO` | Strikeouts |
| `HBP` | Hit by pitch |
| `SF` | Sacrifice flies |
| `SH` | Sacrifice hits |
| `GDP` | Grounded into double play |
| `SB` | Stolen bases |
| `CS` | Caught stealing |
| `AVG` | Batting average |
| `OBP` | On-base percentage |
| `SLG` | Slugging percentage |
| `OPS` | OBP + SLG |
| `ISO` | Isolated power |
| `BABIP` | Batting avg on balls in play |
| `wOBA` | Weighted on-base average |
| `wRC+` | Weighted runs created plus (league-adjusted) |
| `WAR` | Wins above replacement |
| `BB%` | Walk rate |
| `K%` | Strikeout rate |
| `BB/K` | Walk-to-strikeout ratio |
| `GB%` | Ground ball rate |
| `FB%` | Fly ball rate |
| `LD%` | Line drive rate |
| `HR/FB` | Home run per fly ball rate |
| `Pull%` | Pull rate |
| `Cent%` | Center rate |
| `Oppo%` | Opposite field rate |
| `Soft%` | Soft contact rate |
| `Med%` | Medium contact rate |
| `Hard%` | Hard contact rate |
| `O-Swing%` | Outside zone swing rate |
| `Z-Swing%` | Zone swing rate |
| `Swing%` | Overall swing rate |
| `O-Contact%` | Outside zone contact rate |
| `Z-Contact%` | Zone contact rate |
| `Contact%` | Overall contact rate |
| `SwStr%` | Swinging strike rate |
| `WPA` | Win probability added |
| `RE24` | Run expectancy based on 24 base-out states |
| `SPD` | Speed score |
| `BSR` | Base running runs |
| `EV` | Exit velocity |
| `LA` | Launch angle |
| `Barrels` | Barrel count |
| `Barrel%` | Barrel rate |
| `maxEV` | Max exit velocity |
| `HardHit` | Hard hit count |
| `HardHit%` | Hard hit rate |
| `xBA` | Expected batting average |
| `xSLG` | Expected slugging |
| `xwOBA` | Expected wOBA |

Plus pitch-type breakdowns (velocity, value, etc. for FB, SL, CT, CB, CH, SF, KN), plus-stats (AVG+, BB%+, K%+, OBP+, SLG+, ISO+, BABIP+, etc.), and WAR components.

---

### `pitching_stats()`

Pulls season-level pitching data from FanGraphs. Returns ~391 columns per player per season.

```python
from pybaseball import pitching_stats

pitching_stats(
    start_season: int,          # Required. First season (e.g. 2023)
    end_season: int = None,     # Optional. Last season.
    league: str = 'all',        # 'all', 'al', 'nl'
    qual: int = 1,              # Min PA against (qual=0 for no minimum)
    ind: int = 1                # 1 = per-season rows; 0 = aggregate
) -> pd.DataFrame
```

**Key Columns Returned (subset of ~391 total):**

| Column | Description |
|--------|-------------|
| `IDfg` | FanGraphs player ID |
| `Name` | Player name |
| `Team` | Team abbreviation |
| `Season` | Year |
| `Age` | Player age |
| `W` | Wins |
| `L` | Losses |
| `ERA` | Earned run average |
| `G` | Games |
| `GS` | Games started |
| `SV` | Saves |
| `BS` | Blown saves |
| `IP` | Innings pitched |
| `TBF` | Total batters faced |
| `H` | Hits allowed |
| `R` | Runs allowed |
| `ER` | Earned runs |
| `HR` | Home runs allowed |
| `BB` | Walks |
| `IBB` | Intentional walks |
| `HBP` | Hit by pitch |
| `SO` | Strikeouts |
| `K/9` | Strikeouts per 9 innings |
| `BB/9` | Walks per 9 innings |
| `K/BB` | Strikeout-to-walk ratio |
| `H/9` | Hits per 9 innings |
| `HR/9` | Home runs per 9 innings |
| `AVG` | Batting average against |
| `WHIP` | Walks + hits per inning pitched |
| `BABIP` | BABIP against |
| `LOB%` | Left on base percentage |
| `FIP` | Fielding independent pitching |
| `xFIP` | Expected FIP (normalizes HR/FB) |
| `SIERA` | Skill-interactive ERA |
| `WAR` | Wins above replacement |
| `GB%` | Ground ball rate |
| `FB%` | Fly ball rate |
| `LD%` | Line drive rate |
| `HR/FB` | Home run per fly ball |
| `O-Swing%` | Outside zone swing rate induced |
| `Z-Swing%` | Zone swing rate induced |
| `SwStr%` | Swinging strike rate induced |
| `K%` | Strikeout rate |
| `BB%` | Walk rate |
| `K-BB%` | K minus BB rate |
| `EV` | Exit velocity against |
| `LA` | Launch angle against |
| `Barrels` | Barrels against |
| `Barrel%` | Barrel rate against |
| `HardHit%` | Hard hit rate against |
| `xBA` | Expected BA against |
| `xSLG` | Expected SLG against |
| `xwOBA` | Expected wOBA against |
| `xERA` | Expected ERA |
| `Stuff+` | Stuff plus (pitch quality model) |
| `Location+` | Location plus (command model) |
| `Pitching+` | Pitching plus (combined) |

Plus pitch-type breakdowns, WPA, RE24, and many more.

---

### Advanced FanGraphs Parameters (via `fg_batting_data` / `fg_pitching_data`)

The underlying FanGraphs fetch method supports additional parameters not exposed in the simplified `batting_stats`/`pitching_stats` wrappers:

```python
from pybaseball.datasources.fangraphs import fg_batting_data, fg_pitching_data

# Full parameter list for the underlying fetch method:
fg_batting_data.fetch(
    start_season=2024,
    end_season=None,
    league='ALL',               # ALL, AL, FL, NL
    ind=1,                      # 1=individual seasons, 0=aggregate
    stat_columns='ALL',         # 'ALL' or list of stat names from FangraphsBattingStats enum
    qual=None,                  # Min PA threshold
    split_seasons=True,
    month='ALL',                # Time filter (see month values below)
    on_active_roster=False,
    minimum_age=0,
    maximum_age=100,
    team='',                    # Team filter; '0,ts' for team-level aggregates
    _filter='',
    players='',
    position='ALL',             # 'all','p','c','1b','2b','3b','ss','lf','cf','rf','of','dh','np'
    max_results=1000000
)
```

**FangraphsMonth Enum Values:**

| Value | Meaning |
|-------|---------|
| `'ALL'` (0) | Full season (default) |
| `'MARCH_APRIL'` / `'MARCH'` / `'APRIL'` (4) | March/April |
| `'MAY'` (5) | May |
| `'JUNE'` (6) | June |
| `'JULY'` (7) | July |
| `'AUGUST'` (8) | August |
| `'SEPTEMBER_OCTOBER'` / `'SEPTEMBER'` / `'OCTOBER'` (9) | September/October |

**Important:** The pybaseball `FangraphsMonth` enum does NOT include first-half/second-half values. FanGraphs' underlying API does support `month=30` (1st Half) and `month=31` (2nd Half), but these are not mapped in pybaseball's enum. To get half-season splits from FanGraphs via pybaseball, you would need to either (a) use `get_splits()` from Baseball Reference, or (b) pass the raw month integer directly by bypassing the enum.

---

### `batting_stats_bref()` / `pitching_stats_bref()`

Alternative functions pulling from Baseball Reference instead of FanGraphs.

```python
from pybaseball import batting_stats_bref, pitching_stats_bref

# Single season from Baseball Reference
batting_stats_bref(season=2024) -> pd.DataFrame
pitching_stats_bref(season=2024) -> pd.DataFrame
```

### `batting_stats_range()` / `pitching_stats_range()`

Pull stats for a custom date range from Baseball Reference.

```python
from pybaseball import batting_stats_range, pitching_stats_range

# Custom date range (YYYY-MM-DD format)
batting_stats_range('2024-07-15', '2024-10-01')
pitching_stats_range('2024-07-15', '2024-10-01')
```

**Important for second-half stats:** These date-range functions are the most direct way to get post-All-Star-Break stats. Use the ASB date as start_dt and the end of the regular season as end_dt.

---

## 2. Statcast Expected Stats

### `statcast_batter_expected_stats()`

Pulls expected statistics from Baseball Savant's expected statistics leaderboard.

```python
from pybaseball import statcast_batter_expected_stats

statcast_batter_expected_stats(
    year: int,                          # Season year (YYYY)
    minPA: Union[int, str] = "q"        # Min PA; "q" = qualified only, or int
) -> pd.DataFrame
```

**Source URL:** `https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=batter&year={year}&position=&team=&filterType=pa&min={minPA}&csv=true`

**Columns Returned:**

| Column | Description |
|--------|-------------|
| `last_name, first_name` | Player name (may vary by year) |
| `player_id` | MLBAM player ID |
| `year` | Season |
| `pa` | Plate appearances |
| `bip` | Balls in play |
| `ba` | Actual batting average |
| `est_ba` | Expected batting average (xBA) |
| `est_ba_minus_ba_diff` | xBA - BA difference |
| `slg` | Actual slugging |
| `est_slg` | Expected slugging (xSLG) |
| `est_slg_minus_slg_diff` | xSLG - SLG difference |
| `woba` | Actual wOBA |
| `est_woba` | Expected wOBA (xwOBA) |
| `est_woba_minus_woba_diff` | xwOBA - wOBA difference |
| `wobacon` | wOBA on contact |
| `est_wobacon` | Expected wOBA on contact |
| `est_wobacon_minus_wobacon_diff` | Difference |
| `launch_angle_avg` | Average launch angle |
| `sweet_spot_percent` | Sweet spot percentage |
| `ev_avg` | Average exit velocity |
| `ev_max` | Max exit velocity |
| `ev_fb_ld` | Exit velocity on fly balls/line drives |
| `ev_gb` | Exit velocity on ground balls |
| `distance_avg` | Average hit distance |
| `distance_hr_avg` | Average HR distance |
| `hard_hit_ct` | Hard hit count |
| `hard_hit_percent` | Hard hit rate (95+ mph) |
| `barrel_ct` | Barrel count |
| `barrel_batted_ball` | Barrels per BIP |
| `barrel_pa` | Barrels per PA |
| `is_qualified` | Whether player is qualified |

---

### `statcast_pitcher_expected_stats()`

Same structure as batter version, but for pitchers (stats against).

```python
from pybaseball import statcast_pitcher_expected_stats

statcast_pitcher_expected_stats(
    year: int,                          # Season year (YYYY)
    minPA: Union[int, str] = "q"        # Min PA against; "q" = qualified
) -> pd.DataFrame
```

**Source URL:** `https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=pitcher&year={year}&position=&team=&filterType=pa&min={minPA}&csv=true`

Returns the same column structure as the batter version, but stats represent quality of contact allowed.

---

## 3. Pitch-Level and Pitch-Type Data

### 3.1 Raw Pitch-Level Data

#### `statcast()`

Returns one row per pitch across all games in a date range.

```python
from pybaseball import statcast

statcast(
    start_dt: str = '[yesterday]',  # YYYY-MM-DD
    end_dt: str = None,             # YYYY-MM-DD (optional)
    team: str = None,               # Team abbreviation filter (e.g. 'BOS')
    verbose: bool = True,           # Progress updates
    parallel: bool = True           # Parallel HTTP requests
) -> pd.DataFrame
```

**Limits:** Baseball Savant caps at 30,000 rows per query. pybaseball auto-splits larger requests.
**Availability:** 2008+, but launch speed/angle only from 2015+.

#### `statcast_pitcher()` / `statcast_batter()`

Same as `statcast()` but filtered to a specific player.

```python
from pybaseball import statcast_pitcher, statcast_batter

statcast_pitcher(
    start_dt: str,      # YYYY-MM-DD
    end_dt: str = None,  # YYYY-MM-DD
    player_id: int = None  # MLBAM player ID
) -> pd.DataFrame

statcast_batter(
    start_dt: str,
    end_dt: str = None,
    player_id: int = None
) -> pd.DataFrame
```

**Key Columns Returned (90+ columns per pitch):**

| Column | Description |
|--------|-------------|
| `pitch_type` | Pitch type code (FF, SL, CH, CU, FC, SI, FS, KC, etc.) |
| `game_date` | Date of game |
| `release_speed` | Pitch velocity (mph) |
| `release_pos_x` | Horizontal release position (ft) |
| `release_pos_z` | Vertical release position (ft) |
| `release_pos_y` | Release distance from plate (ft) |
| `player_name` | Player name |
| `batter` | Batter MLBAM ID |
| `pitcher` | Pitcher MLBAM ID |
| `events` | Plate appearance result |
| `description` | Pitch result description |
| `zone` | Strike zone location (1-14) |
| `stand` | Batter handedness (L/R) |
| `p_throws` | Pitcher handedness (L/R) |
| `type` | B=ball, S=strike, X=in play |
| `bb_type` | ground_ball, line_drive, fly_ball, popup |
| `pfx_x` | Horizontal movement (inches, pitcher perspective) |
| `pfx_z` | Vertical movement (inches, pitcher perspective) |
| `plate_x` | Horizontal position at plate (ft) |
| `plate_z` | Vertical position at plate (ft) |
| `launch_speed` | Exit velocity (mph) |
| `launch_angle` | Launch angle (degrees) |
| `effective_speed` | Perceived velocity |
| `release_spin_rate` | Spin rate (rpm) |
| `release_extension` | Release extension (ft) |
| `spin_axis` | Spin axis direction (degrees 0-360) |
| `hit_distance_sc` | Hit distance (ft) |
| `estimated_ba_using_speedangle` | xBA for this batted ball |
| `estimated_woba_using_speedangle` | xwOBA for this batted ball |
| `woba_value` | wOBA value of outcome |
| `delta_home_win_exp` | Change in win expectancy |
| `delta_run_exp` | Change in run expectancy |
| `pitch_name` | Full pitch name (e.g. "4-Seam Fastball") |
| `at_bat_number` | PA number in game |
| `pitch_number` | Pitch number in PA |
| `home_score`, `away_score` | Pre-pitch score |
| `balls`, `strikes` | Pre-pitch count |
| `outs_when_up` | Outs at time of pitch |
| `inning`, `inning_topbot` | Inning info |
| `if_fielding_alignment` | Infield shift alignment |
| `of_fielding_alignment` | Outfield alignment |
| `on_1b`, `on_2b`, `on_3b` | Baserunner MLBAM IDs |
| `vx0`, `vy0`, `vz0` | Initial velocity components (ft/s) |
| `ax`, `ay`, `az` | Acceleration components (ft/s^2) |

---

### 3.2 Season-Level Pitch Arsenal Data (THIS IS THE KEY FUNCTION FOR PITCH CHARACTERISTICS)

#### `statcast_pitcher_pitch_arsenal()`

Retrieves season-level per-pitcher pitch characteristics: average speed, percentage share, OR average spin -- one row per pitcher, columns for each pitch type.

```python
from pybaseball import statcast_pitcher_pitch_arsenal

statcast_pitcher_pitch_arsenal(
    year: int,                          # Season year
    minP: int = 250,                    # Min pitches thrown
    arsenal_type: str = "avg_speed"     # "avg_speed", "n_", or "avg_spin"
) -> pd.DataFrame
```

**Source URL:** `https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year={year}&min={minP}&type={arsenal_type}&hand=&csv=true`

**arsenal_type options:**

| Value | What it returns |
|-------|----------------|
| `"avg_speed"` | Average velocity (mph) for each pitch type |
| `"n_"` | Usage percentage for each pitch type |
| `"avg_spin"` | Average spin rate (rpm) for each pitch type |

**Columns Returned:** One column per pitch type present in the data. Typical pitch types:
- `ff_avg_speed` / `ff_n_` / `ff_avg_spin` - 4-Seam Fastball
- `si_avg_speed` / `si_n_` / `si_avg_spin` - Sinker
- `fc_avg_speed` / `fc_n_` / `fc_avg_spin` - Cutter
- `sl_avg_speed` / `sl_n_` / `sl_avg_spin` - Slider
- `ch_avg_speed` / `ch_n_` / `ch_avg_spin` - Changeup
- `cu_avg_speed` / `cu_n_` / `cu_avg_spin` - Curveball
- `fs_avg_speed` / `fs_n_` / `fs_avg_spin` - Splitter
- `kc_avg_speed` / `kc_n_` / `kc_avg_spin` - Knuckle Curve
- Plus `player_id`, `last_name, first_name`, `team_name_abbrev`, etc.

**Usage Examples:**
```python
# Average pitch velocities for all qualified pitchers
velo = statcast_pitcher_pitch_arsenal(2024, arsenal_type="avg_speed")

# Pitch usage percentages
usage = statcast_pitcher_pitch_arsenal(2024, arsenal_type="n_")

# Average spin rates
spin = statcast_pitcher_pitch_arsenal(2024, arsenal_type="avg_spin")

# Then merge all three on player_id for a complete arsenal profile
```

---

#### `statcast_pitcher_arsenal_stats()`

Retrieves outcome stats broken down by pitch type per pitcher: run values, whiff%, BA, SLG, etc.

```python
from pybaseball import statcast_pitcher_arsenal_stats

statcast_pitcher_arsenal_stats(
    year: int,                  # Season year
    minPA: int = 25             # Min PA against
) -> pd.DataFrame
```

**Source URL:** `https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=pitcher&pitchType=&year={year}&team=&min={minPA}&csv=true`

**Columns include:** `pitch_type`, `run_value`, `run_value_per100`, `whiff_percent`, `ba`, `slg`, `woba`, `put_away`, `hard_hit_percent`, etc. One row per pitcher per pitch type.

---

#### `statcast_pitcher_pitch_movement()`

Retrieves pitch movement (horizontal and vertical break) data.

```python
from pybaseball import statcast_pitcher_pitch_movement

statcast_pitcher_pitch_movement(
    year: int,                          # Season year
    minP: Union[int, str] = "q",        # Min pitches
    pitch_type: str = "FF"              # Pitch type filter
) -> pd.DataFrame
```

**pitch_type options:** `"FF"`, `"SIFT"` (Sinker), `"CH"`, `"CUKC"` (Curveball/Knuckle Curve), `"FC"`, `"SL"`, `"FS"`, `"ALL"`

**Columns include:** `pitcher_break_x` (horizontal break in inches), `pitcher_break_z` (vertical break in inches), `avg_speed`, `pitches_thrown`, `pitcher_id`, etc.

---

#### `statcast_pitcher_active_spin()`

Retrieves active spin percentage data per pitcher.

```python
from pybaseball import statcast_pitcher_active_spin

statcast_pitcher_active_spin(
    year: int,                  # Season year
    minP: int = 250             # Min pitches
) -> pd.DataFrame
```

---

#### `statcast_pitcher_spin_dir_comp()`

Compares spin direction between two pitch types for each pitcher.

```python
from pybaseball import statcast_pitcher_spin_dir_comp

statcast_pitcher_spin_dir_comp(
    year: int,
    pitch_a: str = "4-Seamer",     # First pitch type
    pitch_b: str = "Changeup",     # Second pitch type (must differ)
    minP: int = 100,               # Min pitches of pitch_a
    pitcher_pov: bool = True       # True=pitcher perspective, False=batter
) -> pd.DataFrame
```

**Valid pitch names:** `"4-Seamer"`, `"Sinker"`, `"Changeup"`, `"Curveball"`, `"Cutter"`, `"Slider"` (or pitch codes)

---

### 3.3 Batter Pitch Arsenal Data

#### `statcast_batter_pitch_arsenal()`

Retrieves batter outcome data split by pitch type faced.

```python
from pybaseball import statcast_batter_pitch_arsenal

statcast_batter_pitch_arsenal(
    year: int,
    minPA: int = 25
) -> pd.DataFrame
```

---

## 4. Baseball Savant Leaderboard Data

### Exit Velocity & Barrels

```python
from pybaseball import statcast_batter_exitvelo_barrels, statcast_pitcher_exitvelo_barrels

# Batter batted ball quality
statcast_batter_exitvelo_barrels(
    year: int,
    minBBE: Union[int, str] = "q"   # Min batted ball events; "q" = qualified
) -> pd.DataFrame

# Pitcher batted ball quality against
statcast_pitcher_exitvelo_barrels(
    year: int,
    minBBE: Union[int, str] = "q"
) -> pd.DataFrame
```

**Columns include:** `avg_hit_speed`, `max_hit_speed`, `avg_hit_angle`, `avg_distance`, `ev95percent`, `barrels`, `brl_percent`, `brl_pa`, etc.

---

### Percentile Rankings

```python
from pybaseball import statcast_batter_percentile_ranks, statcast_pitcher_percentile_ranks

# Returns percentile ranks (0-100) for key metrics
statcast_batter_percentile_ranks(year: int) -> pd.DataFrame
statcast_pitcher_percentile_ranks(year: int) -> pd.DataFrame
```

Minimum thresholds: 2.1 PA per team game (batters), 1.25 PA per team game (pitchers).

---

### Sprint Speed & Running

```python
from pybaseball import statcast_sprint_speed, statcast_running_splits

statcast_sprint_speed(year: int, min_opp: int = 10) -> pd.DataFrame
statcast_running_splits(year: int, min_opp: int = 5, raw_splits: bool = True) -> pd.DataFrame
```

---

### Fielding

```python
from pybaseball import (
    statcast_outs_above_average,
    statcast_outfield_directional_oaa,
    statcast_outfield_catch_prob,
    statcast_outfielder_jump,
    statcast_catcher_poptime,
    statcast_catcher_framing,
    statcast_fielding_run_value,
)

statcast_outs_above_average(year, pos, min_att="q", view="Fielder")
statcast_outfield_directional_oaa(year, min_opp="q")
statcast_outfield_catch_prob(year, min_opp="q")
statcast_outfielder_jump(year, min_att="q")
statcast_catcher_poptime(year, min_2b_att=5, min_3b_att=0)
statcast_catcher_framing(year, min_called_p="q")
statcast_fielding_run_value(year, pos, min_inn=100)
```

---

## 5. Caching System

### Enable/Disable

```python
from pybaseball import cache

cache.enable()    # Turn on caching (disabled by default)
cache.disable()   # Turn off caching
cache.purge()     # Clear all cached data
```

### How It Works

- **Storage location:** `~/.pybaseball/cache/` (user's home directory)
- **Override location:** Set `PYBASEBALL_CACHE` environment variable
- **Default format:** Parquet (faster, smaller; can change to CSV)
- **Default expiration:** 1 week for most functions; some use 365 days (e.g., statcast functions)
- **Granularity:** Caches at the function + parameter level. Same function with same args returns cached data; different args = separate cache entry
- **No subset caching:** If you cached `batting_stats(2020, 2024)`, calling `batting_stats(2022, 2024)` will NOT use the cache

### Change Storage Format

```python
from pybaseball import cache
cache.enable()
cache.config.cache_type = 'csv'    # Switch from parquet to CSV
cache.config.save()
```

### Recommendation for This Project

Enable caching early to avoid redundant Baseball Savant scraping:
```python
from pybaseball import cache
cache.enable()
```

---

## 6. Player ID Systems and Cross-Referencing

### ID Systems Used

| System | Field Name | Used By | Type |
|--------|-----------|---------|------|
| MLBAM (MLB Advanced Media) | `key_mlbam` | Baseball Savant, Statcast | int |
| FanGraphs | `key_fangraphs` (or `IDfg`) | FanGraphs leaderboards | int |
| Baseball Reference | `key_bbref` | Baseball Reference | str (e.g. "troutmi01") |
| Retrosheet | `key_retro` | Retrosheet game logs | str |

### `playerid_lookup()`

Look up player IDs by name.

```python
from pybaseball import playerid_lookup

playerid_lookup(
    last: str,              # Last name (case-insensitive)
    first: str = None,      # First name (optional, case-insensitive)
    fuzzy: bool = False     # Approximate matching (returns 5 closest)
) -> pd.DataFrame
```

**Columns Returned:**

| Column | Type | Description |
|--------|------|-------------|
| `name_last` | str | Last name (lowercase) |
| `name_first` | str | First name (lowercase) |
| `key_mlbam` | int | MLBAM ID (use for Statcast functions) |
| `key_retro` | str | Retrosheet ID |
| `key_bbref` | str | Baseball Reference ID (use for get_splits) |
| `key_fangraphs` | int | FanGraphs ID (matches IDfg in batting_stats/pitching_stats) |
| `mlb_played_first` | int | First MLB season |
| `mlb_played_last` | int | Last MLB season |

**Examples:**
```python
playerid_lookup('trout', 'mike')          # Exact match
playerid_lookup('ohtani', 'shohei')       # Returns key_mlbam, key_fangraphs, etc.
playerid_lookup('martinez', 'pedro', fuzzy=True)  # Fuzzy match, 5 results
```

### `playerid_reverse_lookup()`

Look up player names/IDs given a list of IDs from any system.

```python
from pybaseball import playerid_reverse_lookup

playerid_reverse_lookup(
    player_ids: list,               # List of player IDs
    key_type: str = 'mlbam'         # 'mlbam', 'retro', 'bbref', or 'fangraphs'
) -> pd.DataFrame
```

**Examples:**
```python
# From Statcast MLBAM IDs to all ID systems
playerid_reverse_lookup([545361, 660271], key_type='mlbam')

# From FanGraphs IDs
playerid_reverse_lookup([10155, 19755], key_type='fangraphs')
```

Returns same columns as `playerid_lookup()`.

### `player_search_list()`

Batch lookup by name.

```python
from pybaseball import player_search_list

player_search_list([("trout", "mike"), ("ohtani", "shohei")])
```

### `chadwick_register()`

Access the full Chadwick Bureau player register.

```python
from pybaseball import chadwick_register

data = chadwick_register()           # In-memory only
data = chadwick_register(save=True)  # Also save to disk
```

Returns the complete cross-reference table for all players with all ID systems.

### Cross-Referencing Strategy

The critical join challenge: **FanGraphs uses `IDfg` (= `key_fangraphs`), while Statcast/Savant uses MLBAM IDs (= `key_mlbam`)**. To merge:

```python
from pybaseball import chadwick_register

# Get the full ID mapping table
register = chadwick_register()
id_map = register[['key_mlbam', 'key_fangraphs', 'key_bbref', 'name_last', 'name_first']].dropna(subset=['key_mlbam', 'key_fangraphs'])

# Now join:
# FanGraphs data has IDfg -> map to key_fangraphs -> get key_mlbam
# Statcast data has player_id (MLBAM) -> map to key_mlbam -> get key_fangraphs
```

---

## 7. Split Stats

### `get_splits()`

Pulls split statistics from Baseball Reference. Returns a multi-index DataFrame.

```python
from pybaseball import get_splits

get_splits(
    playerid: str,                  # Baseball Reference player ID (e.g. 'troutmi01')
    year: int = None,               # Specific year; None = career splits
    player_info: bool = False,      # If True, also returns player info dict
    pitching_splits: bool = False   # True for pitching; False for batting
) -> pd.DataFrame  # or (pd.DataFrame, dict) if player_info=True
```

**Split Categories Available (from Baseball Reference):**

The returned DataFrame uses a multi-index with split categories including:
- **Platoon:** vs LHP, vs RHP
- **Home/Away:** Home, Away
- **Half:** 1st Half, 2nd Half (split at All-Star Break)
- **Month:** April/March, May, June, July, August, September/October
- **Day/Night:** Day, Night
- **Batting Order:** by lineup position
- **Count:** various count situations
- **Leverage:** High, Medium, Low leverage
- **Baserunners:** bases empty, runners on, RISP, bases loaded
- **Outs:** 0 outs, 1 out, 2 outs
- **Opponent quality:** various
- **Pitches seen:** pitch count brackets
- And many more...

**Important Note:** The player ID required is the Baseball Reference ID (`key_bbref`), NOT the MLBAM or FanGraphs ID.

**Examples:**
```python
# Career batting splits for Mike Trout
splits = get_splits('troutmi01')

# 2024 batting splits with player info
splits, info = get_splits('troutmi01', year=2024, player_info=True)

# Career pitching splits for Gerrit Cole
splits = get_splits('colege01', pitching_splits=True)
```

### Alternative: Date-Range Functions for Half-Season Stats

For getting FanGraphs-quality stats for the second half specifically, use date-range functions:

```python
from pybaseball import batting_stats_range, pitching_stats_range

# 2024 second half (ASB was July 16, 2024)
batting_2h = batting_stats_range('2024-07-16', '2024-09-29')
pitching_2h = pitching_stats_range('2024-07-16', '2024-09-29')
```

**Tradeoff:** `batting_stats_range` pulls from Baseball Reference (fewer columns, ~30 standard stats) while `batting_stats` pulls from FanGraphs (~318 columns with advanced metrics). For second-half splits with advanced metrics, raw Statcast data filtered by date is the best option.

---

## 8. Additional Useful Functions

### Team Stats

```python
from pybaseball import team_batting, team_pitching, team_fielding

team_batting(start_season, end_season=None)
team_pitching(start_season, end_season=None)
team_fielding(start_season, end_season=None)
```

### Schedule & Standings

```python
from pybaseball import schedule_and_record, standings

schedule_and_record(season=2024, team='NYY')  # Game-by-game for a team
standings(season=2024)                         # Division standings (returns list of DataFrames)
```

### WAR (Baseball Reference)

```python
from pybaseball import bwar_bat, bwar_pitch

bwar_bat()    # All-time batter WAR from Baseball Reference
bwar_pitch()  # All-time pitcher WAR from Baseball Reference
```

### Draft & Prospects

```python
from pybaseball import amateur_draft, top_prospects

amateur_draft(year=2024)
top_prospects()
```

---

## 9. Complete Function Index

### Data Collection Functions (Most Relevant for This Project)

| Function | Source | Level | Key Use |
|----------|--------|-------|---------|
| `batting_stats()` | FanGraphs | Season | Primary batter stats (~318 cols) |
| `pitching_stats()` | FanGraphs | Season | Primary pitcher stats (~391 cols) |
| `statcast_batter_expected_stats()` | Savant | Season | xBA, xSLG, xwOBA, EV, LA, barrel% |
| `statcast_pitcher_expected_stats()` | Savant | Season | xBA, xSLG, xwOBA against |
| `statcast_pitcher_pitch_arsenal()` | Savant | Season | Avg speed, usage%, avg spin by pitch type |
| `statcast_pitcher_arsenal_stats()` | Savant | Season | Run value, whiff%, BA/SLG by pitch type |
| `statcast_pitcher_pitch_movement()` | Savant | Season | Horizontal/vertical break by pitch type |
| `statcast_pitcher_active_spin()` | Savant | Season | Active spin % by pitch type |
| `statcast_batter_exitvelo_barrels()` | Savant | Season | EV, barrel%, batted ball quality |
| `statcast_pitcher_exitvelo_barrels()` | Savant | Season | EV, barrel% against |
| `statcast_batter_percentile_ranks()` | Savant | Season | Percentile ranks for key metrics |
| `statcast_pitcher_percentile_ranks()` | Savant | Season | Percentile ranks for key metrics |
| `statcast()` | Savant | Pitch | All pitches in date range (~90 cols) |
| `statcast_pitcher()` | Savant | Pitch | Single pitcher, all pitches |
| `statcast_batter()` | Savant | Pitch | Single batter, all pitches |
| `get_splits()` | BBRef | Season | Split stats (1H/2H, platoon, etc.) |
| `batting_stats_range()` | BBRef | Custom dates | Second-half stats by date range |
| `pitching_stats_range()` | BBRef | Custom dates | Second-half stats by date range |
| `playerid_lookup()` | Chadwick | Lookup | Name -> all IDs |
| `playerid_reverse_lookup()` | Chadwick | Lookup | ID -> all IDs |
| `chadwick_register()` | Chadwick | Lookup | Complete ID cross-reference |
| `statcast_sprint_speed()` | Savant | Season | Sprint speed data |

### Data Availability Timeline

| Feature | Available From |
|---------|---------------|
| Basic stats (FanGraphs) | 1871+ |
| Statcast pitch tracking | 2008+ |
| Exit velocity, launch angle | 2015+ |
| Expected stats (xBA, xwOBA) | 2015+ |
| Sprint speed | 2015+ |
| Barrel classification | 2015+ |
| Stuff+, Location+, Pitching+ | 2020+ |
| Active spin | 2020+ |
| Bat speed / swing data | 2024+ |
