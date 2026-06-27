import streamlit as st
from utils.theme import apply_theme
from chatbot.sustainability_advisor import generate_advice_report
from ml.location.location_engine import (
    generate_location_report,
    generate_location_recommendations,
    generate_location_insights,
)


st.set_page_config(
    page_title="EcoGen AI Advisor",
    page_icon="🌿",
    layout="wide",
)
apply_theme()

st.markdown(
    """
    <style>
    :root{
      --bg-1: #0f172a;
      --glass-bg: rgba(255,255,255,0.04);
      --glass-border: rgba(255,255,255,0.06);
      --accent: #60a5fa;
      --card-gradient-1: linear-gradient(135deg,#042a2b 0%, #0b1220 100%);
    }
    body { background: var(--bg-1); }
    .block-container { padding-top: 1rem; }

    /* Hero banner */
    .hero {
        background: linear-gradient(90deg, rgba(2,6,23,0.95), rgba(6,30,50,0.9));
        background-image: linear-gradient(90deg, #0f172a 0%, #042a2b 50%, #0b1220 100%);
        border-radius: 0.9rem;
        padding: 2rem;
        margin-bottom: 1rem;
        color: #e6eef8;
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    }
    .hero h1 { margin: 0; font-size: 2.1rem; letter-spacing: -0.5px; }
    .hero p { margin: 0.25rem 0 0; color: #bcd7ff; opacity: 0.9; }

    /* Glassmorphism for metrics */
    div[data-testid="stMetric"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 0.75rem;
        padding: 0.8rem;
        backdrop-filter: blur(6px) saturate(120%);
        box-shadow: 0 4px 24px rgba(2,6,23,0.6);
    }

    /* Recommendation cards */
    .recommendation-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 0.9rem;
        padding: 1rem;
        margin-bottom: 0.9rem;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }
    .rec-icon {
        font-size: 1.8rem;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0.6rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        box-shadow: 0 6px 18px rgba(2,6,23,0.5) inset;
    }
    .rec-body { flex: 1; }
    .rec-title { margin: 0 0 0.25rem 0; font-size: 1.05rem; }
    .rec-desc { margin: 0; color: #cbd5e1; }
    .rec-meta { margin-top: 0.5rem; display:flex; gap:0.5rem; align-items:center; }

    /* Priority badges */
    .priority { padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-weight:600; font-size:0.85rem; }
    .priority-high { background: linear-gradient(90deg,#ff8a00,#ff3b30); color: #1b0b00; }
    .priority-medium { background: linear-gradient(90deg,#ffd24d,#ffb703); color:#2d1600; }
    .priority-low { background: linear-gradient(90deg,#a7f3d0,#34d399); color:#052210; }

    </style>
    """,
    unsafe_allow_html=True,
)

# Hero section
st.markdown(
    """
    <div class="hero">
      <h1>AI Sustainability Advisor</h1>
      <p>Personalized sustainability intelligence powered by EcoGen AI</p>
    </div>
    """,
    unsafe_allow_html=True,
)


if "advisor_result" not in st.session_state:
    st.session_state.advisor_result = None


st.title("🌱 AI Sustainability Advisor")
st.write(
    "Get personalized sustainability guidance based on your profile, usage patterns, and goals."
)

with st.sidebar:
    st.header("Advisor Inputs")
    st.caption("Use the form below to generate coaching insights.")
    st.markdown("---")
    selected_city = st.selectbox(
        "Select your city",
        ["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi", "Pune", "Kolkata"],
        index=0,
    )

col1, col2 = st.columns(2)

with col1:
    monthly_electricity_usage = st.number_input(
        "Monthly electricity usage (units)",
        min_value=0.0,
        value=250.0,
        step=10.0,
    )
    monthly_water_consumption = st.number_input(
        "Monthly water consumption (liters)",
        min_value=0.0,
        value=6000.0,
        step=100.0,
    )
    daily_travel_distance = st.number_input(
        "Daily travel distance (km)",
        min_value=0.0,
        value=25.0,
        step=1.0,
    )

with col2:
    monthly_waste_generated = st.number_input(
        "Monthly waste generated (kg)",
        min_value=0.0,
        value=15.0,
        step=1.0,
    )
    sustainability_score = st.slider(
        "Sustainability score",
        min_value=0,
        max_value=100,
        value=68,
    )
    goal = st.selectbox(
        "Primary goal",
        ["Reduce emissions", "Save energy", "Save water", "Lower waste", "Improve lifestyle"],
    )

