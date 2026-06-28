"""
Page Router for EcoGen AI

Routes sidebar navigation to the appropriate application module.
"""

import streamlit as st

from application.dashboard import show_dashboard

from assessment.assessment_form import show_assessment_form


def route_page(page, context):
    """
    Route the selected page.

    Parameters
    ----------
    page : str
        Sidebar selection.

    context : dict
        User context returned by get_user_context().
    """

    user = context["user"]
    assessment = context["assessment"]

    if page == "🏠 Dashboard":

        show_dashboard(
            user,
            assessment,
        )

    elif page == "📝 Monthly Assessment":

        show_assessment_form()

    elif page == "🤖 AI Coach":

        st.title("🤖 AI Coach")

        st.info(
            "The AI Coach is integrated into your Dashboard."
        )

        show_dashboard(
            user,
            assessment,
        )

    elif page == "🌱 EcoTwin":

        st.title("🌱 EcoTwin")

        st.info(
            "EcoTwin integration begins next."
        )

    elif page == "📈 Reports":

        st.title("📈 Reports")

        st.info(
            "Reports module coming soon."
        )

    elif page == "🏆 Rewards":

        st.title("🏆 Rewards")

        st.info(
            "Rewards module coming soon."
        )

    elif page == "📅 Green Planner":

        st.title("📅 Green Planner")

        st.info(
            "Planner module coming soon."
        )

    elif page == "🛍 Green Products":

        st.title("🛍 Green Products")

        st.info(
            "Products module coming soon."
        )

    elif page == "🌎 Community":

        st.title("🌎 Community")

        st.info(
            "Community module coming soon."
        )