"""
Global project settings.
"""

# Historical data range for training
TRAIN_START_YEAR = 2015
TRAIN_END_YEAR = 2024

# Season to predict
PREDICT_YEAR = 2025  # 2025 stats -> 2026 fantasy projections

# Minimum thresholds for inclusion in training data
MIN_PA_BATTER = 100      # minimum plate appearances per season
MIN_IP_PITCHER = 20      # minimum innings pitched per season

# Minimum thresholds for prediction candidates
MIN_PA_PREDICT = 50
MIN_IP_PREDICT = 10

# Paths
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
PROJECTIONS_DIR = "data/projections"
CACHE_DIR = "data/cache"
MODELS_DIR = "models"
PREDICTIONS_DIR = "predictions"

# pybaseball cache
PYBASEBALL_CACHE_DIR = "data/cache/pybaseball"

# Random seed
RANDOM_STATE = 42
