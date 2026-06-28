"""
User Service for EcoGen AI

Provides a unified interface to retrieve the
currently logged-in user's data.
"""

from auth.session import get_current_user

from profile.profile_manager import get_profile

from assessment.assessment_manager import (
    get_latest_assessment,
)


def get_user_context():
    """
    Return all information required by the application.

    Returns
    -------
    dict
        {
            "user": ...,
            "profile": ...,
            "assessment": ...
        }
    """

    user = get_current_user()

    if user is None:
        return None

    user_id = user["user_id"]

    profile = get_profile(user_id)

    assessment = get_latest_assessment(user_id)

    return {
        "user": user,
        "profile": profile,
        "assessment": assessment,
    }