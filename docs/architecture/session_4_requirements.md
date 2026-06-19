# EcoGen AI - Session 4 Requirements

## Session Name

AI-Powered Sustainability Recommendation Engine

---

## Objective

Build an intelligent recommendation engine that converts carbon footprint predictions and sustainability scores into actionable, personalized sustainability recommendations.

Current System:

User Profile
→ Carbon Calculation
→ Sustainability Score
→ ML Prediction

Problem:

The system predicts carbon footprint but does not tell users what actions they should take.

Session 4 will bridge that gap.

---

## Current Project Status

### Completed

Session 1

* Sustainability Profiling Engine
* Carbon Calculator
* Sustainability Scoring Engine
* Unit Tests

Session 2

* SQLite Database Integration
* User Profile Storage
* Carbon Result Storage
* Database Testing

Session 3

* Dataset Generation
* Machine Learning Model Training
* Model Evaluation
* Prediction Engine
* Model Persistence

---

## Session 4 Goal

Move from:

Prediction
↓
Carbon Footprint Value

to:

Prediction
↓
Carbon Analysis
↓
Personalized Recommendations
↓
Estimated Carbon Reduction

---

## Module To Build

File:

ml/recommendations/recommendation_engine.py

---

## Input Data

User Profile

* age
* family_size
* location
* electricity_bill
* water_usage
* daily_travel_km
* waste_generated
* vehicle_type

Carbon Results

* total_carbon_footprint
* sustainability_score

ML Prediction

* predicted_carbon_footprint

---

## Recommendation Categories

### Energy Recommendations

Trigger:

High electricity consumption

Examples:

* Replace incandescent bulbs with LED lighting
* Turn off standby devices
* Use energy-efficient appliances
* Install rooftop solar panels
* Monitor monthly energy usage

Estimated Reduction:

5% – 25%

---

### Transportation Recommendations

Trigger:

High travel distance

Examples:

* Use public transport twice a week
* Carpool with colleagues
* Use electric vehicles
* Reduce unnecessary trips
* Use cycling for short distances

Estimated Reduction:

5% – 30%

---

### Water Recommendations

Trigger:

High water usage

Examples:

* Fix leaking taps
* Install water-saving fixtures
* Reuse grey water
* Reduce shower duration

Estimated Reduction:

2% – 10%

---

### Waste Recommendations

Trigger:

High waste generation

Examples:

* Compost organic waste
* Recycle plastics and paper
* Reduce food waste
* Use reusable containers

Estimated Reduction:

2% – 15%

---

## Recommendation Priority System

Priority Levels:

HIGH

MEDIUM

LOW

Example:

HIGH

* Electricity Bill > 3000

MEDIUM

* Electricity Bill 1500–3000

LOW

* Electricity Bill < 1500

---

## Recommendation Output Format

Example:

{
"recommendations": [
{
"category": "Energy",
"priority": "HIGH",
"action": "Install LED lighting",
"estimated_reduction": "12%"
},
{
"category": "Transport",
"priority": "MEDIUM",
"action": "Use public transport twice a week",
"estimated_reduction": "8%"
}
]
}

---

## Recommendation Scoring

The engine should:

1. Analyze carbon footprint
2. Analyze sustainability score
3. Rank recommendations
4. Estimate reduction potential
5. Return prioritized actions

---

## Required Functions

generate_energy_recommendations()

generate_transport_recommendations()

generate_water_recommendations()

generate_waste_recommendations()

generate_personalized_plan()

calculate_estimated_reduction()

---

## Folder Structure

ml/
└── recommendations/
└── recommendation_engine.py

tests/
└── test_recommendation.py

---

## Success Criteria

Input:

Electricity Bill = 4000
Daily Travel = 70 km
Waste = 80 kg

Output:

High Priority Energy Recommendations

High Priority Transport Recommendations

Medium Priority Waste Recommendations

Estimated Total Reduction Potential

---

## Constraints

Do Not Modify

* ml/carbon/
* ml/scoring/
* ml/prediction/
* app/
* rag/
* genai/

Only Work In

* ml/recommendations/
* tests/

---

## Deliverables

1. Recommendation Engine
2. Priority Ranking System
3. Reduction Estimation Logic
4. Personalized Sustainability Plan
5. Recommendation Unit Tests

Session 4 is complete only when recommendations are generated automatically from user carbon footprint and sustainability data.
