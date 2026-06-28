"""
EcoGen AI Application Controller
"""

import streamlit as st

from assessment.assessment_form import show_assessment_form

from application.navigation import show_navigation
from application.page_router import route_page

from services.user_service import get_user_context


def run_application():
    """
    Launch EcoGen AI after successful authentication.
    """

    context = get_user_context()

    if context is None:

        st.error("User session not found.")

        return

    assessment = context["assessment"]

    # First-time user
    if assessment is None:

        st.title("🌍 EcoGen AI")

        st.info(
            "Complete your first Monthly Sustainability Assessment."
        )

        show_assessment_form()

        return

    # Sidebar
    page = show_navigation()

    # Route selected page
    route_page(
        page=page,
        context=context,
    )