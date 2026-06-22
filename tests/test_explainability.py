from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT_DIR))
os.chdir(ROOT_DIR)

from ml.explainability.shap_engine import (
    calculate_feature_importance,
    generate_actionable_insights,
    get_top_contributors,
    load_dataset,
    load_trained_model,
)


@pytest.fixture
def model() -> Any:
    """Load the trained model once for explainability tests."""
    return load_trained_model()


@pytest.fixture
def dataset() -> Any:
    """Load the dataset once for explainability tests."""
    return load_dataset()


def test_model_loads() -> Any:
    """Verify the trained model loads successfully."""

    model = load_trained_model()
    assert model is not None
    return model


def test_dataset_loads() -> Any:
    """Verify the dataset loads successfully."""

    dataset = load_dataset()
    assert dataset is not None
    assert not dataset.empty
    return dataset


def test_feature_importance_sums_to_hundred(model: Any, dataset: Any) -> None:
    """Verify feature importance percentages sum approximately to 100%."""

    importance = calculate_feature_importance(model, dataset)
    total = sum(importance.values())
    assert abs(total - 100.0) < 1.0


def test_top_contributors_returned(model: Any, dataset: Any) -> None:
    """Verify top contributors are returned."""

    importance = calculate_feature_importance(model, dataset)
    contributors = get_top_contributors(importance)
    assert isinstance(contributors, list)
    assert len(contributors) > 0
    assert all("feature" in contributor and "importance" in contributor for contributor in contributors)


def test_actionable_insights_generated(model: Any, dataset: Any) -> None:
    """Verify actionable insights are generated."""

    importance = calculate_feature_importance(model, dataset)
    contributors = get_top_contributors(importance)
    insights = generate_actionable_insights(contributors)
    assert isinstance(insights, list)
    assert len(insights) >= 2
    assert all(isinstance(insight, str) for insight in insights)


def main() -> None:
    model = test_model_loads()
    print("TEST 1 PASSED")

    dataset = test_dataset_loads()
    print("TEST 2 PASSED")

    test_feature_importance_sums_to_hundred(model, dataset)
    print("TEST 3 PASSED")

    test_top_contributors_returned(model, dataset)
    print("TEST 4 PASSED")

    test_actionable_insights_generated(model, dataset)
    print("TEST 5 PASSED")

    print("ALL EXPLAINABILITY TESTS PASSED")


if __name__ == "__main__":
    main()
