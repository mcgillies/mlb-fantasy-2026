# Feature Engineering

## Lag Features (Level)
- Using prior year stats as predictors
- 1-year and 2-year lags

## Trend Features (Direction)
- Second-half deltas (2H - 1H) to capture trajectory
- Why deltas over full 2H features?

## Key Features by Type

### Batters
- Contact quality (exit velocity, barrel rate, hard hit %)
- Plate discipline (O-Swing%, Z-Contact%, whiff rate)
- Speed metrics (sprint speed)
- Age

### Pitchers
- Stuff+ (pitch quality composite)
- Command metrics (zone rate, chase rate induced)
- Batted ball profile (GB%, FB%, HR/FB)
- Workload history

## Feature Selection
- Correlation analysis
- Avoiding multicollinearity
