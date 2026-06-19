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