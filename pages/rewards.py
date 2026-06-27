import streamlit as st
import plotly.graph_objects as go
from utils.theme import apply_theme
from rewards.reward_engine import (
    assign_badge,
    calculate_points,
    calculate_streak,
    get_earned_achievements,
    get_next_milestone,
)


st.set_page_config(
    page_title="EcoGen AI Rewards",
    page_icon="🏆",
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
    .badge-card {
        background: linear-gradient(180deg, #10213f, #0b1633);
        border: 1px solid #1e3a8a;
        border-radius: 0.9rem;
        padding: 0.9rem;
        margin-bottom: 0.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "reward_data" not in st.session_state:
    st.session_state.reward_data = None


st.title("🏆 Eco Rewards System")
st.write(
    "Track points, streaks, badges, and milestone progress for your sustainability journey."
)

with st.sidebar:
    st.header("Reward Inputs")
    sustainability_score = st.slider(
        "Sustainability Score",
        min_value=0,
        max_value=100,
        value=72,
    )
    carbon_reduction = st.slider(
        "Carbon Reduction (%)",
        min_value=0.0,
        max_value=100.0,
        value=18.0,
        step=1.0,
    )
    planner_completion = st.slider(
        "Planner Completion (%)",
        min_value=0.0,
        max_value=100.0,
        value=65.0,
        step=1.0,
    )
    daily_streak = st.number_input(
        "Daily Streak",
        min_value=0,
        max_value=365,
        value=12,
        step=1,
    )
    weekly_streak = st.number_input(
        "Weekly Streak",
        min_value=0,
        max_value=52,
        value=4,
        step=1,
    )
    monthly_streak = st.number_input(
        "Monthly Streak",
        min_value=0,
        max_value=24,
        value=1,
        step=1,
    )

    if st.button("Calculate Rewards", use_container_width=True):
        try:
            points = calculate_points(
                sustainability_score=sustainability_score,
                carbon_reduction=carbon_reduction,
                planner_completion=planner_completion,
                daily_streak=daily_streak,
                weekly_streak=weekly_streak,
                monthly_streak=monthly_streak,
            )
            streak_data = calculate_streak(
                daily_streak=daily_streak,
                weekly_streak=weekly_streak,
                monthly_streak=monthly_streak,
            )
            badge_data = assign_badge(points["total_points"])
            next_milestone = get_next_milestone(points["total_points"])
            earned = get_earned_achievements(points["total_points"])

            st.session_state.reward_data = {
                "points": points,
                "streak": streak_data,
                "badge": badge_data,
                "next_milestone": next_milestone,
                "earned": earned,
            }
            st.success("Rewards calculated successfully.")
        except Exception as exc:
            st.error(f"Unable to calculate rewards: {exc}")
            st.session_state.reward_data = None


if st.session_state.reward_data:
    data = st.session_state.reward_data
    points = data["points"]
    streak = data["streak"]
    badge = data["badge"]
    milestone = data["next_milestone"]
    earned = data["earned"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Points", f"{points['total_points']:.0f}")
    with col2:
        st.metric("Current Badge", badge["current_badge"])
    with col3:
        st.metric("Next Badge Target", f"{badge['next_badge_target']}")
    with col4:
        st.metric("Remaining to Next", badge["remaining_to_next"])

    st.markdown("### Achievement Progress")
    st.progress(badge["progress_to_next"] / 100)
    st.caption(
        f"{badge['current_badge']} · {badge['progress_to_next']}% to {badge['next_badge']}"
    )

    # Reward summary dashboard
    st.markdown("### Reward Summary")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.subheader("Points Breakdown")
        st.write(f"Score points: {points['score_points']:.1f}")
        st.write(f"Reduction points: {points['reduction_points']:.1f}")
        st.write(f"Planner points: {points['planner_points']:.1f}")
        st.write(f"Streak points: {points['streak_points']:.1f}")
    with summary_col2:
        st.subheader("Streak Tracker")
        st.write(f"Daily Streak: {streak['daily_streak']} days")
        st.write(f"Weekly Streak: {streak['weekly_streak']} weeks")
        st.write(f"Monthly Streak: {streak['monthly_streak']} months")
        st.write(f"Best Streak: {streak['best_streak']}")

    # Badge gallery
    st.markdown("### Badge Gallery")
    badge_columns = st.columns(5)
    for idx, badge_item in enumerate([
        "Green Beginner",
        "Eco Explorer",
        "Eco Warrior",
        "Sustainability Champion",
        "Planet Guardian",
    ]):
        with badge_columns[idx]:
            if badge_item in [item["name"] for item in earned]:
                st.markdown(
                    f"""
                    <div class="badge-card">
                        <h4>🏅 {badge_item}</h4>
                        <p>Unlocked</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="badge-card">
                        <h4>🔒 {badge_item}</h4>
                        <p>Locked</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Milestone tracker
    st.markdown("### Milestone Tracker")
    st.write(
        f"Next milestone: {milestone['name']} ({milestone['remaining']} points remaining)"
    )

    # Impact visualization
    st.markdown("### Points Distribution")
    fig = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Score Points",
                    "Reduction Points",
                    "Planner Points",
                    "Streak Points",
                ],
                values=[
                    points["score_points"],
                    points["reduction_points"],
                    points["planner_points"],
                    points["streak_points"],
                ],
                hole=0.35,
                marker_colors=["#22c55e", "#38bdf8", "#a78bfa", "#f97316"],
            )
        ]
    )
    fig.update_layout(template="plotly_dark", margin={"l": 10, "r": 10, "t": 30, "b": 10})
    st.plotly_chart(fig, use_container_width=True)

    # Earned achievements
    st.markdown("### Earned Achievements")
    if earned:
        for item in earned:
            st.success(f"{item['name']} — {item['description']}")
    else:
        st.info("No achievements unlocked yet. Keep going!")

else:
    st.info(
        "Enter your sustainability metrics and click 'Calculate Rewards' to see your rewards dashboard."
    )
