"""
EcoGen AI - 30-Day Green Action Planner

This module contains the business logic for generating a personalized
30-day sustainability action plan using Gemini and reusable planning helpers.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error, request


API_KEY_ENV_KEYS = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def _validate_number(value: Any, name: str) -> float:
    """Convert a value to float and raise a clear error if invalid."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a numeric value.") from exc


def build_action_plan_prompt(inputs: Dict[str, Any]) -> str:
    """Build a prompt instructing Gemini to return a structured 4-week plan."""
    sustainability_score = _validate_number(
        inputs.get("sustainability_score", 0), "sustainability_score"
    )
    monthly_carbon = _validate_number(
        inputs.get("monthly_carbon_footprint", 0), "monthly_carbon_footprint"
    )
    monthly_electricity = _validate_number(
        inputs.get("monthly_electricity_usage", 0), "monthly_electricity_usage"
    )
    monthly_water = _validate_number(
        inputs.get("monthly_water_consumption", 0), "monthly_water_consumption"
    )
    goal = inputs.get("sustainability_goal", "Reduce environmental impact")

    return f"""
You are EcoGen AI, a sustainability planning assistant.
Create a personalized 30-day green action plan for the user.

User inputs:
- Sustainability Score: {sustainability_score}
- Monthly Carbon Footprint: {monthly_carbon} kg CO2
- Monthly Electricity Usage: {monthly_electricity} units
- Monthly Water Consumption: {monthly_water} liters
- Sustainability Goal: {goal}

Rules:
1. Return valid JSON only.
2. Provide exactly 4 weekly sections: Week 1, Week 2, Week 3, and Week 4.
3. For each week, include:
   - tasks: a list of actionable task strings
   - expected_carbon_reduction: a short phrase or number with units
   - expected_cost_savings: a short phrase or number with currency
   - difficulty_level: Easy, Medium, or Hard
   - priority: High, Medium, or Low
4. Add a summary section with:
   - total_expected_reduction
   - total_expected_savings
   - main_focus
5. Make recommendations practical, specific, and tailored to the user's goal.

JSON format:
{{
  "summary": {{
    "total_expected_reduction": "X% reduction",
    "total_expected_savings": "$Y to $Z",
    "main_focus": "primary theme"
  }},
  "weeks": [
    {{
      "week": 1,
      "title": "Week 1 Goals",
      "tasks": ["task 1", "task 2"],
      "expected_carbon_reduction": "5-7%",
      "expected_cost_savings": "$10 to $20",
      "difficulty_level": "Easy",
      "priority": "High"
    }}
  ]
}}
"""


def _call_gemini(prompt: str, api_key: Optional[str] = None) -> str:
    """Send a prompt to the Gemini API and return the raw response text."""
    key = api_key or next((os.getenv(k) for k in API_KEY_ENV_KEYS if os.getenv(k)), None)

    if not key:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment."
        )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.5,
            "topP": 0.85,
            "maxOutputTokens": 1400,
        },
    }

    request_data = json.dumps(payload).encode("utf-8")
    endpoint = f"{MODEL_URL}?key={key}"

    req = request.Request(
        endpoint,
        data=request_data,
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


def _normalize_plan(raw_response: str) -> Dict[str, Any]:
    """Parse Gemini output and normalize it into a consistent structure."""
    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            parsed = json.loads(cleaned[start : end + 1])
        else:
            parsed = {"summary": {}, "weeks": []}

    summary = parsed.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}

    weeks = parsed.get("weeks", [])
    if not isinstance(weeks, list):
        weeks = []

    normalized_weeks: List[Dict[str, Any]] = []

    for index, week in enumerate(weeks[:4], start=1):
        if not isinstance(week, dict):
            continue
        tasks = week.get("tasks", [])
        if not isinstance(tasks, list):
            tasks = []
        normalized_weeks.append(
            {
                "week": int(week.get("week", index)),
                "title": str(week.get("title", f"Week {index} Goals")),
                "tasks": [str(task) for task in tasks if str(task).strip()],
                "expected_carbon_reduction": str(
                    week.get("expected_carbon_reduction", "0-3%")
                ),
                "expected_cost_savings": str(
                    week.get("expected_cost_savings", "$0 to $5")
                ),
                "difficulty_level": str(
                    week.get("difficulty_level", "Medium")
                ),
                "priority": str(week.get("priority", "Medium")),
            }
        )

    while len(normalized_weeks) < 4:
        normalized_weeks.append(
            {
                "week": len(normalized_weeks) + 1,
                "title": f"Week {len(normalized_weeks) + 1} Goals",
                "tasks": [
                    "Review progress and identify one quick win.",
                    "Track energy, water, and waste habits daily.",
                ],
                "expected_carbon_reduction": "2-4%",
                "expected_cost_savings": "$5 to $10",
                "difficulty_level": "Easy",
                "priority": "Medium",
            }
        )

    return {
        "summary": {
            "total_expected_reduction": str(
                summary.get(
                    "total_expected_reduction",
                    "8-12% total reduction",
                )
            ),
            "total_expected_savings": str(
                summary.get(
                    "total_expected_savings",
                    "$25 to $40",
                )
            ),
            "main_focus": str(
                summary.get(
                    "main_focus",
                    "Daily sustainability habit building",
                )
            ),
        },
        "weeks": normalized_weeks,
    }


