import streamlit as st

from chatbot.sustainability_advisor import generate_advice_report


st.set_page_config(
    page_title="EcoGen AI Advisor",
    page_icon="🌿",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main { background: #0f172a; }
    .block-container { padding-top: 1rem; }
    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 0.75rem;
        padding: 0.8rem;
    }
    .recommendation-card {
        background: linear-gradient(180deg, #0b1220, #132238);
        border: 1px solid #1e3a5f;
        border-radius: 0.9rem;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    </style>
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

    st.markdown("### Recommended Actions")
    for item in result.get("recommendations", []):
        with st.container():
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <h4>{item.get('rank', '')}. {item.get('category', 'General')}</h4>
                    <p>{item.get('recommendation', '')}</p>
                    <p><strong>Priority:</strong> {item.get('priority', '')}</p>
                    <p><strong>Expected impact:</strong> {item.get('expected_impact', '')}</p>
                    <p><strong>Estimated savings:</strong> {item.get('estimated_cost_savings', '')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info(
        "Click 'Generate AI Advice' to see personalized sustainability recommendations."
    )
