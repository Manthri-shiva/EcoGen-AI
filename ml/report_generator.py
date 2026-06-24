"""
EcoGen AI Report Generator
"""


def generate_report_data(
    ecodna_type,
    sustainability_score,
    carbon_footprint,
    roadmap,
    missions,
    achievements,
):

    return {
        "EcoDNA": ecodna_type,
        "Score": sustainability_score,
        "Footprint": carbon_footprint,
        "Roadmap": roadmap,
        "Missions": missions,
        "Achievements": achievements,
    }