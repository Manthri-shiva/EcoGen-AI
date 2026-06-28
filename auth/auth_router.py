"""
Authentication Router for EcoGen AI
"""

import streamlit as st

from auth.login import show_login_page
from auth.register import show_register_page
from auth.session import is_logged_in


def show_auth_router():
    """
    Display Login/Register pages until
    the user successfully authenticates.
    """

    if is_logged_in():
        return True

    st.sidebar.title("EcoGen AI")

    page = st.sidebar.radio(
        "Authentication",
        [
            "Login",
            "Register",
        ],
    )

    if page == "Login":
        show_login_page()
    else:
        show_register_page()

    return False