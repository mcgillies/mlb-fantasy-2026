"""
Prediction pipeline.

Generates fantasy point predictions for the upcoming season.

For batters: model predicts Fpoints/PA, scaled by projected PA.
For pitchers: model predicts skill-based Fpoints/IP, scaled by projected IP,
then W/L/Hold/Save contributions are added from external projections.
"""

import pandas as pd
from config.settings import PREDICTIONS_DIR


def predict_rate_stats(model, X):
    """
    Generate rate-based predictions (Fpoints/PA or Fpoints/IP).

    Args:
        model: Trained model.
        X: Feature matrix for prediction year.

    Returns:
        Array of predicted rate stats.
    """
    return model.predict(X)


def scale_to_totals(rate_preds, projected_usage):
    """
    Scale rate predictions to total fantasy points using projected PA/IP.

    Args:
        rate_preds: Predicted Fpoints per PA or IP.
        projected_usage: Projected PA or IP for each player.

    Returns:
        Total projected fantasy points (skill component only for pitchers).
    """
    return rate_preds * projected_usage


def add_pitcher_team_fpoints(df, projected_wlhs):
    """
    Add team-dependent fantasy point contributions to pitcher predictions.

    Args:
        df: DataFrame with skill-based Fpoints_skill column.
        projected_wlhs: DataFrame with projected W, L, Hold, S per pitcher
                        (from external projection systems).

    Returns:
        DataFrame with Fpoints_team and Fpoints_total added.
    """
    # TODO: merge external W/L/Hold/Save projections, apply scoring weights
    pass


def generate_rankings(predictions_df, position_col="Pos"):
    """
    Generate overall and positional rankings from predictions.

    Args:
        predictions_df: DataFrame with player info and predicted Fpoints.
        position_col: Column containing player positions.

    Returns:
        Dict of DataFrames keyed by position, plus 'overall'.
    """
    # TODO: implement ranking generation
    pass


def save_predictions(predictions_df, filename="full_predictions.csv"):
    """Save predictions to CSV."""
    path = f"{PREDICTIONS_DIR}/{filename}"
    predictions_df.to_csv(path, index=False)
    print(f"Predictions saved to {path}")
