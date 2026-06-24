from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    output_path,
    report_data,
):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "EcoGen AI Sustainability Report",
            styles["Title"],
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"EcoDNA Type: {report_data['EcoDNA']}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"Sustainability Score: {report_data['Score']}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"Carbon Footprint: {report_data['Footprint']} kg CO₂",
            styles["Normal"],
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Roadmap",
            styles["Heading2"],
        )
    )

    for item in report_data["Roadmap"]:

        elements.append(
            Paragraph(
                str(item),
                styles["Normal"],
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Missions",
            styles["Heading2"],
        )
    )

    for mission in report_data["Missions"]:

        elements.append(
            Paragraph(
                str(mission),
                styles["Normal"],
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Achievements",
            styles["Heading2"],
        )
    )

    for achievement in report_data["Achievements"]:

        elements.append(
            Paragraph(
                str(achievement),
                styles["Normal"],
            )
        )

    doc.build(elements)

    return output_path