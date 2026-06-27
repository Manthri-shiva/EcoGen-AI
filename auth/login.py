"""
User Login Page for EcoGen AI
"""

import streamlit as st

from auth.auth_manager import authenticate_user
from auth.session import login_user


def show_login_page():
    """
    Display the login form.
    """

    st.title("🔐 Login to EcoGen AI")

    with st.form("login_form"):

        email = st.text_input("Email Address")

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button("Login")

    if submitted:

        if not email.strip():
            st.error("Email is required.")
            return

        if not password.strip():
            st.error("Password is required.")
            return

        success, result = authenticate_user(
            email,
            password,
        )

        if success:

            login_user(result)

            st.success(
                f"Welcome back, {result[1]}!"
            )

            st.rerun()

        else:

            st.error(result)