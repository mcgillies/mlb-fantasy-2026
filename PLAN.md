# MLB Fantasy 2026 - Project Plan

## Overview
Predict 2026 fantasy baseball points using advanced metrics from Baseball Savant via pybaseball. Train separate batter and pitcher models on per-PA/IP rate stats, then scale to totals using external PA/IP projections. Pitcher W/L/Hold/Save are handled separately via external projections (team-dependent, not skill-based).

---

## Phase 1: Data Collection & Processing
**Status: In progress**

### 1.1 Collect historical base stats (2015-2025)
- [x] Use `pybaseball.batting_stats()` to pull FanGraphs batting data (4,836 player-seasons, 320 cols)
- [x] Use `pybaseball.pitching_stats()` to pull FanGraphs pitching data (5,696 player-seasons, 393 cols)
- [x] Verify columns include: PA, G, TB, R, RBI, BB, SB, K (batters) and IP, K, BB, H, ER (pitchers)
- [x] Save raw data to `data/raw/`

### 1.2 Collect Statcast advanced metrics (2015-2025)
- [x] Batter expected stats: xBA, xSLG, xwOBA, barrel%, hard_hit%, exit_velo, launch_angle (included in FG data + savant_batter_expected.csv)
- [x] Batter swing metrics: whiff%, chase%, contact%, zone_swing% (included in FanGraphs data)
- [x] Pitcher expected stats: xBA, xSLG, xwOBA, xERA (included in FG data + savant_pitcher_expected.csv)
- [x] Pitcher pitch characteristics: fastball velo, spin rate, usage rates (savant_pitcher_arsenal.csv - 6,294 rows)
- [x] Pitcher plate discipline induced: whiff%, K%, BB%, K-BB% (included in FG data + savant_pitcher_arsenal_stats.csv)
- [x] Investigate what pybaseball functions provide the best coverage
- [x] Handle year-over-year schema changes in Statcast data
- [x] Collect player ID mapping (chadwick_register - 25,901 players) for FanGraphs<->Savant joins

### 1.3 Collect second-half splits (2015-2025)
- [ ] Pull post-All-Star-Break stats/metrics for batters and pitchers
- [ ] Use as additional features to capture late-season trends and breakouts
- [ ] Determine best pybaseball approach (date-filtered statcast or FanGraphs splits)
- **Note:** Will implement 2H-1H deltas for key metrics rather than full second-half feature set

### 1.4 Calculate fantasy points
- [x] Apply batter scoring formula: TB + R + RBI + BB + SB - K
- [x] Apply skill-based pitcher scoring: 3*IP + K - BB - H - 2*ER (excludes W/L/Hold/Save)
- [x] Compute rate stats: Fpoints_PA (mean=0.463), Fpoints_IP (mean=1.685)
- [x] Verified calculations look reasonable

### 1.5 Merge and process data
- [x] Selected ~32 key features per player type based on predictive correlation analysis
- [x] Created lag features: 1-year and 2-year lags for all features
- [x] Created rolling averages: 2-year and 3-year windows for Fpoints
- [x] Merged FanGraphs + Savant data using player ID crosswalk
- [x] Added pitcher arsenal data (fastball velo, spin, etc.)
- [x] Saved processed datasets to `data/processed/`
  - batters_processed.csv: 3,578 rows, 113 cols (66 model features)
  - pitchers_processed.csv: 3,985 rows, 120 cols (78 model features)

### 1.6 Handle missing data
- [ ] **Improve imputation beyond median** — current approach fills NaN with training median, which is naive
  - Consider: KNN imputation, position-specific means, age-based imputation
  - For pitch-level features: impute based on pitcher's other pitches or league averages for pitch type
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
**Status: Mostly complete**

### 2.1 Create lag features
- [x] 1-year lag for 32 batter features, 31 pitcher features
- [x] 2-year lag for all features (additional lookback)
- [x] Historical rolling average of fantasy points per PA/IP (2-year and 3-year windows)

### 2.2 Second-half features
- [ ] Post-ASB 2H-1H deltas for key metrics (optional enhancement)
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
**Status: In progress (notebooks ready for user to run)**

### 3.1 Batter model
- [x] Target: Fpoints_PA (skill-based fantasy points per plate appearance)
- [x] Train XGBoost, LightGBM, Random Forest, Ridge (notebooks/03_batter_model.ipynb)
- [x] Hyperparameter tuning (GridSearchCV)
- [x] Cross-validation with 5-fold CV
- [x] Train/val split: 2016-2023 train, 2024-2025 validation
- [x] predict_player() function with SHAP waterfall
- [x] predict_season() and show_season_summary() for evaluation
- [ ] Run notebook and evaluate results

### 3.2 Pitcher model
- [x] Target: Fpoints_IP (skill-based, excludes W/L/Hold/Save)
- [x] Same model comparison as batters (notebooks/04_pitcher_model.ipynb)
- [x] Combined SP/RP model with role indicator (SP_pct feature)
- [x] SP vs RP performance comparison included
- [x] predict_player() shows team-based points breakdown
- [ ] Run notebook and evaluate results

### 3.3 Model evaluation
- [x] MAE, RMSE, R² on holdout data (built into notebooks)
- [x] Rank correlation between predicted and actual
- [x] Feature importance analysis (built-in + SHAP)
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
