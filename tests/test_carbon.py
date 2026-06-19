from ml.carbon.carbon_engine import CarbonCalculator

calculator = CarbonCalculator(
    electricity_bill=1500,
    water_usage=500,
    daily_travel_km=20,
    waste_generated=30
)

print("\nCarbon Footprint Results\n")

print(
    "Energy:",
    calculator.calculate_energy_emission()
)

print(
    "Transport:",
    calculator.calculate_transport_emission()
)

print(
    "Water:",
    calculator.calculate_water_impact()
)

print(
    "Waste:",
    calculator.calculate_waste_impact()
)

print(
    "Total:",
    calculator.calculate_total_footprint()
)