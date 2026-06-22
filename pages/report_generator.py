import base64
import io

import pandas as pd
import streamlit as st

from reports.report_generator import (
    create_summary_data,
    generate_csv_report,
    generate_pdf_report,
)


st.set_page_config(
    page_title="EcoGen AI Report Generator",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #0f172a; }
    .block-container { padding-top: 1rem; }
    div[data-testid="stMetric"] {
        background: #0b1220;
        border: 1px solid #1e293b;
        border-radius: 0.8rem;
        padding: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("📄 Sustainability Report Generator")
st.write(
    "Create downloadable PDF and CSV sustainability reports for your eco profile."
)

# Build report data
report_data = create_summary_data()

# Report preview area
st.subheader("Report Preview")

preview_cols = st.columns(3)
with preview_cols[0]:
    st.metric("Sustainability Score", f"{report_data['sustainability_score']:.1f}")
with preview_cols[1]:
    st.metric(
        "Monthly Carbon Footprint",
        f"{report_data['carbon_footprint_summary']['monthly']} kg",
    )
with preview_cols[2]:
    st.metric(
        "Planner Completion",
        f"{report_data['planner_progress']['completion_percentage']}%",
    )

summary_df = pd.DataFrame(
    {
        "Section": [
            "User",
            "Energy Usage",
            "Water Usage",
            "Waste Management",
            "Rewards",
            "Community Contribution",
        ],
        "Value": [
            report_data["user"]["name"],
            f"{report_data['energy_usage_summary']['monthly_usage']} units",
            f"{report_data['water_usage_summary']['monthly_usage']} liters",
            f"{report_data['waste_management_summary']['monthly_waste']} kg",
            f"{report_data['rewards']['badge']} ({report_data['rewards']['points']} pts)",
            f"Rank #{report_data['community_contribution']['rank']}",
        ],
    }
)
st.dataframe(summary_df, use_container_width=True)

# Report generation status
st.subheader("Report Generation Status")
status_col1, status_col2 = st.columns(2)
with status_col1:
    st.success("Report data loaded successfully.")
with status_col2:
    st.info("Ready to export PDF and CSV files.")

# Download buttons
col1, col2 = st.columns(2)
with col1:
    try:
        pdf_bytes = generate_pdf_report(report_data)
        pdf_b64 = base64.b64encode(pdf_bytes).decode()
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="eco_sustainability_report.pdf",
            mime="application/pdf",
        )
    except Exception as exc:
        st.error(f"Unable to generate PDF: {exc}")

with col2:
    try:
        csv_bytes = generate_csv_report(report_data)
        st.download_button(
            label="Download CSV Summary",
            data=csv_bytes,
            file_name="eco_sustainability_summary.csv",
            mime="text/csv",
        )
    except Exception as exc:
        st.error(f"Unable to generate CSV: {exc}")

st.markdown("### Recommendations")
for item in report_data["recommendations"]:
    st.write(f"• {item}")

st.markdown("### Achievements")
for item in report_data["carbon_reduction_achievements"]:
    st.write(f"• {item}")
