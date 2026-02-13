"""
Model evaluation and comparison utilities.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true, y_pred):
    """Compute regression metrics."""
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }


def backtest(model, df, target_col, feature_cols, test_years):
    """
    Backtest model by training on years before test_year and predicting test_year.

    Args:
        model: Sklearn-compatible model.
        df: Full dataset with 'year' column.
        target_col: Target variable name.
        feature_cols: List of feature column names.
        test_years: List of years to test on.

    Returns:
        DataFrame of metrics per test year.
    """
    # TODO: implement year-by-year backtesting
    pass
