from auth.auth_manager import create_profiles_table
from auth.auth_manager import (
    create_users_table,
    register_user,
    authenticate_user,
)

create_users_table()

print(register_user(
    "Shiva",
    "shiva@gmail.com",
    "EcoGen@123"
))

print(
    authenticate_user(
        "shiva@gmail.com",
        "EcoGen@123",
    )
)