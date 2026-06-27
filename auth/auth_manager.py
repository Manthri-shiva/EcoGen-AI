"""
Authentication Manager for EcoGen AI

Handles all authentication-related database operations.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

from auth.password_utils import (
    hash_password,
    verify_password,
)

# Database Location
DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "sqlite"
    / "ecogen.db"
)


def get_connection():
    """
    Create SQLite connection.
    """
    return sqlite3.connect(DB_PATH)


def create_users_table():
    """
    Create users table if it does not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TEXT,

            last_login TEXT

        )
        """
    )

    conn.commit()
    conn.close()


def user_exists(email: str) -> bool:
    """
    Check whether email already exists.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,),
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


def register_user(
    full_name: str,
    email: str,
    password: str,
):
    """
    Register a new user.
    """

    if user_exists(email):
        return False, "Email already exists."

    password_hash = hash_password(password)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(
            full_name,
            email,
            password_hash,
            created_at
        )
        VALUES(?,?,?,?)
        """,
        (
            full_name,
            email,
            password_hash,
            datetime.now().isoformat(),
        ),
    )

    conn.commit()

    conn.close()

    return True, "Registration Successful."


def get_user_by_email(email: str):
    """
    Return user by email.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,),
    )

    user = cursor.fetchone()

    conn.close()

    return user


def authenticate_user(
    email: str,
    password: str,
):
    """
    Authenticate login.
    """

    user = get_user_by_email(email)

    if user is None:
        return False, "User not found."

    stored_hash = user[3]

    if verify_password(
        password,
        stored_hash,
    ):

        update_last_login(user[0])

        return True, user

    return False, "Invalid password."


def update_last_login(user_id: int):
    """
    Update last login timestamp.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET last_login=?
        WHERE user_id=?
        """,
        (
            datetime.now().isoformat(),
            user_id,
        ),
    )

    conn.commit()

    conn.close()
def create_profiles_table():
    """
    Create the user profiles table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles(

            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            age INTEGER,

            gender TEXT,

            occupation TEXT,

            city TEXT,

            country TEXT,

            household_size INTEGER,

            home_type TEXT,

            vehicle_type TEXT,

            income_range TEXT,

            created_at TEXT,

            updated_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)
        )
        """
    )

    conn.commit()
    conn.close()