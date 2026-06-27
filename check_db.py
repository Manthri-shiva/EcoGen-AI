"""
Database Verification Script for EcoGen AI
"""

import sqlite3
from pathlib import Path

from auth.auth_manager import create_profiles_table
from assessment.assessment_manager import create_analysis_table

DB_PATH = (
    Path(__file__).resolve().parent
    / "database"
    / "sqlite"
    / "ecogen.db"
)

print("Database:", DB_PATH)

# Create required tables
create_profiles_table()
create_analysis_table()

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List all tables
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("\nTables Found:")

for table in tables:
    print(f"- {table[0]}")

conn.close()

print("\nDatabase verification completed successfully.")