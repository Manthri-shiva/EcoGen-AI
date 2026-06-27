"""
Navigation Controller for EcoGen AI

Handles navigation between all authenticated application modules.
"""

import streamlit as st


def show_navigation() -> str:
    """
    Display the application sidebar navigation.

    Returns
    -------
    str
        Selected module.
    """

    st.sidebar.title("🌍 EcoGen AI")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        (
            "🏠 Dashboard",
            "📝 Monthly Assessment",
            "🤖 AI Coach",
            "🌱 EcoTwin",
            "📈 Reports",
            "🏆 Rewards",
            "📅 Green Planner",
            "🛍 Green Products",
            "🌎 Community",
        ),
    )

    st.sidebar.markdown("---")

    st.sidebar.success("EcoGen AI v1.0")

    return page