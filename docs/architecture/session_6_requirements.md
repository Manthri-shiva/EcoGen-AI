# EcoGen AI - Session 6 Requirements

## Session Name

Location Intelligence Engine

---

# Objective

Build a Location Intelligence Engine that provides location-specific sustainability analysis and recommendations.

Current System:

User Profile
↓
Carbon Calculator
↓
ML Prediction
↓
Explainability Engine
↓
Recommendation Engine

Problem:

Current recommendations are generic and do not consider:

* User location
* Regional climate
* Renewable energy availability
* Transportation infrastructure
* Water scarcity
* Waste management systems

Session 6 solves this problem.

---

# Current Project Status

## Completed

### Session 1

* Carbon Calculator
* Sustainability Scoring Engine

### Session 2

* Database Integration
* User Profile Management

### Session 3

* Dataset Generation
* ML Model Training
* Prediction Engine

### Session 4

* Recommendation Engine
* Reduction Estimation

### Session 5

* Explainability Engine
* Feature Importance Analysis

---

# Session 6 Goal

Move from:

Recommendation:
Install Solar Panels

to:

Recommendation:
Install Solar Panels

Reason:
Your location (Hyderabad) receives high annual solar radiation and has strong rooftop solar potential.

---

# Module To Build

File:

ml/location/location_engine.py

---

# Supported Locations

Initial Version:

* Hyderabad
* Bengaluru
* Chennai
* Mumbai
* Delhi
* Pune
* Kolkata

Future versions can expand.

---

# Location Data Model

Each city should include:

City Name

Solar Potential

* HIGH
* MEDIUM
* LOW

Public Transport Quality

* HIGH
* MEDIUM
* LOW

Water Scarcity Risk

* HIGH
* MEDIUM
* LOW

Waste Management Efficiency

* HIGH
* MEDIUM
* LOW

Air Pollution Level

* HIGH
* MEDIUM
* LOW

---

# Example City Profiles

Hyderabad

Solar Potential: HIGH
Public Transport: MEDIUM
Water Scarcity: HIGH
Waste Management: MEDIUM
Air Pollution: MEDIUM

---

Bengaluru

Solar Potential: HIGH
Public Transport: HIGH
Water Scarcity: MEDIUM
Waste Management: MEDIUM
Air Pollution: MEDIUM

---

Mumbai

Solar Potential: MEDIUM
Public Transport: HIGH
Water Scarcity: LOW
Waste Management: HIGH
Air Pollution: HIGH

---

Delhi

Solar Potential: HIGH
Public Transport: HIGH
Water Scarcity: HIGH
Waste Management: MEDIUM
Air Pollution: HIGH

---

# Required Functions

load_location_profiles()

get_location_profile()

generate_location_recommendations()

generate_location_insights()

generate_location_report()

---

# Recommendation Logic

Solar Potential = HIGH

Recommend:

* Rooftop Solar
* Solar Water Heating
* Renewable Energy Adoption

---

Public Transport = HIGH

Recommend:

* Metro Usage
* Public Transport
* Carpooling

---

Water Scarcity = HIGH

Recommend:

* Rainwater Harvesting
* Water Conservation
* Grey Water Reuse

---

Air Pollution = HIGH

Recommend:

* Public Transport
* EV Adoption
* Reduced Private Vehicle Usage

---

Waste Management = LOW

Recommend:

* Household Composting
* Waste Segregation
* Community Recycling Programs

---

# Output Format

{
"city": "Hyderabad",
"location_profile": {},
"recommendations": [],
"insights": []
}

---

# Example Output

Location Report

City:
Hyderabad

Key Insights:

* High rooftop solar potential.
* Water conservation should be prioritized.
* Public transportation can reduce emissions.

Recommendations:

1. Install rooftop solar panels.
2. Implement rainwater harvesting.
3. Use public transportation more frequently.

---

# Folder Structure

ml/
└── location/
└── location_engine.py

tests/
└── test_location.py

---

# Success Criteria

Input:

City = Hyderabad

Output:

Location Profile

Location-Based Recommendations

Location-Based Insights

Location Report

---

# Constraints

Do Not Modify:

* ml/prediction/
* ml/recommendations/
* ml/explainability/
* database/

Only Work In:

* ml/location/
* tests/

---

# Deliverables

1. Location Intelligence Engine
2. City Profile System
3. Location-Based Recommendations
4. Location Insights
5. Location Testing

Session 6 is complete only when recommendations become location-aware and city-specific rather than generic.
