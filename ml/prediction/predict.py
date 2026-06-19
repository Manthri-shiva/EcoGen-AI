"""
Prediction utilities for EcoGen AI.

Loads a trained model and exposes predict_carbon_footprint()
which accepts user inputs and returns a predicted carbon footprint.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

import pandas as pd
from joblib import load

MODEL_PATH = Path("models") / "carbon_model.pkl"

_CACHED_MODEL = None


def load_model(path: Path = MODEL_PATH) -> Any:
    """
    Load trained model from disk.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found: {path}"
        )

    return load(path)


def predict_carbon_footprint(
    age: float,
    family_size: float,
    electricity_bill: float,
    water_usage: float,
    daily_travel_km: float,
    waste_generated: float,
) -> float:
    """
    Predict carbon footprint using trained model.
    """

    global _CACHED_MODEL

    if _CACHED_MODEL is None:
        _CACHED_MODEL = load_model()

    input_data = pd.DataFrame(
        [{
            "age": float(age),
            "family_size": float(family_size),
            "electricity_bill": float(electricity_bill),
            "water_usage": float(water_usage),
            "daily_travel_km": float(daily_travel_km),
            "waste_generated": float(waste_generated)
        }]
    )

    prediction = _CACHED_MODEL.predict(input_data)

    return float(prediction[0])


if __name__ == "__main__":

    try:

        print("Model loaded successfully")

        result = predict_carbon_footprint(
            age=25,
            family_size=4,
            electricity_bill=2000,
            water_usage=500,
            daily_travel_km=20,
            waste_generated=25
        )

        print(
            f"Predicted Carbon Footprint: {result:.2f} kg CO2"
        )

    except Exception as error:

        print(
            f"Error: {error}"
        )

        sys.exit(1)