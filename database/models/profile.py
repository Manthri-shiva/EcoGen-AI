# Profile model
from dataclasses import dataclass


@dataclass
class Profile:
    id: int | None
    user_id: int

    age: int
    location: str
    family_size: int

    electricity_bill: float
    water_usage: float

    vehicle_type: str
    daily_travel_km: float

    waste_generated: float