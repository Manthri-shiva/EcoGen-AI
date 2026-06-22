"""
EcoGen AI - Sustainability Report Generator

This module creates downloadable sustainability reports in PDF and CSV formats.
It keeps report generation logic separate from the Streamlit UI.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

try:
    from fpdf import FPDF
except ImportError:  # pragma: no cover
    FPDF = None


def create_summary_data() -> Dict[str, Any]:
    """Create sample data that mirrors the dashboard and planner outputs."""
    return {
        "user": {
            "name": "Aarav Sharma",
            "email": "aarav@example.com",
            "location": "Hyderabad",
            "family_size": 4,
        },
        "sustainability_score": 84.5,
        "carbon_footprint_summary": {
            "monthly": 1742,
            "daily": 58,
            "reduction": 18.5,
        },
        "energy_usage_summary": {
            "monthly_usage": 320,
            "cost": 52.0,
            "improvement": 12,
        },
        "water_usage_summary": {
            "monthly_usage": 6500,
            "cost": 35.0,
            "improvement": 9,
        },
        "waste_management_summary": {
            "monthly_waste": 15,
            "recycled": 9,
            "reduction": 7,
        },
        "carbon_reduction_achievements": [
            "Reduced electricity usage by 12%",
            "Improved waste segregation habits",
        ],
        "recommendations": [
            "Use smart thermostats for better energy control.",
            "Install low-flow fixtures to reduce water waste.",
            "Choose public transport for one extra commute weekly.",
        ],
        "planner_progress": {
            "completed_tasks": 18,
            "total_tasks": 24,
            "completion_percentage": 75,
        },
        "rewards": {
            "points": 680,
            "badge": "Eco Warrior",
        },
        "community_contribution": {
            "community_score": 78.6,
            "rank": 4,
        },
    }


def build_report_sections(data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare sections for report generation."""
    completion = data["planner_progress"]["completion_percentage"]
    return {
        "title": "EcoGen AI Sustainability Report",
        "cover_subtitle": "Personal Environmental Impact & Progress Summary",
        "summary_metrics": [
            ("Sustainability Score", f"{data['sustainability_score']:.1f}"),
            ("Monthly Carbon Footprint", f"{data['carbon_footprint_summary']['monthly']} kg"),
            ("Energy Usage", f"{data['energy_usage_summary']['monthly_usage']} units"),
            ("Water Usage", f"{data['water_usage_summary']['monthly_usage']} liters"),
        ],
        "planner_status": (
            f"{completion}% planner completion with {data['planner_progress']['completed_tasks']} "
            f"tasks completed out of {data['planner_progress']['total_tasks']}."
        ),
        "achievement_text": (
            f"Current badge: {data['rewards']['badge']} with {data['rewards']['points']} points."
        ),
    }


def _create_pdf_document(data: Dict[str, Any]) -> bytes:
    """Generate a polished PDF report using FPDF."""
    if FPDF is None:
        raise RuntimeError(
            "FPDF is not installed. Install it with 'pip install fpdf' to generate PDF reports."
        )

    sections = build_report_sections(data)

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.set_text_color(20, 40, 60)
            self.cell(0, 10, sections["title"], 0, 1, "R")
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(128)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()

    # Cover page
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 18, sections["title"], 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(
        0,
        8,
        sections["cover_subtitle"],
        align="C",
    )
    pdf.ln(10)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        7,
        (
            f"Prepared for: {data['user']['name']}\n"
            f"Location: {data['user']['location']}\n"
            f"Email: {data['user']['email']}"
        ),
    )
    pdf.ln(10)

    # Executive summary
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 10, "Executive Summary", 0, 1)
    pdf.ln(2)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)
    for label, value in sections["summary_metrics"]:
        pdf.cell(95, 8, f"{label}: {value}", 1, 0)
        pdf.cell(95, 8, "", 0, 1)

    pdf.ln(5)

    # Recommendations section
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 10, "Recommendations", 0, 1)
    pdf.ln(2)
    pdf.set_font("Arial", "", 11)
    for recommendation in data["recommendations"]:
        pdf.multi_cell(0, 7, f"• {recommendation}")

    pdf.add_page()

    # Achievements and planner progress
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 10, "Achievements & Planner Progress", 0, 1)
    pdf.ln(2)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, sections["planner_status"])
    pdf.multi_cell(0, 7, sections["achievement_text"])

    # Carbon reduction achievements
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Carbon Reduction Achievements", 0, 1)
    pdf.set_font("Arial", "", 11)
    for item in data["carbon_reduction_achievements"]:
        pdf.multi_cell(0, 7, f"• {item}")

    pdf.ln(5)

    # Community contribution
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Community Contribution", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        7,
        (
            f"Community Score: {data['community_contribution']['community_score']:.1f}\n"
            f"Community Rank: #{data['community_contribution']['rank']}"
        ),
    )

    return pdf.output(dest="S")


def generate_pdf_report(data: Dict[str, Any] | None = None) -> bytes:
    """Generate a PDF report from the provided summarized data."""
    report_data = data if data is not None else create_summary_data()
    return _create_pdf_document(report_data)


def generate_csv_report(data: Dict[str, Any] | None = None) -> bytes:
    """Generate a CSV summary from the provided report data."""
    report_data = data if data is not None else create_summary_data()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Section", "Value"])

    writer.writerow(["User Name", report_data["user"]["name"]])
    writer.writerow(["Location", report_data["user"]["location"]])
    writer.writerow(["Sustainability Score", report_data["sustainability_score"]])
    writer.writerow(
        ["Monthly Carbon Footprint", report_data["carbon_footprint_summary"]["monthly"]]
    )
    writer.writerow(
        ["Monthly Energy Usage", report_data["energy_usage_summary"]["monthly_usage"]]
    )
    writer.writerow(
        ["Monthly Water Usage", report_data["water_usage_summary"]["monthly_usage"]]
    )
    writer.writerow(
        ["Monthly Waste", report_data["waste_management_summary"]["monthly_waste"]]
    )
    writer.writerow(
        ["Planner Completion", report_data["planner_progress"]["completion_percentage"]]
    )
    writer.writerow(["Badge", report_data["rewards"]["badge"]])

    return output.getvalue().encode("utf-8")
