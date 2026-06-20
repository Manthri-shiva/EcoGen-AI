from genai.advisor.sustainability_advisor import (
    generate_advisor_report,
    generate_monthly_plan,
    generate_priority_actions,
    generate_sustainability_advice,
    generate_user_summary,
    generate_weekly_plan,
)


def _sample_inputs():
    return {
        "age": 25,
        "family_size": 4,
        "location": "Hyderabad",
        "carbon_footprint": 1742,
        "sustainability_score": 62,
        "top_contributors": [
            "electricity_bill",
            "daily_travel_km",
            "waste_generated",
        ],
    }


def test_user_summary_generation() -> None:
    inputs = _sample_inputs()
    summary = generate_user_summary(
        age=inputs["age"],
        family_size=inputs["family_size"],
        location=inputs["location"],
        carbon_footprint=inputs["carbon_footprint"],
        sustainability_score=inputs["sustainability_score"],
        top_contributors=inputs["top_contributors"],
    )

    assert "Age: 25" in summary
    assert "Location: Hyderabad" in summary
    assert "Carbon Footprint: 1742 kg CO2" in summary


def test_sustainability_advice_generation() -> None:
    inputs = _sample_inputs()
    advice = generate_sustainability_advice(
        carbon_footprint=inputs["carbon_footprint"],
        sustainability_score=inputs["sustainability_score"],
        top_contributors=inputs["top_contributors"],
        location=inputs["location"],
    )

    assert "largest contributor" in advice
    assert "Hyderabad" in advice


def test_priority_action_generation() -> None:
    inputs = _sample_inputs()
    actions = generate_priority_actions(
        top_contributors=inputs["top_contributors"],
        sustainability_score=inputs["sustainability_score"],
    )

    assert isinstance(actions, dict)
    assert "high_priority" in actions
    assert "medium_priority" in actions
    assert "low_priority" in actions
    assert actions["high_priority"]


def test_weekly_plan_generation() -> None:
    inputs = _sample_inputs()
    plan = generate_weekly_plan(
        top_contributors=inputs["top_contributors"],
        sustainability_score=inputs["sustainability_score"],
    )

    assert len(plan) == 4
    assert all("week" in item and "tasks" in item for item in plan)


def test_monthly_plan_generation() -> None:
    inputs = _sample_inputs()
    plan = generate_monthly_plan(
        top_contributors=inputs["top_contributors"],
        sustainability_score=inputs["sustainability_score"],
    )

    assert len(plan) == 3
    assert all("month" in item and "actions" in item for item in plan)


def test_advisor_report_generation() -> None:
    inputs = _sample_inputs()
    report = generate_advisor_report(
        age=inputs["age"],
        family_size=inputs["family_size"],
        location=inputs["location"],
        carbon_footprint=inputs["carbon_footprint"],
        sustainability_score=inputs["sustainability_score"],
        top_contributors=inputs["top_contributors"],
    )

    assert isinstance(report, dict)
    assert "user_summary" in report
    assert "advisor_message" in report
    assert "priority_actions" in report
    assert "weekly_plan" in report
    assert "monthly_plan" in report


def main() -> None:
    test_user_summary_generation()
    print("TEST 1 PASSED")

    test_sustainability_advice_generation()
    print("TEST 2 PASSED")

    test_priority_action_generation()
    print("TEST 3 PASSED")

    test_weekly_plan_generation()
    print("TEST 4 PASSED")

    test_monthly_plan_generation()
    print("TEST 5 PASSED")

    test_advisor_report_generation()
    print("TEST 6 PASSED")

    print("ALL ADVISOR TESTS PASSED")


if __name__ == "__main__":
    main()
