"""
Profile Router for EcoGen AI
"""

from auth.session import get_current_user
from profile.profile_manager import profile_exists
from profile.profile_form import show_profile_form


def show_profile_router():
    """
    Ensure the logged-in user has completed
    their profile.

    Returns
    -------
    bool
        True if profile exists or has just been saved.
    """

    user = get_current_user()

    if user is None:
        return False

    if profile_exists(user["user_id"]):
        return True

    return show_profile_form()