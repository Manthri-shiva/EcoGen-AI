"""
Monthly Sustainability Assessment Form
"""

import streamlit as st

from auth.session import get_current_user
from assessment.assessment_manager import process_assessment


def show_assessment_form():
    """
    Display the monthly sustainability assessment form.

    Returns
    -------
    dict | None
        Analysis results if submitted successfully,
        otherwise None.
    """

    user = get_current_user()

    st.title("🌱 Monthly Sustainability Assessment")

    st.caption(
        "Enter your sustainability data for this month. "
        "EcoGen AI will automatically analyze your environmental impact."
    )

    with st.form("assessment_form"):

        electricity = st.number_input(
            "Monthly Electricity Usage (kWh)",
            min_value=0.0,
            value=250.0,
            step=10.0,
        )

        water = st.number_input(
            "Monthly Water Usage (Liters)",
            min_value=0.0,
            value=8000.0,
            step=100.0,
        )

        travel = st.number_input(
            "Average Daily Travel Distance (km)",
            min_value=0.0,
            value=15.0,
            step=1.0,
        )

        waste = st.number_input(
            "Monthly Waste Generated (kg)",
            min_value=0.0,
            value=20.0,
            step=1.0,
        )

        submitted = st.form_submit_button("Analyze Sustainability")

    if not submitted:
        return None

    results = process_assessment(
        user_id=user["user_id"],
        electricity_kwh=electricity,
        water_liters=water,
        travel_km=travel,
        waste_kg=waste,
    )

    st.success("✅ Sustainability assessment completed successfully!")

    st.subheader("Assessment Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Carbon Footprint",
            f"{results['carbon_footprint']:.2f} kg CO₂",
        )

        st.metric(
            "Sustainability Score",
            f"{results['sustainability_score']:.1f}",
        )

    with col2:
        st.metric(
            "EcoDNA",
            results["eco_dna"],
        )

        st.metric(
            "Journey Level",
            results["journey_level"],
        )

    st.metric(
        "Reward Points",
        results["reward_points"],
    )

    return results