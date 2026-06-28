"""
Session Manager for EcoGen AI

Handles user login sessions using Streamlit session_state.
"""

import streamlit as st


def login_user(user):
    """
    Store authenticated user information in the session.
    """

    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user[0]
    st.session_state["user_name"] = user[1]
    st.session_state["user_email"] = user[2]


def logout_user():
    """
    Clear the current user session.
    """

    st.session_state.clear()


def is_logged_in() -> bool:
    """
    Check whether a user is logged in.
    """

    return st.session_state.get("logged_in", False)


def get_current_user():
    """
    Return current logged-in user information.
    """

    if not is_logged_in():
        return None

    return {
        "user_id": st.session_state.get("user_id"),
        "user_name": st.session_state.get("user_name"),
        "user_email": st.session_state.get("user_email"),
    }


def require_login():
    """
    Stop page execution if the user is not authenticated.
    """

    if not is_logged_in():
        st.warning("Please login to continue.")
        st.stop()