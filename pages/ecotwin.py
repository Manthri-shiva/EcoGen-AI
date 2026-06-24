"""EcoGen AI - EcoTwin AI Digital Twin page."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st


st.set_page_config(
    page_title="EcoTwin AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# TEMPORARILY COMMENT THESE
# from utils.theme import apply_theme
# from utils.ui_components import (
#     hero_section,
#     status_badge
# )

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ml.digital_twin import create_digital_twin_profile

from ml.scenario_engine import simulate_scenario
from ml.recommendation_optimizer import (
    get_optimized_recommendations,
)

from ml.ecodna import (
    get_ecodna_type,
)

def render_metric_card(title: str, value: str, subtitle: str = "", accent: str = "#60A5FA") -> None:
    st.markdown(
        f"""
        <div class="metric-card animated-card">
            <div class="metric-card__title">{title}</div>
            <div class="metric-card__value">{value}</div>
            <div class="metric-card__subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_card(text: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-card__icon">📍</div>
            <div class="insight-card__text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(icon: str, title: str, details: str, priority: str) -> None:
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-card__icon">{icon}</div>
            <div class="recommendation-card__content">
                <div class="recommendation-card__title">{title}</div>
                <div class="recommendation-card__details">{details}</div>
                <div class="recommendation-card__priority">{priority}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    :root {
      --bg: #050b1d;
      --surface: rgba(10, 18, 38, 0.88);
      --surface-strong: rgba(10, 18, 38, 0.96);
      --border: rgba(96, 165, 250, 0.14);
      --text: #e5ecff;
      --muted: #9aa4b2;
      --accent: #60a5fa;
      --accent-2: #34d399;
      --danger: #fb7185;
      --shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
    }

    body {
        background: radial-gradient(circle at top left, rgba(96, 165, 250, 0.12), transparent 40%),
                    linear-gradient(180deg, #020617 0%, #081b34 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    .hero {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 1.5rem;
        background: linear-gradient(135deg, rgba(16, 47, 92, 0.96), rgba(3, 16, 38, 0.95));
        border: 1px solid rgba(96, 165, 250, 0.24);
        border-radius: 1.5rem;
        padding: 2rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.5rem;
    }
    .hero__text {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hero h1 {
        margin: 0;
        font-size: clamp(2.4rem, 4vw, 3.6rem);
        letter-spacing: -0.07em;
    }
    .hero p {
        margin: 1rem 0 0;
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 55rem;
    }
    .hero__badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 1.4rem;
    }
    .hero__badge {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: var(--text);
        padding: 0.8rem 1rem;
        border-radius: 999px;
        font-size: 0.95rem;
    }

    .animated-card {
        animation: float 8s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    .metric-card,
    .insight-card,
    .recommendation-card,
    .section-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 1.4rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(18px);
    }

    .metric-card {
        padding: 1.3rem;
        min-height: 150px;
    }
    .metric-card__title {
        color: var(--muted);
        letter-spacing: 0.02em;
        margin-bottom: 0.65rem;
    }
    .metric-card__value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text);
    }
    .metric-card__subtitle {
        margin-top: 0.75rem;
        color: var(--accent);
        font-size: 0.95rem;
    }

    .insight-card {
        display: flex;
        gap: 0.85rem;
        padding: 1rem 1rem 1rem 1rem;
        margin-bottom: 1rem;
    }
    .insight-card__icon {
        width: 44px;
        height: 44px;
        border-radius: 16px;
        background: rgba(96, 165, 250, 0.16);
        display: grid;
        place-items: center;
        font-size: 1.2rem;
    }
    .insight-card__text {
        color: var(--text);
        line-height: 1.65;
    }

    .recommendation-card {
        display: grid;
        grid-template-columns: 50px 1fr;
        gap: 1rem;
        padding: 1rem 1rem 1rem 1rem;
        margin-bottom: 1rem;
    }
    .recommendation-card__icon {
        width: 50px;
        height: 50px;
        border-radius: 18px;
        display: grid;
        place-items: center;
        background: linear-gradient(180deg, rgba(52, 211, 153, 0.24), rgba(96, 165, 250, 0.14));
        font-size: 1.35rem;
    }
    .recommendation-card__content {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }
    .recommendation-card__title {
        font-size: 1rem;
        font-weight: 700;
    }
    .recommendation-card__details {
        color: var(--muted);
        line-height: 1.6;
    }
    .recommendation-card__priority {
        color: var(--accent);
        font-size: 0.9rem;
        font-weight: 600;
    }

    .section-card {
        padding: 1.5rem;
        margin-bottom: 1.3rem;
    }

    .section-title {
        margin-bottom: 1rem;
        color: var(--text);
    }

    .form-column {
        gap: 1.2rem;
    }

    .glass-panel {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 1.2rem;
        padding: 1.4rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(16px);
    }

    .button-primary button {
        background: linear-gradient(135deg, #60a5fa, #34d399);
        border: none;
        color: #fff;
        font-weight: 700;
    }

    @media screen and (max-width: 1024px) {
        .hero {
            grid-template-columns: 1fr;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    @media screen and (max-width: 720px) {
        .hero {
            padding: 1.4rem;
        }

        .metric-card,
        .insight-card,
        .recommendation-card,
        .section-card {
            border-radius: 1rem;
        }

        .recommendation-card {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="hero__text">
        <h1>🌍 EcoTwin AI</h1>
        <p>Premium digital twin insights for carbon, sustainability, and location-aware action planning.</p>
        <div class="hero__badges">
          <div class="hero__badge">Dark Mode Dashboard</div>
          <div class="hero__badge">Forecast Intelligence</div>
          <div class="hero__badge">Location-aware Advice</div>
        </div>
      </div>
      <div class="glass-panel">
        <div style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
          <div style="min-width:180px;">
            <div style="font-size:0.95rem; color:var(--muted);">Current Footprint</div>
            <div style="font-size:2rem; font-weight:700; color:var(--text);">420 kg CO₂</div>
          </div>
          <div style="min-width:180px;">
            <div style="font-size:0.95rem; color:var(--muted);">Sustainability Score</div>
            <div style="font-size:2rem; font-weight:700; color:var(--accent);">58 / 100</div>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("ecotwin_form"):
    col_left, col_right = st.columns([1.7, 1])

    with col_left:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Inputs")
        city = st.selectbox(
            "City",
            options=["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi", "Pune", "Kolkata"],
            index=0,
        )
        sustainability_score = st.slider(
            "Sustainability Score",
            min_value=0,
            max_value=100,
            value=58,
            help="Your current sustainability performance on a 0-100 scale.",
        )
        current_footprint = st.number_input(
            "Current Carbon Footprint (kg CO₂)",
            min_value=0.0,
            value=420.0,
            step=10.0,
            format="%.1f",
        )

        st.markdown("---")
        st.subheader("Profile Snapshot")
        age = st.number_input("Age", min_value=0, max_value=120, value=34, step=1)
        household_size = st.number_input("Household size", min_value=1, max_value=10, value=4, step=1)
        notes = st.text_area(
            "Optional Notes",
            value="Household uses a mix of grid power and public transit.",
            height=88,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Current State")
        render_metric_card("City", city, "Selected location")
        render_metric_card("Footprint", f"{current_footprint:.1f} kg CO₂", "Current monthly footprint")
        render_metric_card("Score", f"{sustainability_score} / 100", "Current sustainability rating")
        st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("Generate EcoTwin Report")

if submitted:
    user_profile = {
        "age": age,
        "household_size": household_size,
        "city": city,
        "current_footprint": current_footprint,
        "sustainability_score": sustainability_score,
        "optional_notes": notes,
    }

    try:
        twin_report = create_digital_twin_profile(
            user_profile=user_profile,
            carbon_footprint=current_footprint,
            sustainability_score=sustainability_score,
            city=city,
        )
    except Exception as exc:
        st.error(f"Unable to generate EcoTwin profile: {exc}")
        twin_report = None

    
    if twin_report:

        current_state = twin_report["current_state"]
        predictions = twin_report["future_predictions"]
        recommendations = twin_report["recommendations"]
        location_insights = twin_report["location_insights"]

        ecodna_type = get_ecodna_type(
            electricity=float(
                current_state["user_profile"].get(
                    "monthly_electricity_usage",
                    0,
                )
            ),
            water=float(
                current_state["user_profile"].get(
                    "monthly_water_consumption",
                    0,
                )
            ),
            travel=float(
                current_state["user_profile"].get(
                    "daily_travel_distance",
                    0,
                )
            ),
            waste=float(
                current_state["user_profile"].get(
                    "monthly_waste_generated",
                    0,
                )
            ),
        )

        optimized_recommendations = get_optimized_recommendations(
            electricity=float(
                current_state["user_profile"].get(
                    "monthly_electricity_usage",
                    0,
                )
            ),
            water=float(
                current_state["user_profile"].get(
                    "monthly_water_consumption",
                    0,
                )
            ),
            travel=float(
                current_state["user_profile"].get(
                    "daily_travel_distance",
                    0,
                )
            ),
            waste=float(
                current_state["user_profile"].get(
                    "monthly_waste_generated",
                    0,
                )
            ),
        )

        forecast_data = [
            {
                "month": 0,
                "footprint": current_state["carbon_footprint"],
            },
            {
                "month": 3,
                "footprint": predictions["3_months"]["projected_footprint"],
            },
            {
                "month": 6,
                "footprint": predictions["6_months"]["projected_footprint"],
            },
            {
                "month": 12,
                "footprint": predictions["12_months"]["projected_footprint"],
            },
        ]

        forecast_df = pd.DataFrame(forecast_data)

        forecast_chart = px.line(
            forecast_df,
            x="month",
            y="footprint",
            markers=True,
            title="Future Forecast",
        )

        st.subheader("📊 Premium Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Current Footprint",
            f"{current_state['carbon_footprint']:.1f} kg",
        )

        col2.metric(
            "3 Month Forecast",
            f"{predictions['3_months']['projected_footprint']:.1f} kg",
        )

        col3.metric(
            "6 Month Forecast",
            f"{predictions['6_months']['projected_footprint']:.1f} kg",
        )

        col4.metric(
            "12 Month Forecast",
            f"{predictions['12_months']['projected_footprint']:.1f} kg",
        )

        st.subheader("🧬 EcoDNA Profile")

        st.success(
            f"Your EcoDNA Type: {ecodna_type}"
        )

        st.subheader("📈 Forecast Visualizations")

        st.plotly_chart(
            forecast_chart,
            use_container_width=True,
        )

        st.subheader("📍 Location Insights")

        for insight in location_insights:
            st.info(insight)

        st.subheader("🌱 Recommended Actions")

        for recommendation in recommendations:
            st.success(recommendation)

        st.subheader("🤖 AI Priority Recommendations")

        for rec in optimized_recommendations:

            st.info(
                f"""
    {rec['title']}

    Priority Score: {rec['priority_score']}

    Carbon Saving: {rec['carbon_saving']} kg/month
    """
            )

        total_savings = sum(
            rec["carbon_saving"]
            for rec in optimized_recommendations
        )

        projected_footprint = max(
            current_state["carbon_footprint"]
            - total_savings,
            0,
        )

        st.subheader("📈 Impact Forecast")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Carbon",
            f"{current_state['carbon_footprint']:.1f} kg",
        )

        col2.metric(
            "Projected Carbon",
            f"{projected_footprint:.1f} kg",
        )

        col3.metric(
            "Potential Savings",
            f"{total_savings:.1f} kg",
        )

        st.subheader("🔮 What-If Scenario Simulator")

        st.info(
            "Scenario simulator temporarily disabled while EcoTwin upgrade is being integrated."
        )

    else:

        st.info(
            "Provide your city, sustainability score, and current carbon footprint, then generate the EcoTwin report."
        )