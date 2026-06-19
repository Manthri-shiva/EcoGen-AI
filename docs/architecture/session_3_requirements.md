# EcoGen AI - Session 3 Requirements

## Session Name

AI Carbon Footprint Prediction Engine

---

## Objective

Build the first Machine Learning module of EcoGen AI.

The system should predict a user's future carbon footprint based on sustainability profile data.

The prediction engine will help users understand how their current lifestyle impacts future environmental outcomes and provide the foundation for AI-driven sustainability recommendations.

---

## Current Project Status

### Completed

Session 1

* Sustainability Profiling Engine
* Carbon Footprint Calculation Engine
* Sustainability Scoring Engine
* Unit Testing

Session 2

* SQLite Database Integration
* User Persistence Layer
* Profile Persistence Layer
* Carbon Result Persistence Layer
* End-to-End Database Testing

---

## Session 3 Goal

Move from:

User Data
→ Carbon Calculation

to:

User Data
→ Carbon Prediction Model
→ Future Carbon Forecast

---

## Machine Learning Objective

Predict:

predicted_carbon_footprint

using:

* electricity_bill
* water_usage
* daily_travel_km
* waste_generated
* family_size
* vehicle_type

---

## Dataset Requirements

Location:

datasets/carbon/

Required File:

sample_users.csv

Minimum Records:

500

Recommended Records:

1000+

Columns:

user_id
age
family_size
electricity_bill
water_usage
daily_travel_km
waste_generated
vehicle_type
total_carbon_footprint

Target Variable:

total_carbon_footprint

---

## Files To Implement

### ml/prediction/train.py

Responsibilities:

* Load dataset
* Data cleaning
* Feature engineering
* Train model
* Save trained model

Output:

models/carbon_model.pkl

---

### ml/prediction/predict.py

Responsibilities:

* Load trained model
* Accept user features
* Generate prediction

Output Example:

{
"predicted_carbon_footprint": 1854.5
}

---

### ml/prediction/evaluate.py

Responsibilities:

* Evaluate model
* Calculate:

  * MAE
  * RMSE
  * R2 Score

Generate evaluation report.

---

## Recommended Algorithms

Phase 1:

* Linear Regression

Phase 2:

* Random Forest Regressor

Phase 3:

* XGBoost Regressor

Current Session:

Implement only Linear Regression and Random Forest.

Do not implement XGBoost yet.

---

## Required Libraries

pandas

numpy

scikit-learn

joblib

matplotlib

---

## Folder Structure

ml/
└── prediction/
├── train.py
├── predict.py
└── evaluate.py

datasets/
└── carbon/
└── sample_users.csv

models/
└── carbon_model.pkl

---

## Success Criteria

The following workflow must execute successfully:

Load Dataset
↓
Train Model
↓
Save Model
↓
Load Model
↓
Predict Carbon Footprint
↓
Evaluate Accuracy

Output Example:

Input:

electricity_bill = 2000
water_usage = 600
daily_travel_km = 30
waste_generated = 50

Output:

predicted_carbon_footprint = 1925.4

---

## Constraints

Do Not Modify:

* app/
* genai/
* rag/
* ml/carbon/
* ml/scoring/

Only work inside:

* ml/prediction/
* datasets/carbon/
* models/

---

## Deliverables

1. Dataset
2. Trained Model
3. Prediction Engine
4. Evaluation Engine
5. Model Performance Report
6. Unit Tests

Session 3 is complete only when prediction and evaluation work successfully.