if st.button("Generate AI Advice", use_container_width=True):
    inputs = {
        "monthly_electricity_usage": monthly_electricity_usage,
        "monthly_water_consumption": monthly_water_consumption,
        "daily_travel_distance": daily_travel_distance,
        "monthly_waste_generated": monthly_waste_generated,
        "sustainability_score": sustainability_score,
        "goal": goal,
    }

    try:
        with st.spinner("Analyzing your profile with Gemini..."):
            result = generate_advice_report(inputs)
        st.session_state.advisor_result = result
        # Generate location intelligence report for the selected city
        try:
            location_report = generate_location_report(selected_city)
            st.session_state.location_report = location_report
        except Exception as _loc_exc:
            st.session_state.location_report = None
    except Exception as exc:
        st.error(f"Unable to generate advice right now: {exc}")
        st.session_state.advisor_result = None

if st.session_state.advisor_result:
    result = st.session_state.advisor_result

    st.subheader("Advisor Summary")
    st.success(result.get("summary", "AI-generated sustainability guidance."))

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Estimated savings", result.get("estimated_cost_savings", "$0"))
    with col_b:
        st.metric("Priority focus", result["recommendations"][0].get("priority", "High") if result.get("recommendations") else "High")
    with col_c:
        st.metric("Recommendation count", len(result.get("recommendations", [])))

    st.markdown("### Expected Environmental Impact")
    st.info(result.get("expected_environmental_impact", "Positive sustainability impact."))

    # -----------------------------------------------------------------------
    # Location Intelligence (render if available)
    # -----------------------------------------------------------------------
    if st.session_state.get("location_report"):
        loc = st.session_state.location_report
        profile = loc.get("location_profile", {})
        loc_recs = loc.get("recommendations", [])
        loc_insights = loc.get("insights", [])

        st.subheader("📍 Location Intelligence")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-body\"><div class=\"rec-title\">Solar Potential</div><div class=\"rec-desc\">{profile.get('solar_potential', 'N/A')}</div></div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-body\"><div class=\"rec-title\">Public Transport</div><div class=\"rec-desc\">{profile.get('public_transport', 'N/A')}</div></div></div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-body\"><div class=\"rec-title\">Water Scarcity</div><div class=\"rec-desc\">{profile.get('water_scarcity', 'N/A')}</div></div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-body\"><div class=\"rec-title\">Waste Management</div><div class=\"rec-desc\">{profile.get('waste_management', 'N/A')}</div></div></div>",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-body\"><div class=\"rec-title\">Air Pollution</div><div class=\"rec-desc\">{profile.get('air_pollution', 'N/A')}</div></div></div>",
                unsafe_allow_html=True,
            )

        # Location recommendations as cards
        st.markdown("### Location Recommendations")
        for rec in loc_recs:
            st.markdown(
                f"<div class=\"recommendation-card\"><div class=\"rec-icon\">🌍</div><div class=\"rec-body\"><div class=\"rec-desc\">{rec}</div></div></div>",
                unsafe_allow_html=True,
            )

        # Insights in expander
        with st.expander("Location Insights"):
            for insight in loc_insights:
                st.info(f"• {insight}")

    st.markdown("### Recommended Actions")
    icons = {
        "Energy": "⚡",
        "Transport": "🚲",
        "Water": "💧",
        "Waste": "♻️",
        "Lifestyle": "🌱",
    }
    priority_class = {
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low",
    }

    for item in result.get("recommendations", []):
        cat = item.get('category', 'General')
        icon = icons.get(cat, '🌿')
        pr = str(item.get('priority', 'Medium')).title()
        pr_class = priority_class.get(pr, 'priority-medium')

        with st.container():
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="rec-icon">{icon}</div>
                    <div class="rec-body">
                        <div class="rec-title"><strong>{item.get('rank', '')}. {cat}</strong> <span class="priority {pr_class}">{pr}</span></div>
                        <div class="rec-desc">{item.get('recommendation', '')}</div>
                        <div class="rec-meta">
                            <div><strong>Impact:</strong> {item.get('expected_impact', '')}</div>
                            <div><strong>Estimated savings:</strong> {item.get('estimated_cost_savings', '')}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info(
        "Click 'Generate AI Advice' to see personalized sustainability recommendations."
    )
