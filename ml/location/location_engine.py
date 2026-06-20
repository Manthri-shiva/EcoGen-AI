"""Location Intelligence Engine for EcoGen AI.

Provides location-specific sustainability profiles, recommendations, and
human-readable insights for supported Indian cities.
"""

from __future__ import annotations

from typing import Any, Dict, List

CityProfile = Dict[str, str]
CityProfiles = Dict[str, CityProfile]

SUPPORTED_CITY_PROFILES: CityProfiles = {
    "Hyderabad": {
        "solar_potential": "HIGH",
        "public_transport": "MEDIUM",
        "water_scarcity": "HIGH",
        "waste_management": "MEDIUM",
        "air_pollution": "MEDIUM",
    },
    "Bengaluru": {
        "solar_potential": "HIGH",
        "public_transport": "HIGH",
        "water_scarcity": "MEDIUM",
        "waste_management": "MEDIUM",
        "air_pollution": "MEDIUM",
    },
    "Chennai": {
        "solar_potential": "HIGH",
        "public_transport": "MEDIUM",
        "water_scarcity": "MEDIUM",
        "waste_management": "MEDIUM",
        "air_pollution": "MEDIUM",
    },
    "Mumbai": {
        "solar_potential": "MEDIUM",
        "public_transport": "HIGH",
        "water_scarcity": "LOW",
        "waste_management": "HIGH",
        "air_pollution": "HIGH",
    },
    "Delhi": {
        "solar_potential": "HIGH",
        "public_transport": "HIGH",
        "water_scarcity": "HIGH",
        "waste_management": "MEDIUM",
        "air_pollution": "HIGH",
    },
    "Pune": {
        "solar_potential": "HIGH",
        "public_transport": "MEDIUM",
        "water_scarcity": "MEDIUM",
        "waste_management": "MEDIUM",
        "air_pollution": "MEDIUM",
    },
    "Kolkata": {
        "solar_potential": "MEDIUM",
        "public_transport": "MEDIUM",
        "water_scarcity": "MEDIUM",
        "waste_management": "MEDIUM",
        "air_pollution": "HIGH",
    },
}


def load_location_profiles() -> CityProfiles:
    """Return built-in location profiles for supported cities."""

    return SUPPORTED_CITY_PROFILES.copy()


def _normalize_city(city: str) -> str:
    """Normalize city name for case-insensitive lookup."""

    if not isinstance(city, str):
        raise TypeError("City name must be a string.")

    normalized = city.strip().title()
    alias_map = {
        "Bengaluru": "Bengaluru",
        "Bangalore": "Bengaluru",
        "Chennai": "Chennai",
        "Hyderabad": "Hyderabad",
        "Mumbai": "Mumbai",
        "Bombay": "Mumbai",
        "Delhi": "Delhi",
        "Pune": "Pune",
        "Poona": "Pune",
        "Kolkata": "Kolkata",
        "Calcutta": "Kolkata",
    }

    return alias_map.get(normalized, normalized)


def get_location_profile(city: str) -> CityProfile:
    """Return profile for the provided city, raising ValueError if unsupported."""

    normalized_city = _normalize_city(city)
    profiles = load_location_profiles()

    if normalized_city not in profiles:
        raise ValueError(
            f"City '{city}' is not supported. Supported cities: {', '.join(sorted(profiles))}."
        )

    return profiles[normalized_city].copy()


def _recommendations_for_solar_potential(profile: CityProfile) -> List[str]:
    recommendations: List[str] = []

    if profile["solar_potential"] == "HIGH":
        recommendations.extend(
            [
                "Rooftop Solar",
                "Solar Water Heating",
                "Renewable Energy Adoption",
            ]
        )

    return recommendations


def _recommendations_for_public_transport(profile: CityProfile) -> List[str]:
    recommendations: List[str] = []

    if profile["public_transport"] == "HIGH":
        recommendations.extend(
            [
                "Metro Usage",
                "Public Transport",
                "Carpooling",
            ]
        )

    return recommendations


