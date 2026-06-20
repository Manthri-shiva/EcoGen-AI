"""
EcoGen AI - Explainability Engine

Explains why the carbon footprint prediction was generated
using feature importance analysis from the trained Linear
Regression model.
"""

from pathlib import Path
from typing import Any, Dict, List, Sequence, Optional

import numpy as np
import pandas as pd
from joblib import load


FEATURE_KEYS = [
    "age",
    "family_size",
    "electricity_bill",
    "water_usage",
    "daily_travel_km",
    "waste_generated",
]

MODEL_PATH = Path("models/carbon_model.pkl")
DATASET_PATH = Path("datasets/carbon/sample_users.csv")


def load_trained_model() -> Any:
    """Load trained ML model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return load(MODEL_PATH)


def load_dataset() -> pd.DataFrame:
    """Load dataset used for training."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    return pd.read_csv(DATASET_PATH)


def calculate_feature_importance(
    model: Any,
    dataset: pd.DataFrame,
    feature_names: Sequence[str] = FEATURE_KEYS
) -> Dict[str, float]:
    """
    Calculate realistic feature importance.

    Uses:
    coefficient × feature standard deviation

    Then normalizes to percentages.
    """

    coefficients = np.abs(
        np.asarray(model.coef_)
    )

    feature_std = dataset[
        list(feature_names)
    ].std()

    weighted_importance = (
        coefficients *
        feature_std.values
    )

    total_importance = np.sum(
        weighted_importance
    )

    percentages = (
        weighted_importance /
        total_importance
    ) * 100

    importance = {}

    for feature, value in zip(
        feature_names,
        percentages
    ):
        importance[feature] = round(
            float(value),
            2
        )

    importance = dict(
        sorted(
            importance.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return importance


def get_top_contributors(
    importance: Dict[str, float],
    top_n: int = 6
) -> List[Dict[str, Any]]:
    """Get ranked contributors."""

    return [
        {
            "feature": feature,
            "importance": percentage
        }
        for feature, percentage in list(
            importance.items()
        )[:top_n]
    ]


def generate_actionable_insights(
    contributors: List[Dict[str, Any]]
) -> List[str]:

    insights = []

    if not contributors:
        return insights

    top_feature = contributors[0]["feature"]

    feature_actions = {
        "electricity_bill":
            "Reducing electricity usage could significantly lower emissions.",

        "daily_travel_km":
            "Using public transport or carpooling can reduce travel emissions.",

        "waste_generated":
            "Reducing waste generation and recycling can improve sustainability.",

        "water_usage":
            "Improving water efficiency can lower environmental impact.",

        "family_size":
            "Household efficiency improvements can reduce resource consumption.",

        "age":
            "Lifestyle choices have a greater impact than age."
    }

    insights.append(
        f"{top_feature.replace('_', ' ').title()} is your largest contributor."
    )

    insights.append(
        feature_actions.get(
            top_feature,
            "Focus on reducing this factor."
        )
    )

    return insights


def predict_carbon_footprint(
    model: Any,
    inputs: Dict[str, float]
) -> float:

    df = pd.DataFrame([inputs])

    prediction = model.predict(df)

    return round(
        float(prediction[0]),
        2
    )


def generate_explanation(
    inputs: Dict[str, float]
) -> Dict[str, Any]:

    model = load_trained_model()

    dataset = load_dataset()

    feature_importance = calculate_feature_importance(
        model,
        dataset
    )

    contributors = get_top_contributors(
        feature_importance
    )

    insights = generate_actionable_insights(
        contributors
    )

    prediction = predict_carbon_footprint(
        model,
        inputs
    )

    return {
        "predicted_footprint": prediction,
        "feature_importance": feature_importance,
        "top_contributors": contributors,
        "insights": insights
    }


if __name__ == "__main__":

    sample_input = {
        "age": 25,
        "family_size": 4,
        "electricity_bill": 2000,
        "water_usage": 500,
        "daily_travel_km": 20,
        "waste_generated": 25
    }

    result = generate_explanation(
        sample_input
    )

    print("\n")
    print("=" * 55)
    print("ECOGEN AI - EXPLAINABILITY REPORT")
    print("=" * 55)

    print(
        f"\nPredicted Carbon Footprint: "
        f"{result['predicted_footprint']} kg CO2"
    )

    print("\nFeature Importance Ranking\n")

    rank = 1

    for feature, value in result[
        "feature_importance"
    ].items():

        print(
            f"{rank}. "
            f"{feature.replace('_', ' ').title()} "
            f"→ {value}%"
        )

        rank += 1

    print("\nTop Contributors\n")

    for contributor in result[
        "top_contributors"
    ][:3]:

        print(
            f"- {contributor['feature'].replace('_', ' ').title()} "
            f"({contributor['importance']}%)"
        )

    print("\nActionable Insights\n")

    for insight in result["insights"]:
        print(f"- {insight}")

    print("\n" + "=" * 55)