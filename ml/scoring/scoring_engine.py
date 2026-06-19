class SustainabilityScorer:

    def __init__(self, carbon_footprint):
        self.carbon_footprint = carbon_footprint

    def energy_score(self):
        return max(0, 100 - int(self.carbon_footprint * 0.10))

    def water_score(self):
        return max(0, 100 - int(self.carbon_footprint * 0.08))

    def waste_score(self):
        return max(0, 100 - int(self.carbon_footprint * 0.05))

    def transport_score(self):
        return max(0, 100 - int(self.carbon_footprint * 0.07))

    def overall_score(self):

        scores = [
            self.energy_score(),
            self.water_score(),
            self.waste_score(),
            self.transport_score()
        ]

        return round(sum(scores) / len(scores), 2)