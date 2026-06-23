"""EcoGen AI - EcoTwin AI Digital Twin page."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ml.digital_twin import create_digital_twin_profile

st.set_page_config(
    page_title="EcoTwin AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
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

        forecast_data = [
            {"month": 0, "footprint": current_state["carbon_footprint"], "label": "Now"},
            {"month": 3, "footprint": predictions["3_months"]["projected_footprint"], "label": "3M"},
            {"month": 6, "footprint": predictions["6_months"]["projected_footprint"], "label": "6M"},
            {"month": 12, "footprint": predictions["12_months"]["projected_footprint"], "label": "12M"},
        ]
        forecast_df = pd.DataFrame(forecast_data)

        reduction_df = pd.DataFrame(
            {
                "month": [0, 3, 6, 12],
                "reduction": [
                    0.0,
                    current_state["carbon_footprint"] - predictions["3_months"]["projected_footprint"],
                    current_state["carbon_footprint"] - predictions["6_months"]["projected_footprint"],
                    current_state["carbon_footprint"] - predictions["12_months"]["projected_footprint"],
                ],
            }
        )

        forecast_chart = px.line(
            forecast_df,
            x="month",
            y="footprint",
            markers=True,
            title="Future Forecast",
            template="plotly_dark",
        )
        forecast_chart.update_traces(line=dict(color="#60A5FA", width=4), marker=dict(size=8, color="#34D399"))
        forecast_chart.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="var(--text)",
            margin=dict(l=0, r=0, t=45, b=0),
        )

        reduction_chart = px.area(
            reduction_df,
            x="month",
            y="reduction",
            title="Carbon Reduction Potential",
            template="plotly_dark",
            labels={"month": "Months", "reduction": "kg CO₂ reduced"},
        )
        reduction_chart.update_traces(fill="tozeroy", line=dict(color="#34D399"), marker=dict(color="#60A5FA"))
        reduction_chart.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="var(--text)",
            margin=dict(l=0, r=0, t=45, b=0),
        )

        score_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=current_state["sustainability_score"],
                number={"suffix": " /100"},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#9aa4b2"},
                    "bar": {"color": "#34d399" if current_state["sustainability_score"] >= 70 else ("#ffd24d" if current_state["sustainability_score"] >= 40 else "#ff6b6b")},
                    "steps": [
                        {"range": [0, 40], "color": "#ff6b6b"},
                        {"range": [40, 70], "color": "#ffd24d"},
                        {"range": [70, 100], "color": "#34d399"},
                    ],
                },
                title={"text": "Sustainability Health", "font": {"color": "#e5ecff"}},
            )
        )
        score_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5ecff",
            margin=dict(l=0, r=0, t=50, b=0),
        )

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Premium Dashboard</h2>", unsafe_allow_html=True)
        cards = st.columns(4, gap="large")
        cards[0].markdown(f"<div class='metric-card animated-card'><div class='metric-card__title'>Current Footprint</div><div class='metric-card__value'>{current_state['carbon_footprint']:.1f} kg CO₂</div><div class='metric-card__subtitle'>Baseline today</div></div>", unsafe_allow_html=True)
        cards[1].markdown(f"<div class='metric-card animated-card'><div class='metric-card__title'>3 Month Forecast</div><div class='metric-card__value'>{predictions['3_months']['projected_footprint']:.1f} kg CO₂</div><div class='metric-card__subtitle'>{predictions['3_months']['reduction_potential']:.1f} kg saved</div></div>", unsafe_allow_html=True)
        cards[2].markdown(f"<div class='metric-card animated-card'><div class='metric-card__title'>6 Month Forecast</div><div class='metric-card__value'>{predictions['6_months']['projected_footprint']:.1f} kg CO₂</div><div class='metric-card__subtitle'>{predictions['6_months']['reduction_potential']:.1f} kg saved</div></div>", unsafe_allow_html=True)
        cards[3].markdown(f"<div class='metric-card animated-card'><div class='metric-card__title'>12 Month Forecast</div><div class='metric-card__value'>{predictions['12_months']['projected_footprint']:.1f} kg CO₂</div><div class='metric-card__subtitle'>{predictions['12_months']['reduction_potential']:.1f} kg saved</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Forecast Visualizations</h2>", unsafe_allow_html=True)
        vis_col1, vis_col2 = st.columns([2.2, 1], gap="large")
        with vis_col1:
            st.plotly_chart(forecast_chart, use_container_width=True)
            st.plotly_chart(reduction_chart, use_container_width=True)
        with vis_col2:
            st.plotly_chart(score_gauge, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Location Insights</h2>", unsafe_allow_html=True)
        insight_cols = st.columns(2, gap="large")
        for idx, insight in enumerate(location_insights):
            render_insight_card(insight)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Recommended Actions</h2>", unsafe_allow_html=True)
        icons = ["⚡", "💧", "🌱", "🚲", "♻️"]
        for idx, recommendation in enumerate(recommendations):
            icon = icons[idx % len(icons)]
            render_recommendation_card(icon, recommendation, "Action guidance from your EcoTwin report.", "Priority: Recommended")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Provide your city, sustainability score, and current carbon footprint, then generate the EcoTwin report.")
