"""
EcoGen AI - Carbon Reduction Simulator UI

This page is intentionally separate from the calculation logic so the UI can be
changed independently without affecting the simulation engine.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from simulator.carbon_simulator import (
    ASSUMPTIONS,
    calculate_carbon_footprint,
    calculate_cost_savings,
    calculate_reduction,
    generate_insights,
)


st.set_page_config(
    page_title="EcoGen AI Simulator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Styling helpers
# ---------------------------------------------------------------------------

def render_kpi_card(title: str, value: str, delta: str = "", color: str = "#FFFFFF") -> None:
    """Render a compact KPI card for the simulator page."""
    st.markdown(
        f"""
        <div style="
            background-color: #0E1117;
            border: 1px solid #2E3A4F;
            border-radius: 0.75rem;
            padding: 0.9rem;
            margin-bottom: 0.9rem;
        ">
            <div style="font-size: 0.85rem; color: #9AA4B2;">{title}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{value}</div>
            <div style="font-size: 0.82rem; color: #60A5FA;">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar navigation placeholders
# ---------------------------------------------------------------------------

st.sidebar.title("EcoGen AI")
st.sidebar.caption("Sustainability Simulator")
nav_options = [
    "Dashboard",
    "Carbon Reduction Simulator",
    "AI Sustainability Advisor",
    "30-Day Green Planner",
    "RAG Sustainability Assistant",
    "Eco Rewards",
    "Community Analytics",
    "Reports",
    "Green Products",
]
st.sidebar.radio("Navigation", nav_options)


# ---------------------------------------------------------------------------
# Header section
# ---------------------------------------------------------------------------

st.title("🌍 Carbon Reduction Simulator")
st.caption(
    "Compare your current footprint with an improved scenario using sample assumptions."
)

with st.expander("Dummy assumptions used in this simulator", expanded=False):
    st.write(
        "- AC impact is estimated using daily hours × 0.45 kg CO₂ per hour × 30 days\n"
        "- Travel impact uses daily distance × 0.18 kg CO₂ per km × 30 days\n"
        "- Water and waste values use monthly liters/kg with simple conversion factors"
    )


# ---------------------------------------------------------------------------
# Input section
# ---------------------------------------------------------------------------

st.subheader("Scenario Inputs")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Current Values")
    current_ac = st.number_input(
        "Daily AC Usage (hours)",
        min_value=0.0,
        max_value=24.0,
        value=8.0,
        step=0.5,
    )
    current_travel = st.number_input(
        "Daily Travel Distance (km)",
        min_value=0.0,
        max_value=500.0,
        value=25.0,
        step=1.0,
    )
    current_water = st.number_input(
        "Monthly Water Consumption (liters)",
        min_value=0.0,
        max_value=30000.0,
        value=5000.0,
        step=100.0,
    )
    current_waste = st.number_input(
        "Monthly Waste Generated (kg)",
        min_value=0.0,
        max_value=500.0,
        value=15.0,
        step=1.0,
    )

with col_right:
    st.markdown("### Improved Values")
    improved_ac = st.number_input(
        "Daily AC Usage (hours)",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5,
    )
    improved_travel = st.number_input(
        "Daily Travel Distance (km)",
        min_value=0.0,
        max_value=500.0,
        value=18.0,
        step=1.0,
    )
    improved_water = st.number_input(
        "Monthly Water Consumption (liters)",
        min_value=0.0,
        max_value=30000.0,
        value=4000.0,
        step=100.0,
    )
    improved_waste = st.number_input(
        "Monthly Waste Generated (kg)",
        min_value=0.0,
        max_value=500.0,
        value=10.0,
        step=1.0,
    )


# ---------------------------------------------------------------------------
# Compute results
# ---------------------------------------------------------------------------

current_inputs = {
    "ac_usage_hours": current_ac,
    "travel_distance_km": current_travel,
    "water_consumption_liters": current_water,
    "waste_generated_kg": current_waste,
}

improved_inputs = {
    "ac_usage_hours": improved_ac,
    "travel_distance_km": improved_travel,
    "water_consumption_liters": improved_water,
    "waste_generated_kg": improved_waste,
}

current_result = calculate_carbon_footprint(**current_inputs)
improved_result = calculate_carbon_footprint(**improved_inputs)
reduction = calculate_reduction(current_result["total"], improved_result["total"])
savings = calculate_cost_savings(current_inputs, improved_inputs)
insights = generate_insights(current_inputs, improved_inputs)


# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------

st.subheader("Simulation Results")
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

with metric_col1:
    render_kpi_card(
        "Current Carbon Footprint",
        f"{current_result['total']:.2f} kg CO₂",
        "Current scenario",
    )
with metric_col2:
    render_kpi_card(
        "Simulated Carbon Footprint",
        f"{improved_result['total']:.2f} kg CO₂",
        "Improved scenario",
    )
with metric_col3:
    render_kpi_card(
        "Carbon Reduction",
        f"{reduction['reduction']:.2f} kg CO₂",
        "Absolute reduction",
    )
with metric_col4:
    render_kpi_card(
        "Percentage Reduction",
        f"{reduction['percentage']:.1f}%",
        "Improvement rate",
    )
with metric_col5:
    render_kpi_card(
        "Estimated Monthly Savings",
        f"${savings['total_savings']:.2f}",
        "Estimated savings",
    )


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    comparison_df = pd.DataFrame(
        {
            "Scenario": ["Current", "Improved"],
            "Total Carbon Footprint": [
                current_result["total"],
                improved_result["total"],
            ],
        }
    )
    st.plotly_chart(
        px.bar(
            comparison_df,
            x="Scenario",
            y="Total Carbon Footprint",
            color="Scenario",
            title="Current vs. Improved Carbon Footprint",
            template="plotly_dark",
        ),
        use_container_width=True,
    )

with chart_col2:
    category_df = pd.DataFrame(
        {
            "Category": ["Energy", "Transport", "Water", "Waste"],
            "Current": [
                current_result["energy"],
                current_result["transport"],
                current_result["water"],
                current_result["waste"],
            ],
            "Improved": [
                improved_result["energy"],
                improved_result["transport"],
                improved_result["water"],
                improved_result["waste"],
            ],
        }
    )
    st.plotly_chart(
        px.bar(
            category_df,
            x="Category",
            y=["Current", "Improved"],
            barmode="group",
            title="Category-wise Comparison",
            template="plotly_dark",
        ),
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Insights and recommendations
# ---------------------------------------------------------------------------

st.subheader("Insights")
for insight in insights:
    st.success(f"• {insight}")

with st.expander("Estimated savings breakdown"):
    st.write(
        f"Energy savings: ${savings['energy_savings']:.2f}"
    )
    st.write(
        f"Transport savings: ${savings['transport_savings']:.2f}"
    )
    st.write(
        f"Water savings: ${savings['water_savings']:.2f}"
    )
    st.write(
        f"Waste savings: ${savings['waste_savings']:.2f}"
    )

st.caption(
    "Note: All values are sample-based estimates for UI validation and can be replaced later with real analytics."
)
