"""
User Registration Page for EcoGen AI
"""

import streamlit as st

from auth.auth_manager import register_user


def show_register_page():
    """
    Display the user registration form.
    """

    st.title("📝 Create EcoGen AI Account")

    with st.form("register_form"):

        full_name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        password = st.text_input(
            "Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
        )

        submitted = st.form_submit_button("Register")

    if submitted:

        if not full_name.strip():
            st.error("Full Name is required.")
            return

        if not email.strip():
            st.error("Email is required.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        if len(password) < 8:
            st.error("Password must contain at least 8 characters.")
            return

        success, message = register_user(
            full_name,
            email,
            password,
        )

        if success:
            st.success(message)
            st.info("You can now login using your credentials.")

        else:
            st.error(message)