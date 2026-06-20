"""GenAI Sustainability Advisor for EcoGen AI.

Provides rule-based, natural-language sustainability coaching
without calling external LLM APIs.
"""

from __future__ import annotations

from typing import Any, Dict, List

FeatureList = List[str]
PriorityActions = Dict[str, List[str]]
WeeklyPlan = List[Dict[str, Any]]
MonthlyPlan = List[Dict[str, Any]]

_LOCATION_CONTEXT: Dict[str, str] = {
    "Hyderabad": "excellent solar potential",
    "Bengaluru": "strong public transport and solar potential",
    "Chennai": "coastal climate and growing renewable energy adoption",
    "Mumbai": "robust mass transit and high air pollution awareness",
    "Delhi": "high pollution challenges and strong public mobility systems",
    "Pune": "good rooftop solar potential and manageable water risks",
    "Kolkata": "high air pollution focus and stable urban infrastructure",
}

_FEATURE_LABELS: Dict[str, str] = {
    "electricity_bill": "electricity usage",
    "daily_travel_km": "transportation",
    "waste_generated": "waste generation",
    "water_usage": "water usage",
    "family_size": "household size",
    "age": "age",
}


def _normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    return text.strip().title()


def _describe_top_contributor(top_contributor: str) -> str:
    return _FEATURE_LABELS.get(top_contributor, top_contributor.replace("_", " "))


def generate_user_summary(
    age: int,
    family_size: int,
    location: str,
    carbon_footprint: float,
    sustainability_score: float,
    top_contributors: FeatureList,
) -> str:
    """Generate a human-readable summary of the user's sustainability profile."""

    if age < 0 or family_size < 0:
        raise ValueError("Age and family size must be non-negative.")

    if carbon_footprint < 0:
        raise ValueError("Carbon footprint must be non-negative.")

    location_normalized = _normalize_text(location)
    top_feature = _describe_top_contributor(top_contributors[0]) if top_contributors else "a key factor"

    return (
        f"Age: {age}\n"
        f"Family Size: {family_size}\n"
        f"Location: {location_normalized}\n"
        f"Carbon Footprint: {carbon_footprint} kg CO2\n"
        f"Sustainability Score: {sustainability_score}\n"
        f"Top Contributor: {top_feature.title()}"
    )


def generate_sustainability_advice(
    carbon_footprint: float,
    sustainability_score: float,
    top_contributors: FeatureList,
    location: str,
) -> str:
    """Generate personalized sustainability advice from analytical inputs."""

    if carbon_footprint < 0 or sustainability_score < 0:
        raise ValueError("Numeric inputs must be non-negative.")

    location_normalized = _normalize_text(location)
    location_context = _LOCATION_CONTEXT.get(location_normalized, "a location with sustainability opportunities")
    top_message = ""

    if top_contributors:
        top_feature = _describe_top_contributor(top_contributors[0])
        top_message = (
            f"Your {top_feature} is the largest contributor to your carbon footprint. "
            f"In {location_normalized}, {location_context}, so focusing there can deliver strong impact."
        )
    else:
        top_message = (
            "Your carbon footprint profile highlights several areas for improvement. "
            "Focus on energy, mobility, water, and waste to improve sustainability."
        )

    advice_parts = [
        top_message,
        "Reducing electricity consumption, choosing low-emission transport, and improving waste habits are practical steps.",
    ]

    if sustainability_score < 50:
        advice_parts.append(
            "Since your sustainability score is below average, start with high-priority energy and transport actions."
        )
    elif sustainability_score < 75:
        advice_parts.append(
            "Your sustainability score is moderate; build momentum with consistent weekly improvements."
        )
    else:
        advice_parts.append(
            "Your sustainability score is strong; focus on long-term habits to sustain progress."
        )

    return "\n\n".join(advice_parts)


def generate_priority_actions(
    top_contributors: FeatureList,
    sustainability_score: float,
) -> PriorityActions:
    """Generate prioritized actions grouped by importance."""

    if sustainability_score < 0:
        raise ValueError("Sustainability score must be non-negative.")

    actions: PriorityActions = {
        "high_priority": [],
        "medium_priority": [],
        "low_priority": [],
    }

    contributor_actions = {
        "electricity_bill": [
            "Reduce electricity usage by switching off unused appliances.",
            "Install LED lighting and energy-efficient devices.",
        ],
        "daily_travel_km": [
            "Use public transport, cycling, or carpooling for daily commutes.",
            "Limit private vehicle usage when possible.",
        ],
        "waste_generated": [
            "Start waste segregation at home.",
            "Reuse and recycle materials before disposal.",
        ],
        "water_usage": [
            "Measure daily water consumption and fix leaks promptly.",
            "Use water-saving fixtures and reuse greywater.",
        ],
        "family_size": [
            "Coordinate resource sharing and reduce household waste.",
            "Adopt efficient cooking and laundry routines.",
        ],
        "age": [
            "Build lasting sustainability habits through small daily changes.",
        ],
    }

    for contributor in top_contributors:
        contributor = contributor.strip()
        actions_for_feature = contributor_actions.get(contributor, [])

        for index, action in enumerate(actions_for_feature):
            if index == 0:
                actions["high_priority"].append(action)
            elif index == 1:
                actions["medium_priority"].append(action)
            else:
                actions["low_priority"].append(action)

    if sustainability_score < 60:
        actions["high_priority"].append(
            "Set a weekly sustainability target and track progress."
        )
    else:
        actions["medium_priority"].append(
            "Continue reviewing your sustainability habits monthly."
        )

    if not actions["high_priority"]:
        actions["high_priority"].append(
            "Start with energy-efficient lighting and smarter daily travel choices."
        )

    if not actions["medium_priority"]:
        actions["medium_priority"].extend(
            [
                "Improve waste segregation at home.",
                "Monitor water consumption regularly.",
            ]
        )

    if not actions["low_priority"]:
        actions["low_priority"].append(
            "Participate in local sustainability initiatives or community clean-ups."
        )

    actions["high_priority"] = list(dict.fromkeys(actions["high_priority"]))
    actions["medium_priority"] = list(dict.fromkeys(actions["medium_priority"]))
    actions["low_priority"] = list(dict.fromkeys(actions["low_priority"]))

    return actions


