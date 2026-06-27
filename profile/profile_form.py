"""
Profile Form for EcoGen AI
"""

import streamlit as st

from auth.session import get_current_user
from profile.profile_manager import save_profile


def show_profile_form():
    """
    Display the one-time profile completion form.

    Returns
    -------
    bool
        True if the profile was saved successfully.
    """

    user = get_current_user()

    st.title("👤 Complete Your Profile")

    st.caption(
        "Complete your profile once. "
        "This information powers EcoTwin AI, AI Coach, and personalized sustainability insights."
    )

    with st.form("profile_form"):

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=25,
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other",
                "Prefer not to say",
            ],
        )

        occupation = st.text_input("Occupation")

        country = st.text_input("Country")

        city = st.text_input("City")

        household_size = st.number_input(
            "Household Size",
            min_value=1,
            max_value=20,
            value=1,
        )

        home_type = st.selectbox(
            "Home Type",
            [
                "Apartment",
                "Independent House",
                "Villa",
                "Other",
            ],
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "None",
                "Bicycle",
                "Motorcycle",
                "Car",
                "Electric Vehicle",
            ],
        )

        income_range = st.selectbox(
            "Income Range",
            [
                "Below 25,000",
                "25,000 - 50,000",
                "50,000 - 100,000",
                "Above 100,000",
            ],
        )

        submitted = st.form_submit_button("Save Profile")

    if not submitted:
        return False

    if not occupation.strip():
        st.error("Occupation is required.")
        return False

    if not country.strip():
        st.error("Country is required.")
        return False

    if not city.strip():
        st.error("City is required.")
        return False

    save_profile(
        user_id=user["user_id"],
        age=age,
        gender=gender,
        occupation=occupation,
        city=city,
        country=country,
        household_size=household_size,
        home_type=home_type,
        vehicle_type=vehicle_type,
        income_range=income_range,
    )

    st.success("✅ Profile saved successfully.")

    return True