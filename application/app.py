"""
EcoGen AI Application Controller
"""

import streamlit as st

from auth.session import get_current_user

from assessment.assessment_form import show_assessment_form
from assessment.assessment_manager import get_latest_assessment

from application.navigation import show_navigation
from application.dashboard import show_dashboard


def run_application():
    """
    Launch EcoGen AI after successful authentication.
    """

    user = get_current_user()

    assessment = get_latest_assessment(
        user["user_id"]
    )

    # First-time user
    if assessment is None:

        st.title("🌍 EcoGen AI")

        st.info(
            "Complete your first Monthly Sustainability Assessment."
        )

        show_assessment_form()

        return

    # Sidebar Navigation
    page = show_navigation()

    # Dashboard
    if page == "🏠 Dashboard":

        show_dashboard(
            user,
            assessment,
        )

    # Assessment
    elif page == "📝 Monthly Assessment":

        show_assessment_form()

    # AI Coach
    elif page == "🤖 AI Coach":

        st.title("🤖 AI Coach")

        st.info(
            "The AI Coach is now integrated into the Dashboard."
        )

        show_dashboard(
            user,
            assessment,
        )

    # EcoTwin
    elif page == "🌱 EcoTwin":

        st.title("🌱 EcoTwin")

        st.info(
            "EcoTwin integration will be implemented in Module 6."
        )

    # Reports
    elif page == "📈 Reports":

        st.title("📈 Reports")

        st.info(
            "Reports integration will be implemented in Module 7."
        )

    # Rewards
    elif page == "🏆 Rewards":

        st.title("🏆 Rewards")

        st.info(
            "Rewards integration will be implemented in Module 8."
        )

    # Planner
    elif page == "📅 Green Planner":

        st.title("📅 Green Planner")

        st.info(
            "Planner integration coming soon."
        )

    # Products
    elif page == "🛍 Green Products":

        st.title("🛍 Green Products")

        st.info(
            "Green Products integration coming soon."
        )

    # Community
    elif page == "🌎 Community":

        st.title("🌎 Community")

        st.info(
            "Community Analytics integration coming soon."
        )