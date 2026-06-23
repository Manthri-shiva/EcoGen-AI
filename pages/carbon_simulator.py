"""
EcoGen AI - Carbon Reduction Simulator UI

This page is intentionally separate from the calculation logic so the UI can be
changed independently without affecting the simulation engine.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from simulator.carbon_simulator import (
    ASSUMPTIONS,
    calculate_carbon_footprint,
    calculate_cost_savings,
    calculate_reduction,
    calculate_sustainability_score,
    generate_insights,
)
from ml.location.location_engine import (
    get_location_profile,
    generate_location_insights,
    generate_location_recommendations,
)
from ml.prediction.predict import predict_carbon_footprint


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
# AI Carbon Footprint Predictor Section
# ---------------------------------------------------------------------------

st.subheader("🤖 AI Carbon Footprint Predictor")
st.caption("Get an AI-powered prediction based on your lifestyle inputs.")

with st.form("ml_predictor_form"):
    pred_col_left, pred_col_right = st.columns(2)
    
    with pred_col_left:
        ml_age = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=120,
            value=30,
            step=1,
        )
        ml_family_size = st.number_input(
            "Family Size (people)",
            min_value=1,
            max_value=20,
            value=4,
            step=1,
        )
        ml_electricity_bill = st.number_input(
            "Monthly Electricity Bill (₹)",
            min_value=0.0,
            max_value=50000.0,
            value=2000.0,
            step=100.0,
        )
    
    with pred_col_right:
        ml_water_usage = st.number_input(
            "Monthly Water Usage (liters)",
            min_value=0.0,
            max_value=100000.0,
            value=5000.0,
            step=100.0,
        )
        ml_daily_travel_km = st.number_input(
            "Daily Travel Distance (km)",
            min_value=0.0,
            max_value=500.0,
            value=20.0,
            step=1.0,
        )
        ml_waste_generated = st.number_input(
            "Monthly Waste Generated (kg)",
            min_value=0.0,
            max_value=500.0,
            value=25.0,
            step=1.0,
        )
    
    ml_predict_button = st.form_submit_button("🔮 Predict Carbon Footprint", use_container_width=True)

if ml_predict_button:
    try:
        predicted_footprint = predict_carbon_footprint(
            age=ml_age,
            family_size=ml_family_size,
            electricity_bill=ml_electricity_bill,
            water_usage=ml_water_usage,
            daily_travel_km=ml_daily_travel_km,
            waste_generated=ml_waste_generated
        )
        
        st.success(f"🌍 Predicted Carbon Footprint: **{predicted_footprint:.2f} kg CO₂**")
    
    except Exception as error:
        st.error(f"Prediction failed: {error}")


# ---------------------------------------------------------------------------
# Location Selection
# ---------------------------------------------------------------------------

st.subheader("📍 Location Selection")
selected_city = st.selectbox(
    "Select your city",
    options=["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi", "Pune", "Kolkata"],
    index=0,  # Default to Hyderabad
)

# Load location profile for selected city
location_profile = get_location_profile(selected_city)


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
# Sustainability scores
# ---------------------------------------------------------------------------

score_col1, score_col2, score_col3 = st.columns(3)

current_score = calculate_sustainability_score(current_result["total"])
improved_score = calculate_sustainability_score(improved_result["total"]) 
score_diff = improved_score - current_score

with score_col1:
    render_kpi_card(
        "Current Score",
        f"{current_score} / 100",
        "Current scenario",
        color="#FACC15",
    )
with score_col2:
    render_kpi_card(
        "Improved Score",
        f"{improved_score} / 100",
        "Improved scenario",
        color="#34D399",
    )
with score_col3:
    delta_sign = "+" if score_diff >= 0 else ""
    render_kpi_card(
        "Score Improvement",
        f"{delta_sign}{score_diff} pts",
        "Change",
        color="#60A5FA",
    )


# ---------------------------------------------------------------------------
# Sustainability Score Gauges
# ---------------------------------------------------------------------------

g_col1, g_col2 = st.columns(2)

# Gauge for Current Score
fig_current = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=current_score,
        number={'suffix': ' /100'},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9AA4B2"},
            'bar': {'color': "#34D399" if current_score >= 70 else ("#FFD24D" if current_score >= 40 else "#FF6B6B")},
            'bgcolor': "#071022",
            'steps': [
                {'range': [0, 40], 'color': '#ff6b6b'},
                {'range': [40, 70], 'color': '#ffd24d'},
                {'range': [70, 100], 'color': '#34d399'},
            ],
        },
        title={'text': "Current Sustainability Score", 'font': {'color': '#e6eef8'}}
    )
)
fig_current.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e6eef8', margin=dict(l=20, r=20, t=50, b=20))

# Gauge for Improved Score
fig_improved = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=improved_score,
        number={'suffix': ' /100'},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9AA4B2"},
            'bar': {'color': "#34D399" if improved_score >= 70 else ("#FFD24D" if improved_score >= 40 else "#FF6B6B")},
            'bgcolor': "#071022",
            'steps': [
                {'range': [0, 40], 'color': '#ff6b6b'},
                {'range': [40, 70], 'color': '#ffd24d'},
                {'range': [70, 100], 'color': '#34d399'},
            ],
        },
        title={'text': "Improved Sustainability Score", 'font': {'color': '#e6eef8'}}
    )
)
fig_improved.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e6eef8', margin=dict(l=20, r=20, t=50, b=20))

with g_col1:
    st.plotly_chart(fig_current, use_container_width=True)
with g_col2:
    st.plotly_chart(fig_improved, use_container_width=True)


# ---------------------------------------------------------------------------
# Location Intelligence Section
# ---------------------------------------------------------------------------

st.subheader("📍 Location Intelligence")
loc_col1, loc_col2, loc_col3 = st.columns(3)

with loc_col1:
    render_kpi_card(
        "City",
        selected_city,
        "Selected location",
    )
    render_kpi_card(
        "Solar Potential",
        location_profile["solar_potential"],
        "Renewable energy opportunity",
    )
    render_kpi_card(
        "Public Transport",
        location_profile["public_transport"],
        "Commute options",
    )

with loc_col2:
    render_kpi_card(
        "Water Scarcity",
        location_profile["water_scarcity"],
        "Water availability",
    )
    render_kpi_card(
        "Waste Management",
        location_profile["waste_management"],
        "Waste handling infrastructure",
    )

with loc_col3:
    render_kpi_card(
        "Air Pollution",
        location_profile["air_pollution"],
        "Air quality level",
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
# Future Carbon Projection
# ---------------------------------------------------------------------------

st.subheader("🔮 Future Carbon Projection")
st.caption("Projected carbon footprint using the improved scenario as a baseline and assuming a 2% monthly improvement.")

# Baseline is the improved scenario total
improved_baseline = improved_result["total"]

# Build monthly projection for 0..12 months
months = list(range(0, 13))  # 0 to 12
projected_values = [improved_baseline * (0.98 ** m) for m in months]
proj_df = pd.DataFrame({"month": months, "footprint": projected_values})

fig_proj = px.line(
    proj_df,
    x="month",
    y="footprint",
    title="Projected Carbon Footprint (2% monthly improvement)",
    markers=True,
    template="plotly_dark",
)
fig_proj.update_traces(line=dict(color="#60A5FA"), marker=dict(size=6, color="#60A5FA"))
fig_proj.update_layout(
    xaxis_title="Months",
    yaxis_title="kg CO₂",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#e6eef8',
    margin=dict(l=20, r=20, t=50, b=20),
)

# Annotate the 3,6,12 month projections
for m in (3, 6, 12):
    val = improved_baseline * (0.98 ** m)
    fig_proj.add_scatter(x=[m], y=[val], mode='markers+text', marker=dict(size=10, color='#34D399'), text=[f"{val:.1f}"], textposition='top center', showlegend=False)

st.plotly_chart(fig_proj, use_container_width=True)

# Projection cards for 3, 6, 12 months
val_3m = improved_baseline * (0.98 ** 3)
val_6m = improved_baseline * (0.98 ** 6)
val_12m = improved_baseline * (0.98 ** 12)

proj_col1, proj_col2, proj_col3 = st.columns(3)
with proj_col1:
    render_kpi_card(
        "3 Months Projection",
        f"{val_3m:.2f} kg CO₂",
        f"{((improved_baseline - val_3m)/improved_baseline*100):.1f}% reduction",
        color="#60A5FA",
    )
with proj_col2:
    render_kpi_card(
        "6 Months Projection",
        f"{val_6m:.2f} kg CO₂",
        f"{((improved_baseline - val_6m)/improved_baseline*100):.1f}% reduction",
        color="#34D399",
    )
with proj_col3:
    render_kpi_card(
        "12 Months Projection",
        f"{val_12m:.2f} kg CO₂",
        f"{((improved_baseline - val_12m)/improved_baseline*100):.1f}% reduction",
        color="#10B981",
    )


# ---------------------------------------------------------------------------
# Location Insights
# ---------------------------------------------------------------------------

st.subheader("🌱 Location Insights")
location_insights = generate_location_insights(selected_city)
for insight in location_insights:
    st.info(f"• {insight}")


# ---------------------------------------------------------------------------
# Location Recommendations
# ---------------------------------------------------------------------------

st.subheader("💡 Location Recommendations")
location_recommendations = generate_location_recommendations(selected_city)
for recommendation in location_recommendations:
    st.success(f"• {recommendation}")


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
