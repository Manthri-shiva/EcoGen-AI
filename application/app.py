"""
EcoGen AI Application Launcher
"""

import streamlit as st

from auth.session import get_current_user
from assessment.assessment_form import show_assessment_form
from assessment.assessment_manager import get_latest_assessment


def run_application():
    """
    Launch the authenticated EcoGen AI application.
    """

    # Logged-in user
    user = get_current_user()

    # Welcome
    st.title("🌍 EcoGen AI")
    st.success(f"Welcome, {user['user_name']} 👋")
    st.write(f"Logged in as **{user['user_email']}**")

    st.markdown("---")

    # Fetch latest assessment
    assessment = get_latest_assessment(user["user_id"])

    # First-time user
    if assessment is None:

        st.info(
            "Complete your first Monthly Sustainability Assessment "
            "to unlock your personalized dashboard."
        )

        show_assessment_form()

        return

    # Dashboard (Version 1)

    st.header("📊 Sustainability Dashboard")

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

    st.subheader("🤖 AI Coach")

    st.success(
        "Excellent progress! Continue reducing electricity usage "
        "to further improve your sustainability score."
    )

    st.markdown("---")

    if st.button("Run New Monthly Assessment"):

        show_assessment_form()