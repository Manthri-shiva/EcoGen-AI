"""
EcoGen AI - Sustainability Advisor Logic

This module keeps the Gemini-based recommendation logic separate from the UI.
It provides prompt creation, API interaction, and response formatting utilities.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List
from urllib import error, request


API_KEY_ENV_KEYS = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def build_sustainability_prompt(inputs: Dict[str, Any]) -> str:
    """
    Build a prompt that instructs Gemini to return structured sustainability advice.
    """
    electricity = float(inputs.get("monthly_electricity_usage", 0))
    water = float(inputs.get("monthly_water_consumption", 0))
    travel = float(inputs.get("daily_travel_distance", 0))
    waste = float(inputs.get("monthly_waste_generated", 0))
    score = float(inputs.get("sustainability_score", 0))

    return f"""
You are EcoGen AI, a sustainability advisor.

Analyze the following user profile and give practical recommendations.

Inputs:
- Monthly Electricity Usage: {electricity} units
- Monthly Water Consumption: {water} liters
- Daily Travel Distance: {travel} km
- Monthly Waste Generated: {waste} kg
- Sustainability Score: {score} / 100

Requirements:
1. Provide exactly 5 recommendations.
2. Focus on energy, water, transport, and waste.
3. Assign a priority level of High, Medium, or Low for each recommendation.
4. Include expected environmental impact and estimated monthly cost savings.
5. Return valid JSON only.

JSON format:
{{
  "summary": "short summary of the user profile",
  "expected_environmental_impact": "brief explanation",
  "estimated_cost_savings": "$X to $Y per month",
  "recommendations": [
    {{
      "rank": 1,
      "category": "Energy",
      "recommendation": "clear action",
      "priority": "High",
      "expected_impact": "brief impact note",
      "estimated_cost_savings": "$X"
    }}
  ]
}}
"""


def get_gemini_response(
    prompt: str,
    api_key: str | None = None,
) -> str:
    """
    Call the Gemini API using environment variables for authentication.
    Returns the raw response text.
    """
    key = api_key or next((os.getenv(k) for k in API_KEY_ENV_KEYS if os.getenv(k)), None)

    if not key:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment."
        )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.45,
            "topP": 0.85,
            "maxOutputTokens": 1000,
        },
    }

    data = json.dumps(payload).encode("utf-8")
    endpoint = f"{MODEL_URL}?key={key}"

    req = request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API request failed: {detail}") from exc
    except Exception as exc:  # pragma: no cover - defensive handling
        raise RuntimeError(f"Failed to communicate with Gemini API: {exc}") from exc

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected Gemini response format.") from exc


def format_recommendations(raw_response: str) -> Dict[str, Any]:
    """
    Parse Gemini output into a clean structure for the UI.
    """
    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: try to extract the first JSON object if the model adds text.
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            parsed = json.loads(cleaned[start : end + 1])
        else:
            parsed = {
                "summary": "AI advisor response is unavailable.",
                "expected_environmental_impact": "Please try again.",
                "estimated_cost_savings": "$0",
                "recommendations": [],
            }

    recommendations = parsed.get("recommendations", [])
    if not isinstance(recommendations, list):
        recommendations = []

    normalized_recommendations: List[Dict[str, Any]] = []

    for index, item in enumerate(recommendations[:5], start=1):
        if not isinstance(item, dict):
            continue
        normalized_recommendations.append(
            {
                "rank": int(item.get("rank", index)),
                "category": str(item.get("category", "General")),
                "recommendation": str(item.get("recommendation", "No recommendation provided.")),
                "priority": str(item.get("priority", "Medium")),
                "expected_impact": str(
                    item.get("expected_impact", "Positive sustainability impact")
                ),
                "estimated_cost_savings": str(
                    item.get("estimated_cost_savings", "$0")
                ),
            }
        )

    return {
        "summary": str(parsed.get("summary", "AI-generated sustainability guidance.")),
        "expected_environmental_impact": str(
            parsed.get(
                "expected_environmental_impact",
                "Potential improvement in energy, water, and waste efficiency.",
            )
        ),
        "estimated_cost_savings": str(
            parsed.get("estimated_cost_savings", "$0 to $50 per month")
        ),
        "recommendations": normalized_recommendations,
    }


def generate_advice_report(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the final advisory report by combining prompt creation and formatting.
    """
    prompt = build_sustainability_prompt(inputs)
    raw_response = get_gemini_response(prompt)
    return format_recommendations(raw_response)
