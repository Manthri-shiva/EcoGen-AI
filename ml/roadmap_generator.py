def generate_roadmap(score, footprint):

    roadmap = []

    if score < 40:
        roadmap.append(
            {
                "week": 1,
                "goal": "Reduce electricity consumption by 10%"
            }
        )

    roadmap.extend(
        [
            {
                "week": 2,
                "goal": "Reduce daily travel emissions"
            },
            {
                "week": 3,
                "goal": "Reduce household waste by 20%"
            },
            {
                "week": 4,
                "goal": "Improve sustainability score by 5 points"
            }
        ]
    )

    return roadmap