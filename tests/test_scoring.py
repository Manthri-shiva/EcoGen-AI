from ml.scoring.scoring_engine import SustainabilityScorer

score = SustainabilityScorer(145)

print("\nSustainability Scores\n")

print("Energy:", score.energy_score())
print("Water:", score.water_score())
print("Waste:", score.waste_score())
print("Transport:", score.transport_score())
print("Overall:", score.overall_score())