"""
Dashboard Module for EcoGen AI

Displays the authenticated user's sustainability dashboard.
"""

import streamlit as st

from ml.ai_coach import generate_ai_coach_report


def show_dashboard(user, assessment):
    """
    Render the Sustainability Dashboard.
    """

    st.title("🌍 EcoGen AI Dashboard")

    st.success(f"Welcome, {user['user_name']} 👋")

    st.write(f"Logged in as **{user['user_email']}**")

    st.markdown("---")

    st.subheader("📊 Sustainability Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Sustainability Score",
            assessment["sustainability_score"],
        )

        st.metric(
            "Carbon Footprint",
            f"{assessment['carbon_footprint']} kg CO₂",
        )

        st.metric(
            "Reward Points",
            assessment["reward_points"],
        )

    with col2:

        st.metric(
            "EcoDNA",
            assessment["eco_dna"],
        )

        st.metric(
            "Journey Level",
            assessment["journey_level"],
        )

        st.metric(
            "Assessment Date",
            assessment["assessment_date"],
        )

    st.markdown("---")

    coach = generate_ai_coach_report(
        sustainability_score=assessment["sustainability_score"],
        eco_dna=assessment["eco_dna"],
        carbon_footprint=assessment["carbon_footprint"],
        electricity_kwh=assessment["electricity_kwh"],
        water_liters=assessment["water_liters"],
        travel_km=assessment["travel_km"],
        waste_kg=assessment["waste_kg"],
    )

    st.subheader("🤖 AI Coach")

    st.success("### 🌱 Your Strengths")

    if coach["strengths"]:
        for item in coach["strengths"]:
            st.write(f"✅ {item}")
    else:
        st.write("No strengths identified yet.")

    st.warning("### 📈 Areas for Improvement")

    if coach["improvements"]:
        for item in coach["improvements"]:
            st.write(f"⚠️ {item}")
    else:
        st.write("Great job! No major improvements identified.")

    st.info("### 💡 Personalized Recommendations")

    if coach["recommendations"]:
        for item in coach["recommendations"]:
            st.write(f"• {item}")
    else:
        st.write("Keep maintaining your sustainable lifestyle.")

    st.success("### 🎯 Best Action")

    st.write(coach["best_action"])

    st.info(
        f"Estimated Improvement: {coach['estimated_improvement']}"
    )