from ml.recommendations.recommendation_engine import generate_personalized_plan


def _count_priorities(plan: dict) -> dict:
    priorities = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for category_recs in plan["recommendations"].values():

        for rec in category_recs:

            priority = rec.get(
                "priority",
                "LOW"
            )

            if priority in priorities:
                priorities[priority] += 1

    return priorities


def _print_results(
    test_name: str,
    plan: dict,
    priorities: dict
) -> None:

    print("\n" + "=" * 60)
    print(test_name)
    print("=" * 60)

    print(
        f"Sustainability Score: "
        f"{plan['sustainability_score']}"
    )

    print(
        f"Predicted Carbon Footprint: "
        f"{plan['predicted_carbon_footprint']} kg CO2"
    )

    print(
        f"Estimated Reduction Potential: "
        f"{plan['estimated_total_reduction_percent']}%"
    )

    print("\nRecommendation Priorities:")

    for level in ["HIGH", "MEDIUM", "LOW"]:

        print(
            f"{level}: "
            f"{priorities[level]}"
        )

    print()


def test_low_consumption_user():

    plan = generate_personalized_plan(
        electricity_bill=800,
        water_usage=150,
        daily_travel_km=5,
        waste_generated=5,
        sustainability_score=90,
        predicted_carbon_footprint=700,
    )

    priorities = _count_priorities(plan)

    _print_results(
        "TEST 1 - LOW CONSUMPTION USER",
        plan,
        priorities
    )

    assert priorities["LOW"] >= priorities["MEDIUM"]
    assert priorities["LOW"] >= priorities["HIGH"]

    return True


def test_medium_consumption_user():

    plan = generate_personalized_plan(
        electricity_bill=2000,
        water_usage=500,
        daily_travel_km=30,
        waste_generated=25,
        sustainability_score=65,
        predicted_carbon_footprint=1500,
    )

    priorities = _count_priorities(plan)

    _print_results(
        "TEST 2 - MEDIUM CONSUMPTION USER",
        plan,
        priorities
    )

    assert priorities["MEDIUM"] >= priorities["LOW"]
    assert priorities["MEDIUM"] >= priorities["HIGH"]

    return True


def test_high_consumption_user():

    plan = generate_personalized_plan(
        electricity_bill=4500,
        water_usage=900,
        daily_travel_km=80,
        waste_generated=70,
        sustainability_score=40,
        predicted_carbon_footprint=3000,
    )

    priorities = _count_priorities(plan)

    _print_results(
        "TEST 3 - HIGH CONSUMPTION USER",
        plan,
        priorities
    )

    assert priorities["HIGH"] >= priorities["MEDIUM"]
    assert priorities["HIGH"] >= priorities["LOW"]

    return True


if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("ECOGEN AI - RECOMMENDATION ENGINE TEST SUITE")
    print("=" * 60)

    try:

        test_low_consumption_user()

        test_medium_consumption_user()

        test_high_consumption_user()

        print("=" * 60)
        print("ALL TESTS PASSED")
        print("=" * 60)

    except AssertionError:

        print("=" * 60)
        print("TEST FAILED")
        print("=" * 60)

    except Exception as error:

        print("=" * 60)
        print(f"ERROR: {error}")
        print("=" * 60)