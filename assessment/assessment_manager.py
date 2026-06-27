"""
Assessment Manager for EcoGen AI

Handles database operations for sustainability assessments.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from assessment.analysis_engine import AnalysisEngine
DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "sqlite"
    / "ecogen.db"
)


def get_connection():
    """Return SQLite connection."""
    return sqlite3.connect(DB_PATH)


def create_analysis_table():
    """
    Create the analysis_history table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history(

            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            assessment_date TEXT,

            electricity_kwh REAL,

            water_liters REAL,

            travel_km REAL,

            waste_kg REAL,

            carbon_footprint REAL,

            sustainability_score REAL,

            eco_dna TEXT,

            journey_level TEXT,

            reward_points INTEGER,

            created_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """
    )

    conn.commit()
    conn.close()


def save_assessment(
    user_id: int,
    electricity_kwh: float,
    water_liters: float,
    travel_km: float,
    waste_kg: float,
    carbon_footprint: float,
    sustainability_score: float,
    eco_dna: str,
    journey_level: str,
    reward_points: int,
):
    """
    Save one sustainability assessment.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history(

            user_id,
            assessment_date,
            electricity_kwh,
            water_liters,
            travel_km,
            waste_kg,
            carbon_footprint,
            sustainability_score,
            eco_dna,
            journey_level,
            reward_points,
            created_at

        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            datetime.now().date().isoformat(),
            electricity_kwh,
            water_liters,
            travel_km,
            waste_kg,
            carbon_footprint,
            sustainability_score,
            eco_dna,
            journey_level,
            reward_points,
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def get_latest_assessment(user_id: int):
    """
    Return the latest sustainability assessment
    as a dictionary.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            analysis_id,
            user_id,
            assessment_date,
            electricity_kwh,
            water_liters,
            travel_km,
            waste_kg,
            carbon_footprint,
            sustainability_score,
            eco_dna,
            journey_level,
            reward_points,
            created_at
        FROM analysis_history
        WHERE user_id=?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "analysis_id": row[0],
        "user_id": row[1],
        "assessment_date": row[2],
        "electricity_kwh": row[3],
        "water_liters": row[4],
        "travel_km": row[5],
        "waste_kg": row[6],
        "carbon_footprint": row[7],
        "sustainability_score": row[8],
        "eco_dna": row[9],
        "journey_level": row[10],
        "reward_points": row[11],
        "created_at": row[12],
    }
def get_assessment_history(user_id: int):
    """
    Return all sustainability assessments for a user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analysis_history
        WHERE user_id=?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    history = cursor.fetchall()

    conn.close()

    return history
def process_assessment(
    user_id: int,
    electricity_kwh: float,
    water_liters: float,
    travel_km: float,
    waste_kg: float,
):
    """
    Run the complete sustainability assessment workflow.

    1. Calculate sustainability metrics.
    2. Save the assessment.
    3. Return the calculated results.
    """

    results = AnalysisEngine.calculate(
        electricity_kwh=electricity_kwh,
        water_liters=water_liters,
        travel_km=travel_km,
        waste_kg=waste_kg,
    )

    save_assessment(
        user_id=user_id,
        electricity_kwh=electricity_kwh,
        water_liters=water_liters,
        travel_km=travel_km,
        waste_kg=waste_kg,
        carbon_footprint=results["carbon_footprint"],
        sustainability_score=results["sustainability_score"],
        eco_dna=results["eco_dna"],
        journey_level=results["journey_level"],
        reward_points=results["reward_points"],
    )

    return results