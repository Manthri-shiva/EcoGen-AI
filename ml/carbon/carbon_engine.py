class CarbonCalculator:

    ELECTRICITY_FACTOR = 0.82
    TRANSPORT_FACTOR = 0.21
    WATER_FACTOR = 0.001
    WASTE_FACTOR = 0.5

    def __init__(
        self,
        electricity_bill,
        water_usage,
        daily_travel_km,
        waste_generated
    ):
        self.electricity_bill = electricity_bill
        self.water_usage = water_usage
        self.daily_travel_km = daily_travel_km
        self.waste_generated = waste_generated

    def calculate_energy_emission(self):
        return round(
            self.electricity_bill *
            self.ELECTRICITY_FACTOR,
            2
        )

    def calculate_transport_emission(self):
        return round(
            self.daily_travel_km *
            self.TRANSPORT_FACTOR *
            30,
            2
        )

    def calculate_water_impact(self):
        return round(
            self.water_usage *
            self.WATER_FACTOR,
            2
        )

    def calculate_waste_impact(self):
        return round(
            self.waste_generated *
            self.WASTE_FACTOR,
            2
        )

    def calculate_total_footprint(self):

        total = (
            self.calculate_energy_emission()
            + self.calculate_transport_emission()
            + self.calculate_water_impact()
            + self.calculate_waste_impact()
        )

        return round(total, 2)