"""
EcoGen AI - Main Entry Point
"""

import streamlit as st

from auth.auth_manager import (
    create_users_table,
    create_profiles_table,
)

from auth.auth_router import show_auth_router
from profile.profile_router import show_profile_router
from application.app import run_application


st.set_page_config(
    page_title="EcoGen AI",
    page_icon="🌍",
    layout="wide",
)


def initialize_database():
    """
    Create all required database tables if they do not exist.
    """

    create_users_table()
    create_profiles_table()


def main():
    """
    EcoGen AI Application Flow

    1. Initialize Database
    2. Authentication
    3. Profile Completion
    4. Launch Application
    """

    # Initialize database tables
    initialize_database()

    # Authentication
    if not show_auth_router():
        return

    # Profile completion
    if not show_profile_router():
        return

    # Launch EcoGen AI
    run_application()


if __name__ == "__main__":
    main()