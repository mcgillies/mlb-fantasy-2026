# Model Training & Evaluation

## Model Choice: Random Forest
- Why Random Forest over XGBoost/LightGBM?
- Interpretability vs. marginal accuracy gains

## Regularization
- Preventing single-feature dominance
- Hyperparameters: max_depth, min_samples_leaf, max_features

## Training Setup
- Train on 2021-2024 data
- Validate on 2025 season
- Target: Fpoints/PA (batters) or Fpoints/IP (pitchers)

## Results

### Batter Model Performance
- RMSE, MAE, R²
- Feature importance (SHAP)

### Pitcher Model Performance
- RMSE, MAE, R²
- Feature importance (SHAP)

## Model Interpretation
- SHAP summary plots
- Example player explanations
