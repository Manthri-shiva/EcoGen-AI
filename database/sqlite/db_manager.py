"""
SQLite Database Manager for EcoGen AI

Handles database connection, schema initialization, and CRUD operations
for users, profiles, and carbon data.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from database.models.profile import Profile
from database.models.carbon_data import CarbonData


class DatabaseManager:
    """
    Manages SQLite database operations for EcoGen AI.
    
    Provides methods for:
    - Connection management
    - Table creation
    - User management
    - Profile management
    - Carbon data storage and retrieval
    """

    def __init__(self, db_path: str = "database/sqlite/ecogen.db"):
        """
        Initialize DatabaseManager with database path.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """
        Establish connection to SQLite database.
        Creates database file if it doesn't exist.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print(f"[+] Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[-] Database connection error: {e}")
            raise

    def create_tables(self) -> None:
        """
        Create all required tables from schema.
        Tables: users, profiles, carbon_data
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        schema = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            age INTEGER,
            location TEXT,
            family_size INTEGER,
            electricity_bill REAL,
            water_usage REAL,
            vehicle_type TEXT,
            daily_travel_km REAL,
            waste_generated REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS carbon_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            electricity_emission REAL,
            transport_emission REAL,
            water_impact REAL,
            waste_impact REAL,
            total_carbon_footprint REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        try:
            self.cursor.executescript(schema)
            self.connection.commit()
            print("[+] Tables created successfully")
        except sqlite3.Error as e:
            print(f"[-] Error creating tables: {e}")
            raise

    def insert_user(self, name: str, email: Optional[str] = None) -> int:
        """
        Insert a new user into the database.
        
        Args:
            name: User's full name
            email: User's email address (optional)
            
        Returns:
            User ID of inserted user
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            self.cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            self.connection.commit()
            user_id = self.cursor.lastrowid
            print(f"[+] User created with ID: {user_id}")
            return user_id
        except sqlite3.Error as e:
            print(f"[-] Error inserting user: {e}")
            raise

    def insert_profile(self, profile: Profile) -> int:
        """
        Insert a user profile into the database.
        
        Args:
            profile: Profile dataclass instance
            
        Returns:
            Profile ID of inserted profile
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            self.cursor.execute(
                """INSERT INTO profiles 
                   (user_id, age, location, family_size, electricity_bill, 
                    water_usage, vehicle_type, daily_travel_km, waste_generated)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (profile.user_id, profile.age, profile.location, 
                 profile.family_size, profile.electricity_bill,
                 profile.water_usage, profile.vehicle_type,
                 profile.daily_travel_km, profile.waste_generated)
            )
            self.connection.commit()
            profile_id = self.cursor.lastrowid
            print(f"[+] Profile created with ID: {profile_id}")
            return profile_id
        except sqlite3.Error as e:
            print(f"[-] Error inserting profile: {e}")
            raise

    def get_profile(self, user_id: int) -> Optional[Profile]:
        """
        Retrieve user profile by user ID.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Profile dataclass instance or None if not found
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            self.cursor.execute(
                "SELECT * FROM profiles WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                (user_id,)
            )
            row = self.cursor.fetchone()
            
            if row:
                profile = Profile(
                    id=row['id'],
                    user_id=row['user_id'],
                    age=row['age'],
                    location=row['location'],
                    family_size=row['family_size'],
                    electricity_bill=row['electricity_bill'],
                    water_usage=row['water_usage'],
                    vehicle_type=row['vehicle_type'],
                    daily_travel_km=row['daily_travel_km'],
                    waste_generated=row['waste_generated']
                )
                print(f"[+] Profile retrieved for user {user_id}")
                return profile
            else:
                print(f"[-] No profile found for user {user_id}")
                return None
        except sqlite3.Error as e:
            print(f"[-] Error retrieving profile: {e}")
            raise

    def insert_carbon_result(self, carbon_data: CarbonData) -> int:
        """
        Insert carbon calculation result into database.
        
        Args:
            carbon_data: CarbonData dataclass instance
            
        Returns:
            Carbon data record ID
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            self.cursor.execute(
                """INSERT INTO carbon_data 
                   (user_id, electricity_emission, transport_emission, 
                    water_impact, waste_impact, total_carbon_footprint)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (carbon_data.user_id, carbon_data.electricity_emission,
                 carbon_data.transport_emission, carbon_data.water_impact,
                 carbon_data.waste_impact, carbon_data.total_carbon_footprint)
            )
            self.connection.commit()
            record_id = self.cursor.lastrowid
            print(f"[+] Carbon data stored with ID: {record_id}")
            return record_id
        except sqlite3.Error as e:
            print(f"[-] Error inserting carbon data: {e}")
            raise

    def get_carbon_result(self, user_id: int) -> Optional[CarbonData]:
        """
        Retrieve latest carbon calculation result for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            CarbonData dataclass instance or None if not found
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            self.cursor.execute(
                """SELECT * FROM carbon_data 
                   WHERE user_id = ? 
                   ORDER BY created_at DESC LIMIT 1""",
                (user_id,)
            )
            row = self.cursor.fetchone()
            
            if row:
                carbon_data = CarbonData(
                    id=row['id'],
                    user_id=row['user_id'],
                    electricity_emission=row['electricity_emission'],
                    transport_emission=row['transport_emission'],
                    water_impact=row['water_impact'],
                    waste_impact=row['waste_impact'],
                    total_carbon_footprint=row['total_carbon_footprint']
                )
                print(f"[+] Carbon data retrieved for user {user_id}")
                return carbon_data
            else:
                print(f"[-] No carbon data found for user {user_id}")
                return None
        except sqlite3.Error as e:
            print(f"[-] Error retrieving carbon data: {e}")
            raise

    def close(self) -> None:
        """
        Close database connection safely.
        """
        if self.connection:
            self.connection.close()
            print("[+] Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
