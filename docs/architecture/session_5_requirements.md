# EcoGen AI - Session 5 Requirements

## Session Name

Explainable AI (XAI) Engine

---

# Objective

Build an Explainable AI module that explains why the Machine Learning model predicted a particular carbon footprint.

Current System:

User Data
↓
Carbon Calculator
↓
Prediction Model
↓
Predicted Carbon Footprint

Problem:

The user receives a prediction but does not know:

* Why the prediction was generated
* Which factors contributed the most
* Which lifestyle habits are increasing carbon emissions

Session 5 solves this problem.

---

# Current Project Status

## Completed

### Session 1

* Carbon Calculator
* Sustainability Scoring Engine
* Unit Testing

### Session 2

* SQLite Database
* User Profile Storage
* Carbon Storage
* Database Testing

### Session 3

* Dataset Generation
* Model Training
* Model Evaluation
* Prediction Engine

### Session 4

* Recommendation Engine
* Priority Ranking
* Reduction Estimation
* Recommendation Testing

---

# Session 5 Goal

Move from:

Prediction
↓
1742 kg CO2

to:

Prediction
↓
1742 kg CO2

Explanation:

Electricity Bill → 52%
Travel Distance → 28%
Waste Generation → 11%
Water Usage → 6%
Family Size → 2%
Age → 1%

---

# Module To Build

File:

ml/explainability/shap_engine.py

---

# Explainability Inputs

User Features:

* age
* family_size
* electricity_bill
* water_usage
* daily_travel_km
* waste_generated

Model:

models/carbon_model.pkl

Dataset:

datasets/carbon/sample_users.csv

---

# Explainability Outputs

The engine should explain:

1. Which features contribute most
2. Which features contribute least
3. Which lifestyle factor should be improved first
4. Percentage contribution of each feature

---

# Feature Importance Ranking

Expected Output Example

Predicted Carbon Footprint:
1742 kg CO2

Feature Contributions

1. Electricity Bill → 52%
2. Daily Travel Distance → 28%
3. Waste Generated → 11%
4. Water Usage → 6%
5. Family Size → 2%
6. Age → 1%

---

# Required Functions

load_trained_model()

load_dataset()

calculate_feature_importance()

generate_explanation()

get_top_contributors()

generate_actionable_insights()

---

# Explainability Logic

The engine must:

1. Load trained model
2. Load dataset
3. Calculate feature importance
4. Rank features
5. Generate human-readable explanation
6. Generate actionable insights

Example:

Your electricity consumption contributes most to your carbon footprint.

Reducing electricity usage by 15% could significantly improve your sustainability score.

---

# Human Readable Insights

Example:

Top Contributor:
Electricity Bill

Impact:
High

Recommendation:
Switch to LED lighting and monitor monthly energy usage.

Expected Benefit:
Reduce overall footprint by 10–20%.

---

# Output Format

{
"predicted_footprint": 1742,
"top_contributors": [
{
"feature": "electricity_bill",
"importance": 52
},
{
"feature": "daily_travel_km",
"importance": 28
}
],
"insights": [
"Electricity consumption is your largest contributor.",
"Transportation emissions are your second largest contributor."
]
}

---

# Folder Structure

ml/
└── explainability/
└── shap_engine.py

tests/
└── test_explainability.py

---

# Success Criteria

Input:

Age = 25
Family Size = 4
Electricity Bill = 2000
Water Usage = 500
Travel Distance = 20 km
Waste Generated = 25

Output:

Predicted Carbon Footprint

Feature Importance Ranking

Top Contributors

Actionable Insights

---

# Constraints

Do Not Modify:

* ml/carbon/
* ml/scoring/
* ml/prediction/
* ml/recommendations/
* database/

Only Work In:

* ml/explainability/
* tests/

---

# Deliverables

1. Explainability Engine
2. Feature Importance Analysis
3. Contributor Ranking
4. Human Readable Insights
5. Explainability Testing

Session 5 is complete only when the AI model can explain WHY a prediction was generated and identify the most important sustainability factors influencing the result.
