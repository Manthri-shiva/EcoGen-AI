# EcoGen AI - Session 7 Requirements

## Session Name

GenAI Sustainability Advisor

---

# Objective

Build an AI Sustainability Advisor that generates personalized sustainability guidance using:

* User Profile
* Carbon Footprint Prediction
* Explainability Results
* Sustainability Score
* Location Intelligence

Current System:

User
↓
Carbon Calculator
↓
Prediction Engine
↓
Explainability Engine
↓
Recommendation Engine
↓
Location Intelligence

Problem:

Current recommendations are static and rule-based.

Example:

* Install rooftop solar
* Use public transport
* Reduce electricity usage

These recommendations lack:

* Personalization
* Natural language explanations
* Goal-based planning
* AI-generated sustainability coaching

Session 7 solves this problem.

---

# Session 7 Goal

Move from:

Recommendation:
Install rooftop solar

to:

AI Advisor Response:

Based on your current electricity usage and your location in Hyderabad, rooftop solar installation could significantly reduce your carbon footprint. Hyderabad has excellent solar potential, making solar energy one of the most impactful sustainability improvements for your household.

Estimated Benefit:
10–20% reduction in emissions.

---

# Module To Build

File:

genai/advisor/sustainability_advisor.py

---

# Inputs

User Profile:

* age
* family_size
* location

Carbon Analysis:

* carbon_footprint
* sustainability_score

Explainability:

* top_contributors

Recommendations:

* sustainability_recommendations

Location Intelligence:

* location_recommendations

---

# Required Functions

generate_user_summary()

generate_sustainability_advice()

generate_priority_actions()

generate_weekly_plan()

generate_monthly_plan()

generate_advisor_report()

---

# Advisor Responsibilities

The advisor should:

1. Analyze the user's sustainability profile
2. Explain key environmental challenges
3. Recommend high-impact actions
4. Generate short-term sustainability plans
5. Generate long-term sustainability plans
6. Encourage positive sustainability habits

---

# User Summary Example

User Summary

Age: 25

Location: Hyderabad

Carbon Footprint:
1742 kg CO2

Sustainability Score:
62

Top Contributor:
Electricity Usage

---

# Sustainability Advice Example

Your electricity consumption is currently the largest contributor to your carbon footprint.

Since Hyderabad has strong solar energy potential, adopting rooftop solar could significantly lower your environmental impact.

Additionally, replacing older appliances with energy-efficient alternatives could improve your sustainability score.

---

# Priority Actions

High Priority:

1. Reduce electricity usage
2. Install rooftop solar
3. Monitor monthly energy consumption

Medium Priority:

1. Increase public transport usage
2. Improve waste segregation

Low Priority:

1. Track water consumption
2. Participate in local sustainability initiatives

---

# Weekly Plan

Week 1

* Replace inefficient bulbs
* Measure daily electricity usage

Week 2

* Begin waste segregation

Week 3

* Explore solar installation options

Week 4

* Review sustainability progress

---

# Monthly Plan

Month 1

Focus:
Energy Optimization

Month 2

Focus:
Transportation Improvements

Month 3

Focus:
Water Conservation

---

# Output Format

{
"user_summary": "",
"advisor_message": "",
"priority_actions": [],
"weekly_plan": [],
"monthly_plan": []
}

---

# Demo Input

Age = 25

Family Size = 4

Location = Hyderabad

Carbon Footprint = 1742

Sustainability Score = 62

Top Contributor:

Electricity Bill

---

# Demo Output

==================================================
ECOGEN AI - AI SUSTAINABILITY ADVISOR
=====================================

User Summary

Advisor Insights

Priority Actions

Weekly Plan

Monthly Plan

==================================================

---

# Folder Structure

genai/
└── advisor/
└── sustainability_advisor.py

tests/
└── test_advisor.py

---

# Success Criteria

Input:

User Sustainability Data

Output:

AI-generated personalized sustainability report

Including:

* Summary
* Advice
* Priority Actions
* Weekly Plan
* Monthly Plan

---

# Constraints

Do Not Modify:

* ml/
* database/
* rag/

Only Work In:

* genai/advisor/
* tests/

---

# Deliverables

1. Sustainability Advisor Engine
2. Personalized Sustainability Guidance
3. Priority Action Planner
4. Weekly Sustainability Planner
5. Monthly Sustainability Planner
6. Advisor Testing

Session 7 is complete only when the system can generate personalized sustainability coaching instead of static recommendations.