def generate_action_plan(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a personalized 30-day green action plan.

    If Gemini is unavailable, automatically return
    a high-quality local fallback plan.
    """

    prompt = build_action_plan_prompt(inputs)

    def _fallback_plan():
        return {
            "summary": {
                "total_expected_reduction": "10-15%",
                "total_expected_savings": "$30-$60",
                "main_focus": "Build sustainable daily habits",
            },
            "weeks": [
                {
                    "week": 1,
                    "title": "Week 1 - Energy Awareness",
                    "tasks": [
                        "Replace unnecessary lights with LEDs",
                        "Switch off appliances when not in use",
                        "Track daily electricity consumption",
                    ],
                    "expected_carbon_reduction": "3%",
                    "expected_cost_savings": "$8",
                    "difficulty_level": "Easy",
                    "priority": "High",
                },
                {
                    "week": 2,
                    "title": "Week 2 - Water Conservation",
                    "tasks": [
                        "Reduce shower duration",
                        "Fix leaking taps",
                        "Reuse water where possible",
                    ],
                    "expected_carbon_reduction": "2%",
                    "expected_cost_savings": "$7",
                    "difficulty_level": "Easy",
                    "priority": "Medium",
                },
                {
                    "week": 3,
                    "title": "Week 3 - Sustainable Transport",
                    "tasks": [
                        "Walk or cycle twice this week",
                        "Use public transport",
                        "Avoid unnecessary car trips",
                    ],
                    "expected_carbon_reduction": "4%",
                    "expected_cost_savings": "$15",
                    "difficulty_level": "Medium",
                    "priority": "High",
                },
                {
                    "week": 4,
                    "title": "Week 4 - Waste Reduction",
                    "tasks": [
                        "Recycle household waste",
                        "Avoid single-use plastics",
                        "Start composting organic waste",
                    ],
                    "expected_carbon_reduction": "5%",
                    "expected_cost_savings": "$12",
                    "difficulty_level": "Easy",
                    "priority": "Medium",
                },
            ],
        }

    try:

        raw_response = _call_gemini(prompt)

        plan = _normalize_plan(raw_response)

        if (
            not plan
            or "weeks" not in plan
            or len(plan["weeks"]) == 0
        ):
            return _fallback_plan()

        return plan

    except Exception as exc:

        print(f"Planner AI Error: {exc}")

        return _fallback_plan()

def calculate_progress(
    plan: Dict[str, Any],
    task_status: Optional[Dict[str, bool]] = None,
) -> Dict[str, Any]:
    """
    Calculate completion percentages and weekly progress indicators.

    Parameters:
        plan: normalized planner output
        task_status: mapping of task keys to completion state
    """
    weeks = plan.get("weeks", [])
    task_status = task_status or {}

    weekly_progress: List[Dict[str, Any]] = []
    completed_total = 0
    total_tasks = 0

    for week in weeks:
        week_tasks = week.get("tasks", [])
        total_tasks += len(week_tasks)

        completed = 0
        for index, task in enumerate(week_tasks):
            key = f"{week.get('week', 0)}:{index}"
            if task_status.get(key, False):
                completed += 1

        completed_total += completed

        if len(week_tasks) == 0:
            progress_value = 0
        else:
            progress_value = round((completed / len(week_tasks)) * 100)

        if progress_value >= 100:
            status = "Completed"
        elif progress_value >= 50:
            status = "In Progress"
        else:
            status = "Not Started"

        weekly_progress.append(
            {
                "week": week.get("week", 0),
                "title": week.get("title", f"Week {week.get('week', 0)} Goals"),
                "completed": completed,
                "total": len(week_tasks),
                "progress": progress_value,
                "status": status,
            }
        )

    if total_tasks == 0:
        overall_percentage = 0
    else:
        overall_percentage = round((completed_total / total_tasks) * 100)

    return {
        "overall_percentage": overall_percentage,
        "completed_tasks": completed_total,
        "total_tasks": total_tasks,
        "weekly_progress": weekly_progress,
    }


def estimate_impact(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate the overall impact from the plan by aggregating week metrics.
    """
    weeks = plan.get("weeks", [])
    total_reduction = 0.0
    total_savings = 0.0

    for week in weeks:
        reduction_text = week.get("expected_carbon_reduction", "0%")
        savings_text = week.get("expected_cost_savings", "$0")

        # Extract simple numeric values from text when possible.
        reduction_value = 0.0
        for part in reduction_text.replace("%", "").split():
            try:
                reduction_value = max(reduction_value, float(part))
            except ValueError:
                continue

        savings_value = 0.0
        for part in savings_text.replace("$", "").replace(",", "").split():
            try:
                savings_value = max(savings_value, float(part))
            except ValueError:
                continue

        total_reduction += reduction_value
        total_savings += savings_value

    return {
        "estimated_total_reduction": round(total_reduction, 2),
        "estimated_total_savings": round(total_savings, 2),
    }


def save_plan(plan: Dict[str, Any], file_path: Optional[str] = None) -> str:
    """
    Save a generated plan to disk and return the file path.

    If no file_path is provided, a default file inside the workspace is used.
    """
    if file_path is None:
        output_dir = Path("artifacts")
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = str(output_dir / "green_action_plan.json")

    output_file = Path(file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(plan, file, indent=2, ensure_ascii=False)

    return str(output_file)
