import json

import plotly.graph_objects as go
import streamlit as st
from utils.theme import apply_theme
from planner.action_planner import (
    calculate_progress,
    estimate_impact,
    generate_action_plan,
    save_plan,
)


st.set_page_config(
    page_title="EcoGen AI Green Planner",
    page_icon="🌿",
    layout="wide",
)
apply_theme()

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
    .week-card {
        background: linear-gradient(180deg, #0c1324, #102540);
        border: 1px solid #1e3a5f;
        border-radius: 0.9rem;
        padding: 1rem;
        margin-bottom: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "planner_plan" not in st.session_state:
    st.session_state.planner_plan = None

if "planner_task_status" not in st.session_state:
    st.session_state.planner_task_status = {}


st.title("🌱 30-Day Green Action Planner")
st.write(
    "Build a personalized sustainability plan and track your weekly progress."
)

with st.sidebar:
    st.header("Planner Inputs")
    sustainability_score = st.slider(
        "Sustainability Score",
        min_value=0,
        max_value=100,
        value=68,
    )
    monthly_carbon_footprint = st.number_input(
        "Monthly Carbon Footprint (kg CO2)",
        min_value=0.0,
        value=1800.0,
        step=50.0,
    )
    monthly_electricity_usage = st.number_input(
        "Monthly Electricity Usage (units)",
        min_value=0.0,
        value=320.0,
        step=10.0,
    )
    monthly_water_consumption = st.number_input(
        "Monthly Water Consumption (liters)",
        min_value=0.0,
        value=6500.0,
        step=100.0,
    )
    sustainability_goal = st.text_input(
        "Sustainability Goal",
        value="Reduce my carbon footprint and save monthly costs",
    )

    if st.button("Generate 30-Day Action Plan", use_container_width=True):
        inputs = {
            "sustainability_score": sustainability_score,
            "monthly_carbon_footprint": monthly_carbon_footprint,
            "monthly_electricity_usage": monthly_electricity_usage,
            "monthly_water_consumption": monthly_water_consumption,
            "sustainability_goal": sustainability_goal,
        }

        try:
            with st.spinner("Creating your personalized 30-day plan..."):
                plan = generate_action_plan(inputs)
            st.session_state.planner_plan = plan
            st.session_state.planner_task_status = {}
            st.success("Plan generated successfully.")
        except Exception as exc:
            st.error(f"Unable to generate action plan: {exc}")
            st.session_state.planner_plan = None


if st.session_state.planner_plan:
    plan = st.session_state.planner_plan
    progress = calculate_progress(
        plan,
        st.session_state.planner_task_status,
    )
    impact = estimate_impact(plan)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Progress", f"{progress['overall_percentage']}%")
    with col2:
        st.metric(
            "Tasks Completed",
            f"{progress['completed_tasks']} / {progress['total_tasks']}",
        )
    with col3:
        st.metric(
            "Expected Reduction",
            plan["summary"].get("total_expected_reduction", "0%"),
        )
    with col4:
        st.metric(
            "Expected Savings",
            plan["summary"].get("total_expected_savings", "$0"),
        )

    st.markdown("### Goal Achievement Progress")
    st.progress(progress["overall_percentage"] / 100)

    # Save plan button
    if st.button("Save Plan", use_container_width=True):
        try:
            saved_path = save_plan(plan)
            st.success(f"Plan saved to: {saved_path}")
        except Exception as exc:
            st.error(f"Unable to save plan: {exc}")

    # Weekly cards with tasks and progress indicators.
    st.markdown("### Weekly Breakdown")
    for week in plan.get("weeks", []):
        week_number = week.get("week", 1)
        week_title = week.get("title", f"Week {week_number} Goals")
        tasks = week.get("tasks", [])

        with st.container():
            st.markdown(
                f"""
                <div class="week-card">
                    <h4>{week_title}</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.caption("Expected Reduction")
                st.write(week.get("expected_carbon_reduction", "0%"))
            with col_b:
                st.caption("Expected Savings")
                st.write(week.get("expected_cost_savings", "$0"))
            with col_c:
                st.caption("Difficulty")
                st.write(week.get("difficulty_level", "Medium"))
            with col_d:
                st.caption("Priority")
                st.write(week.get("priority", "Medium"))

            st.caption("Tasks")
            task_keys = {}
            for i, task in enumerate(tasks):
                key = f"{week_number}:{i}"
                task_keys[key] = task
                st.checkbox(
                    task,
                    key=key,
                    value=st.session_state.planner_task_status.get(key, False),
                    on_change=lambda key=key: st.session_state.planner_task_status.update(
                        {key: st.session_state[key]}
                    ),
                )

            # Display progress bar for this week's tasks.
            week_progress = next(
                item for item in progress["weekly_progress"] if item["week"] == week_number
            )
            st.progress(week_progress["progress"] / 100)
            st.caption(
                f"{week_progress['status']} · {week_progress['completed']} of {week_progress['total']} tasks done"
            )

    # Visualization of weekly impact.
    st.markdown("### Impact Visualization")
    chart_data = []
    for week in plan.get("weeks", []):
        reduction_text = week.get("expected_carbon_reduction", "0%")
        savings_text = week.get("expected_cost_savings", "$0")

        reduction_value = 0
        for token in reduction_text.replace('%', '').split():
            try:
                reduction_value = max(reduction_value, float(token))
            except ValueError:
                continue

        savings_value = 0
        for token in savings_text.replace('$', '').replace(',', '').split():
            try:
                savings_value = max(savings_value, float(token))
            except ValueError:
                continue

        chart_data.append(
            {
                "Week": week.get("title", f"Week {week.get('week', 1)}"),
                "Expected Carbon Reduction (%)": reduction_value,
                "Expected Cost Savings ($)": savings_value,
            }
        )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[item["Week"] for item in chart_data],
            y=[item["Expected Carbon Reduction (%)"] for item in chart_data],
            name="Carbon Reduction (%)",
            marker_color="#4ade80",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[item["Week"] for item in chart_data],
            y=[item["Expected Cost Savings ($)"] for item in chart_data],
            name="Cost Savings ($)",
            marker_color="#60a5fa",
        )
    )
    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary section.
    st.markdown("### Summary")
    st.info(plan["summary"].get("main_focus", "Focus on habit improvement"))
    st.write(
        f"Estimated total reduction: {plan['summary'].get('total_expected_reduction', '0%')}"
    )
    st.write(
        f"Estimated total savings: {plan['summary'].get('total_expected_savings', '$0')}"
    )

else:
    st.info(
        "Enter your sustainability details and click 'Generate 30-Day Action Plan' to begin."
    )
