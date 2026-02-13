"""
Model training for batter and pitcher fantasy point prediction.

Uses gradient boosting (XGBoost/LightGBM) and random forest models.
"""

import joblib
import numpy as np
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from config.settings import RANDOM_STATE, MODELS_DIR


MODELS = {
    "xgboost": XGBRegressor(random_state=RANDOM_STATE),
    "lightgbm": LGBMRegressor(random_state=RANDOM_STATE, verbose=-1),
    "random_forest": RandomForestRegressor(random_state=RANDOM_STATE),
    "gradient_boosting": GradientBoostingRegressor(random_state=RANDOM_STATE),
}


def train_model(X_train, y_train, model_type="xgboost", params=None):
    """
    Train a model on the provided data.

    Args:
        X_train: Feature matrix.
        y_train: Target vector.
        model_type: One of 'xgboost', 'lightgbm', 'random_forest', 'gradient_boosting'.
        params: Optional hyperparameter dict to override defaults.

    Returns:
        Trained model.
    """
    # TODO: implement training with optional hyperparameter tuning
    pass


def evaluate_model(model, X, y, cv=5):
    """
    Evaluate model using cross-validation.

    Returns:
        Dict of metrics (MAE, RMSE, R2).
    """
    # TODO: implement cross-validation evaluation
    pass


def save_model(model, name):
    """Save a trained model to disk."""
    path = f"{MODELS_DIR}/{name}.joblib"
    joblib.dump(model, path)
    print(f"Model saved to {path}")


def load_model(name):
    """Load a trained model from disk."""
    path = f"{MODELS_DIR}/{name}.joblib"
    return joblib.load(path)
