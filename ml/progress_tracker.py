"""
EcoGen AI Progress Tracker
"""


def generate_progress_history(
    current_footprint,
    reduction_rate=0.07,
):

    history = []

    footprint = current_footprint

    for week in range(1, 5):

        history.append(
            {
                "week": f"Week {week}",
                "footprint": round(
                    footprint,
                    2,
                ),
            }
        )

        footprint *= (
            1 - reduction_rate
        )

    return history