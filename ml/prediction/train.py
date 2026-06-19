"""Train a Linear Regression model for EcoGen AI (Session 3 Phase 2).

Loads dataset from `datasets/carbon/sample_users.csv`, trains a linear
regression model using specified numeric features, evaluates performance,
and saves the trained model to `models/carbon_model.pkl`.

This file includes type hints, comments, and error handling.
"""
from __future__ import annotations

from typing import Tuple, List
import os
import sys
from pathlib import Path

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover - explicit install error
    raise ImportError("pandas is required to run this script. Install with: pip install pandas") from exc

try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
except Exception as exc:  # pragma: no cover - explicit install error
    raise ImportError("scikit-learn is required to run this script. Install with: pip install scikit-learn") from exc

try:
    from joblib import dump
except Exception:
    try:
        # Older sklearn exposes joblib under sklearn.externals
        from sklearn.externals.joblib import dump  # type: ignore
    except Exception as exc:  # pragma: no cover - explicit install error
        raise ImportError("joblib is required to save the model. Install with: pip install joblib") from exc


DATA_PATH = Path("datasets") / "carbon" / "sample_users.csv"
MODEL_PATH = Path("models") / "carbon_model.pkl"


def load_dataset(path: Path) -> pd.DataFrame:
    """Load dataset from CSV and perform basic validation.

    Args:
        path: Path to the CSV file.

    Returns:
        A pandas DataFrame with the dataset.

    Raises:
        FileNotFoundError: if the CSV does not exist.
        ValueError: if required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)

    required_columns = [
        "age",
        "family_size",
        "electricity_bill",
        "water_usage",
        "daily_travel_km",
        "waste_generated",
        "total_carbon_footprint",
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    return df


def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Select features and target from the DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (X, y) where X is DataFrame of features and y is target Series.
    """
    feature_cols: List[str] = [
        "age",
        "family_size",
        "electricity_bill",
        "water_usage",
        "daily_travel_km",
        "waste_generated",
    ]

    X = df[feature_cols].copy()
    y = df["total_carbon_footprint"].copy()
    return X, y


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Train a Linear Regression model and return it.

    Args:
        X_train: Training features.
        y_train: Training target.

    Returns:
        Trained LinearRegression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[float, float, float]:
    """Evaluate model and return MAE, RMSE, R2.

    Args:
        model: Trained model.
        X_test: Test features.
        y_test: Test target.

    Returns:
        Tuple of (mae, rmse, r2)
    """
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = float(mse ** 0.5)
    r2 = r2_score(y_test, preds)
    return mae, rmse, r2


def save_model(model: LinearRegression, path: Path) -> None:
    """Persist the trained model to disk using joblib.

    Args:
        model: Trained model instance.
        path: Destination path for the saved model.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(model, path)


def main() -> int:
    """Main training routine.

    Returns:
        Exit code (0 success, non-zero failure)
    """
    try:
        df = load_dataset(DATA_PATH)
    except Exception as exc:
        print(f"[ERROR] Loading dataset failed: {exc}")
        return 2

    # Prepare features and target
    X, y = prepare_features(df)

    # Print dataset shape
    print(f"Dataset shape: {df.shape}")

    # Split dataset (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Number of training samples: {X_train.shape[0]}")
    print(f"Number of testing samples: {X_test.shape[0]}")

    # Train
    try:
        model = train_model(X_train, y_train)
    except Exception as exc:
        print(f"[ERROR] Model training failed: {exc}")
        return 3

    # Evaluate
    try:
        mae, rmse, r2 = evaluate_model(model, X_test, y_test)
    except Exception as exc:
        print(f"[ERROR] Model evaluation failed: {exc}")
        return 4

    # Print metrics
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")

    # Save model
    try:
        save_model(model, MODEL_PATH)
        print(f"Model saved to: {MODEL_PATH}")
    except Exception as exc:
        print(f"[ERROR] Saving model failed: {exc}")
        return 5

    return 0


if __name__ == "__main__":
    code = main()
    sys.exit(code)
# Train prediction model
