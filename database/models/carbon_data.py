# Carbon data model
from dataclasses import dataclass


@dataclass
class CarbonData:
    id: int | None
    user_id: int

    electricity_emission: float
    transport_emission: float
    water_impact: float
    waste_impact: float

    total_carbon_footprint: float
from dataclasses import dataclass


@dataclass
class CarbonData:
    id: int | None
    user_id: int

    electricity_emission: float
    transport_emission: float
    water_impact: float
    waste_impact: float

    total_carbon_footprint: float