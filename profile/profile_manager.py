"""
Profile Manager for EcoGen AI

Handles CRUD operations for user profiles.
"""

import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "sqlite"
    / "ecogen.db"
)


def get_connection():
    """Return SQLite connection."""
    return sqlite3.connect(DB_PATH)


def profile_exists(user_id: int) -> bool:
    """Check whether a profile already exists."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT profile_id FROM profiles WHERE user_id=?",
        (user_id,),
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


def save_profile(
    user_id: int,
    age: int,
    gender: str,
    occupation: str,
    city: str,
    country: str,
    household_size: int,
    home_type: str,
    vehicle_type: str,
    income_range: str,
):
    """Create a new profile."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO profiles(
            user_id,
            age,
            gender,
            occupation,
            city,
            country,
            household_size,
            home_type,
            vehicle_type,
            income_range,
            created_at,
            updated_at
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            age,
            gender,
            occupation,
            city,
            country,
            household_size,
            home_type,
            vehicle_type,
            income_range,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()

def get_profile(user_id: int):
    """
    Return profile as a dictionary.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            profile_id,
            user_id,
            age,
            gender,
            occupation,
            city,
            country,
            household_size,
            home_type,
            vehicle_type,
            income_range,
            created_at,
            updated_at
        FROM profiles
        WHERE user_id=?
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "profile_id": row[0],
        "user_id": row[1],
        "age": row[2],
        "gender": row[3],
        "occupation": row[4],
        "city": row[5],
        "country": row[6],
        "household_size": row[7],
        "home_type": row[8],
        "vehicle_type": row[9],
        "income_range": row[10],
        "created_at": row[11],
        "updated_at": row[12],
    }
def update_profile(
    user_id: int,
    age: int,
    gender: str,
    occupation: str,
    city: str,
    country: str,
    household_size: int,
    home_type: str,
    vehicle_type: str,
    income_range: str,
):
    """Update an existing profile."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE profiles
        SET
            age=?,
            gender=?,
            occupation=?,
            city=?,
            country=?,
            household_size=?,
            home_type=?,
            vehicle_type=?,
            income_range=?,
            updated_at=?
        WHERE user_id=?
        """,
        (
            age,
            gender,
            occupation,
            city,
            country,
            household_size,
            home_type,
            vehicle_type,
            income_range,
            datetime.now().isoformat(),
            user_id,
        ),
    )

    conn.commit()
    conn.close()