def _recommendations_for_water_scarcity(profile: CityProfile) -> List[str]:
    recommendations: List[str] = []

    if profile["water_scarcity"] == "HIGH":
        recommendations.extend(
            [
                "Rainwater Harvesting",
                "Water Conservation",
                "Grey Water Reuse",
            ]
        )

    return recommendations


def _recommendations_for_air_pollution(profile: CityProfile) -> List[str]:
    recommendations: List[str] = []

    if profile["air_pollution"] == "HIGH":
        recommendations.extend(
            [
                "Public Transport",
                "EV Adoption",
                "Reduced Private Vehicle Usage",
            ]
        )

    return recommendations


def _recommendations_for_waste_management(profile: CityProfile) -> List[str]:
    recommendations: List[str] = []

    if profile["waste_management"] == "LOW":
        recommendations.extend(
            [
                "Household Composting",
                "Waste Segregation",
                "Community Recycling Programs",
            ]
        )

    return recommendations


def generate_location_recommendations(city: str) -> List[str]:
    """Generate location-specific recommendations for the provided city."""

    profile = get_location_profile(city)
    recommendations: List[str] = []

    recommendations.extend(_recommendations_for_solar_potential(profile))
    recommendations.extend(_recommendations_for_public_transport(profile))
    recommendations.extend(_recommendations_for_water_scarcity(profile))
    recommendations.extend(_recommendations_for_air_pollution(profile))
    recommendations.extend(_recommendations_for_waste_management(profile))

    return list(dict.fromkeys(recommendations))


def generate_location_insights(city: str) -> List[str]:
    """Generate human-readable insights for the provided city."""

    profile = get_location_profile(city)
    insights: List[str] = []

    if profile["solar_potential"] == "HIGH":
        insights.append(
            f"{city.title()} has excellent solar energy potential."
        )
    elif profile["solar_potential"] == "MEDIUM":
        insights.append(
            f"{city.title()} has moderate solar potential that can still support rooftop solutions."
        )
    else:
        insights.append(
            f"{city.title()} has lower solar potential, so optimize other renewable options."
        )

    if profile["water_scarcity"] == "HIGH":
        insights.append(
            "Water conservation should be prioritized in this city."
        )
    elif profile["water_scarcity"] == "MEDIUM":
        insights.append(
            "Water efficiency measures are recommended."
        )
    else:
        insights.append(
            "Water availability is relatively stable, but conservation remains valuable."
        )

    if profile["air_pollution"] == "HIGH":
        insights.append(
            "Air quality concerns make low-emission transport a priority."
        )
    elif profile["air_pollution"] == "MEDIUM":
        insights.append(
            "Improving commuter choices can help manage air pollution."
        )
    else:
        insights.append(
            "Air quality is comparatively better, though sustainable travel still matters."
        )

    if profile["waste_management"] == "LOW":
        insights.append(
            "Waste management improvements are needed to reduce environmental impact."
        )
    else:
        insights.append(
            "Existing waste management systems can be reinforced with better recycling."
        )

    if profile["public_transport"] == "HIGH":
        insights.append(
            "Strong public transport infrastructure supports low-carbon commuting."
        )
    else:
        insights.append(
            "Investing in shared travel options can improve mobility and lower emissions."
        )

    return insights


def generate_location_report(city: str) -> Dict[str, Any]:
    """Generate a location intelligence report for the given city."""

    profile = get_location_profile(city)
    recommendations = generate_location_recommendations(city)
    insights = generate_location_insights(city)

    return {
        "city": city.title(),
        "location_profile": profile,
        "recommendations": recommendations,
        "insights": insights,
    }


if __name__ == "__main__":
    city_name = "Hyderabad"
    report = generate_location_report(city_name)

    print(f"City: {report['city']}\n")
    print("Location Profile:")
    for key, value in report["location_profile"].items():
        formatted_key = key.replace("_", " ").title()
        print(f"- {formatted_key}: {value}")

    print("\nInsights:")
    for insight in report["insights"]:
        print(f"- {insight}")

    print("\nRecommendations:")
    for recommendation in report["recommendations"]:
        print(f"- {recommendation}")
