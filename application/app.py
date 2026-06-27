"""
EcoGen AI Application Launcher
"""

import streamlit as st

from auth.session import get_current_user


def run_application():
    """
    Launch the authenticated application.
    """

    user = get_current_user()

    st.success(f"Welcome, {user['user_name']}! 👋")

    st.title("🌍 EcoGen AI")

    st.markdown("---")

    st.subheader("Application Status")

    st.success("✅ Authentication Completed")

    st.success("✅ Profile Completed")

    st.info("Next Phase: Monthly Sustainability Assessment")

    st.write(f"Logged in as: **{user['user_email']}**")