def generate_weekly_plan(
    top_contributors: FeatureList,
    sustainability_score: float,
) -> WeeklyPlan:
    """Generate a four-week sustainability action plan."""

    if sustainability_score < 0:
        raise ValueError("Sustainability score must be non-negative.")

    weekly_plan: WeeklyPlan = [
        {
            "week": "Week 1",
            "tasks": [
                "Replace inefficient bulbs with LEDs.",
                "Measure daily electricity usage and note high-consumption periods.",
            ],
        },
        {
            "week": "Week 2",
            "tasks": [
                "Begin waste segregation and recycle household materials.",
                "Track water usage and reduce unnecessary consumption.",
            ],
        },
        {
            "week": "Week 3",
            "tasks": [
                "Explore solar installation options or energy-efficient upgrades.",
                "Try public transport or carpooling for several days.",
            ],
        },
        {
            "week": "Week 4",
            "tasks": [
                "Review sustainability progress and note improvements.",
                "Plan the next month with energy, transport, water, and waste goals.",
            ],
        },
    ]

    if "electricity_bill" in top_contributors:
        weekly_plan[0]["tasks"].append(
            "Use a power meter or smart plug to identify wasteful devices."
        )

    if "daily_travel_km" in top_contributors:
        weekly_plan[2]["tasks"].append(
            "Map alternate low-emission travel routes and test one this week."
        )

    if "waste_generated" in top_contributors:
        weekly_plan[1]["tasks"].append(
            "Create a compost bin or schedule recycling pickups."
        )

    return weekly_plan


def generate_monthly_plan(
    top_contributors: FeatureList,
    sustainability_score: float,
) -> MonthlyPlan:
    """Generate a three-month sustainability improvement plan."""

    if sustainability_score < 0:
        raise ValueError("Sustainability score must be non-negative.")

    monthly_plan: MonthlyPlan = [
        {
            "month": "Month 1",
            "focus": "Energy Optimization",
            "actions": [
                "Audit home energy use and replace inefficient appliances.",
                "Install LED lighting and smart power strips.",
            ],
        },
        {
            "month": "Month 2",
            "focus": "Transportation Improvements",
            "actions": [
                "Increase public transport or carpooling use.",
                "Reduce private vehicle trips and choose active travel when possible.",
            ],
        },
        {
            "month": "Month 3",
            "focus": "Water and Waste Conservation",
            "actions": [
                "Implement water-saving fixtures and reuse greywater where safe.",
                "Enhance waste segregation and compost organic materials.",
            ],
        },
    ]

    if "water_usage" in top_contributors:
        monthly_plan[2]["actions"].append(
            "Adopt a household water reduction challenge."
        )

    if "waste_generated" in top_contributors:
        monthly_plan[2]["actions"].append(
            "Organize a home recycling plan and reduce single-use products."
        )

    return monthly_plan


def generate_advisor_report(
    age: int,
    family_size: int,
    location: str,
    carbon_footprint: float,
    sustainability_score: float,
    top_contributors: FeatureList,
) -> Dict[str, Any]:
    """Generate a comprehensive advisor report for the user."""

    user_summary = generate_user_summary(
        age=age,
        family_size=family_size,
        location=location,
        carbon_footprint=carbon_footprint,
        sustainability_score=sustainability_score,
        top_contributors=top_contributors,
    )

    advisor_message = generate_sustainability_advice(
        carbon_footprint=carbon_footprint,
        sustainability_score=sustainability_score,
        top_contributors=top_contributors,
        location=location,
    )

    priority_actions = generate_priority_actions(
        top_contributors=top_contributors,
        sustainability_score=sustainability_score,
    )

    weekly_plan = generate_weekly_plan(
        top_contributors=top_contributors,
        sustainability_score=sustainability_score,
    )

    monthly_plan = generate_monthly_plan(
        top_contributors=top_contributors,
        sustainability_score=sustainability_score,
    )

    return {
        "user_summary": user_summary,
        "advisor_message": advisor_message,
        "priority_actions": priority_actions,
        "weekly_plan": weekly_plan,
        "monthly_plan": monthly_plan,
    }


if __name__ == "__main__":
    age = 25
    family_size = 4
    location = "Hyderabad"
    carbon_footprint = 1742
    sustainability_score = 62
    top_contributors = [
        "electricity_bill",
        "daily_travel_km",
        "waste_generated",
    ]

    report = generate_advisor_report(
        age=age,
        family_size=family_size,
        location=location,
        carbon_footprint=carbon_footprint,
        sustainability_score=sustainability_score,
        top_contributors=top_contributors,
    )

    print("User Summary")
    print(report["user_summary"])
    print("\nAdvisor Insights")
    print(report["advisor_message"])

    print("\nPriority Actions")
    for priority, actions in report["priority_actions"].items():
        print(f"\n{priority.replace('_', ' ').title()}")
        for action in actions:
            print(f"- {action}")

    print("\nWeekly Plan")
    for week in report["weekly_plan"]:
        print(f"\n{week['week']}")
        for task in week["tasks"]:
            print(f"- {task}")

    print("\nMonthly Plan")
    for month in report["monthly_plan"]:
        print(f"\n{month['month']} - {month['focus']}")
        for action in month["actions"]:
            print(f"- {action}")

    print("\n" + "=" * 50)
