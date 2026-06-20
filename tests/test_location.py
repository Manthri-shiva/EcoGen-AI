from ml.location.location_engine import (
    generate_location_insights,
    generate_location_recommendations,
    generate_location_report,
    get_location_profile,
    load_location_profiles,
)


def test_profiles_load() -> None:
    profiles = load_location_profiles()
    assert isinstance(profiles, dict)
    assert profiles


def test_hyderabad_profile() -> None:
    profile = get_location_profile("Hyderabad")
    assert isinstance(profile, dict)
    assert profile["solar_potential"] == "HIGH"
    assert profile["water_scarcity"] == "HIGH"


def test_recommendations_generated() -> None:
    recommendations = generate_location_recommendations("Bengaluru")
    assert isinstance(recommendations, list)
    assert "Metro Usage" in recommendations
    assert "Public Transport" in recommendations


def test_insights_generated() -> None:
    insights = generate_location_insights("Delhi")
    assert isinstance(insights, list)
    assert any("solar" in insight.lower() for insight in insights)
    assert any("water" in insight.lower() for insight in insights)


def test_location_report() -> None:
    report = generate_location_report("Hyderabad")
    assert isinstance(report, dict)
    assert report["city"] == "Hyderabad"
    assert "location_profile" in report
    assert "recommendations" in report
    assert "insights" in report


def test_invalid_city_raises() -> None:
    try:
        get_location_profile("Unknown City")
    except ValueError:
        return
    raise AssertionError("Expected ValueError for unsupported city")


def main() -> None:
    test_profiles_load()
    print("TEST 1 PASSED")

    test_hyderabad_profile()
    print("TEST 2 PASSED")

    test_recommendations_generated()
    print("TEST 3 PASSED")

    test_insights_generated()
    print("TEST 4 PASSED")

    test_location_report()
    print("TEST 5 PASSED")

    test_invalid_city_raises()
    print("TEST 6 PASSED")

    print("ALL LOCATION TESTS PASSED")


if __name__ == "__main__":
    main()
