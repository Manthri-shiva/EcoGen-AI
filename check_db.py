import sqlite3
from pathlib import Path

from auth.auth_manager import create_profiles_table

DB_PATH = (
    Path(__file__).resolve().parent
    / "database"
    / "sqlite"
    / "ecogen.db"
)

print("Database:", DB_PATH)

# Create the table
create_profiles_table()

# Check all tables
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("\nTables:")

for table in tables:
    print("-", table[0])

conn.close()