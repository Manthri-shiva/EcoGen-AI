# EcoGen AI - Session 2 Requirements

## Project Overview

EcoGen AI is an AI-powered Sustainability Intelligence Platform that helps users measure, analyze, and improve their environmental impact.

Current completed modules:

* Sustainability Profiling Engine
* Carbon Footprint Calculation Engine
* Sustainability Scoring Engine
* Database Schema
* Unit Tests

## Session 1 Status

Completed:

* database/schema/schema.sql
* ml/profiling/profiling_engine.py
* ml/carbon/carbon_engine.py
* ml/scoring/scoring_engine.py
* tests/test_carbon.py
* tests/test_scoring.py

Verified:

* Carbon footprint calculations working
* Sustainability score calculations working
* Package imports working
* Unit tests passing

## Session 2 Objective

Build Data Persistence Layer using SQLite.

Required Flow:

User Profile
→ Save to SQLite
→ Retrieve from SQLite
→ Calculate Carbon Footprint
→ Store Carbon Results
→ Return Structured Data

## Files Allowed To Modify

database/sqlite/
database/models/
ml/profiling/
tests/

## Files Not Allowed To Modify

ml/carbon/
ml/scoring/
app/
rag/
genai/

These modules are already implemented or belong to other team members.

## Session 2 Deliverables

1. DatabaseManager class
2. SQLite connection management
3. Insert user functionality
4. Insert profile functionality
5. Retrieve profile functionality
6. Store carbon result functionality
7. Database integration testing

## Coding Standards

* Python 3.11+
* OOP design
* Type hints where possible
* No hardcoded values
* Clear docstrings
* Modular architecture
* Production-ready code

## Success Criteria

The following should work:

Create User
↓
Create Profile
↓
Save Profile
↓
Retrieve Profile
↓
Calculate Carbon Footprint
↓
Save Carbon Data
↓
Return Results

All functionality must be testable using automated test scripts.
