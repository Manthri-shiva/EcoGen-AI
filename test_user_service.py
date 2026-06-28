"""
Test the User Service.
"""

from services.user_service import get_user_context

context = get_user_context()

print(context)