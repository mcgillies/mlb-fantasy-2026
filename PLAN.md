# MLB Fantasy 2026 - Project Plan

## Overview
Predict 2026 fantasy baseball points using advanced metrics from Baseball Savant via pybaseball. Train separate batter and pitcher models on per-PA/IP rate stats, then scale to totals using external PA/IP projections. Pitcher W/L/Hold/Save are handled separately via external projections (team-dependent, not skill-based).

---

## Phase 1: Data Collection & Processing
**Status: Not started**

### 1.1 Collect historical base stats (2015-2025)
- [ ] Use `pybaseball.batting_stats()` to pull FanGraphs batting data
- [ ] Use `pybaseball.pitching_stats()` to pull FanGraphs pitching data
- [ ] Verify columns include: PA, G, TB, R, RBI, BB, SB, K (batters) and IP, K, BB, H, ER (pitchers)
- [ ] Save raw data to `data/raw/`

### 1.2 Collect Statcast advanced metrics (2015-2025)
- [ ] Batter expected stats: xBA, xSLG, xwOBA, barrel%, hard_hit%, exit_velo, launch_angle
- [ ] Batter swing metrics: swing_speed, whiff%, chase%, contact%, zone_swing%
- [ ] Pitcher expected stats: xBA, xSLG, xwOBA, xERA
- [ ] Pitcher pitch characteristics: fastball velo, spin rate, break, usage rates
- [ ] Pitcher plate discipline induced: whiff%, chase%, K%, BB%, K-BB%
- [ ] Investigate what pybaseball functions provide the best coverage
- [ ] Handle year-over-year schema changes in Statcast data

### 1.3 Collect second-half splits (2015-2025)
- [ ] Pull post-All-Star-Break stats/metrics for batters and pitchers
- [ ] Use as additional features to capture late-season trends and breakouts
- [ ] Determine best pybaseball approach (date-filtered statcast or FanGraphs splits)

### 1.4 Calculate fantasy points
- [ ] Apply batter scoring formula (config/scoring.py) to base stats
- [ ] Apply skill-based pitcher scoring (excludes W/L/Hold/Save) to base stats
- [ ] Compute rate stats: Fpoints_PA (batters), Fpoints_IP (pitchers)
- [ ] Verify against manual calculations for a few known players

### 1.5 Merge and process data
- [ ] Join base stats with Statcast metrics using player IDs (not names)
- [ ] Lag metrics by 1 year (year N-1 metrics predict year N fpoints)
- [ ] Normalize player names (unicode handling)
- [ ] Save processed datasets to `data/processed/`

### 1.6 Handle missing data
- [ ] Identify rookies (no previous MLB stats) — impute with league/position means or external projections
- [ ] Identify injured players (low PA/IP in previous year) — use most recent healthy season or weighted average
- [ ] Add data quality flags (is_rookie, is_injured_season, small_sample)
- [ ] Consider pulling minor league data for top prospects if available via pybaseball

### 1.7 Collect external projections
- [ ] Download PA/IP projections from Steamer/ZiPS/ATC (for scaling rate to totals)
- [ ] Download W/L/Hold/Save projections for pitchers (team-dependent component)
- [ ] These may need to be manual CSV downloads from FanGraphs
- [ ] Store in `data/projections/`

---

## Phase 2: Feature Engineering
**Status: Not started**

### 2.1 Create lag features
- [ ] 1-year lag (already present via the year N-1 metrics merge)
- [ ] 2-year lag for key metrics (additional lookback)
- [ ] Historical rolling average of fantasy points per PA/IP (2-3 year windows)

### 2.2 Second-half features
- [ ] Post-ASB metrics as separate features (e.g., xBA_2H, exit_velo_2H)
- [ ] Evaluate whether these add signal vs noise in early experiments

### 2.3 Derived features
- [ ] Age
- [ ] Years of MLB experience
- [ ] Year-over-year deltas for key metrics (improvement/decline trends)
- [ ] Consider interaction features if they help

### 2.4 Feature selection
- [ ] Analyze correlations, drop redundant features
- [ ] Document final feature sets for batter and pitcher models

---

## Phase 3: Model Training
**Status: Not started**

### 3.1 Batter model
- [ ] Target: Fpoints_PA (skill-based fantasy points per plate appearance)
- [ ] Train XGBoost, LightGBM, Random Forest, Gradient Boosting
- [ ] Hyperparameter tuning (grid search or Bayesian)
- [ ] Cross-validation with time-aware splits
- [ ] Backtest: train on years < N, predict year N (using N-1 metrics)
- [ ] Select best model

### 3.2 Pitcher model
- [ ] Target: Fpoints_IP (skill-based, excludes W/L/Hold/Save)
- [ ] Same model comparison as batters
- [ ] Consider whether SP/RP need separate models or a combined model with role indicator
- [ ] Do NOT use W/L/S/Hold as features — these are outcomes, not predictors

### 3.3 Model evaluation
- [ ] MAE, RMSE, R² on holdout data
- [ ] Year-by-year backtest results (train < N, test = N, features from N-1)
- [ ] Feature importance analysis (built-in + SHAP)
- [ ] Residual analysis — are errors systematic for any player type?

---

## Phase 4: Prediction & Ranking
**Status: Not started**

### 4.1 Generate 2026 predictions
- [ ] Apply trained models to 2025 Statcast metrics
- [ ] Get rate predictions (Fpoints/PA, Fpoints/IP — skill-based)
- [ ] Scale to totals using averaged external PA/IP projections
- [ ] Add W/L/Hold/Save contributions for pitchers from external projections
- [ ] Handle edge cases (rookies, role changes, injuries)

### 4.2 Rankings
- [ ] Overall rankings by total projected Fpoints
- [ ] Positional rankings (C, 1B, 2B, 3B, SS, OF, SP, RP, DH)
- [ ] Save to `predictions/`

---

## Phase 5: Interactive App
**Status: Not started**

### 5.1 Streamlit app
- [ ] Player selector (dropdown for batter/pitcher, then player name)
- [ ] Display: predicted Fpoints (rate + total), key stats, position
- [ ] For pitchers: show skill-based + team-based breakdown
- [ ] SHAP waterfall plot for individual prediction explanation
- [ ] Optional: comparison with expert projections

---

## Phase 6: Write-up & Documentation
**Status: Not started**

### 6.1 Jupyter Book
- [ ] Introduction and methodology
- [ ] Model definitions and feature importance
- [ ] Positional analysis chapters
- [ ] Notable players and interesting findings
- [ ] Build and publish

---

## Key Improvements Over 2025

| Area | 2025 | 2026 |
|------|------|------|
| Data collection | Manual CSV downloads | pybaseball (automated, reproducible) |
| Player matching | Name-based (collision issues) | Player ID-based primary keys |
| Pitcher scoring | Model trained on incomplete formula | Skill-only target; W/L/Hold/S via external projections |
| Historical depth | Single year lookback | Multi-year lags + rolling averages |
| Sub-season context | Full season only | Second-half splits as features |
| Missing data | Not handled | Imputation for rookies & injured |
| Explainability | LIME | SHAP (faster for tree models) |
| Rate denomination | Fpoints/G (batters) | Fpoints/PA (more stable) |
| Interactive | Static notebooks | Streamlit app |
