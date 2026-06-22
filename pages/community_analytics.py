import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from reports.community_analytics import (
    aggregate_user_statistics,
    calculate_community_impact,
    calculate_monthly_trends,
    create_dataframe,
    generate_leaderboard,
)


st.set_page_config(
    page_title="EcoGen AI Community Analytics",
    page_icon="🌍",
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
    .leaderboard-row {
        background: #0b1220;
        border-bottom: 1px solid #1e293b;
        padding: 0.4rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("🌐 Community Impact Analytics")
st.write(
    "Understand community-wide sustainability progress, contributor performance, and trend patterns."
)

# Load analytics data
impact = calculate_community_impact()
leaderboard = generate_leaderboard()
statistics = aggregate_user_statistics()
trends = calculate_monthly_trends()
df = create_dataframe()

# KPI cards
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        "Total Registered Users",
        f"{impact['total_registered_users']}",
    )
with col2:
    st.metric(
        "Total Carbon Reduction",
        f"{impact['total_carbon_reduction']:.1f} kg",
    )
with col3:
    st.metric(
        "Total Energy Saved",
        f"{impact['total_energy_saved']:.1f} kWh",
    )
with col4:
    st.metric(
        "Total Water Saved",
        f"{impact['total_water_saved']:.1f} L",
    )
with col5:
    st.metric(
        "Total Waste Reduced",
        f"{impact['total_waste_reduced']:.1f} kg",
    )

st.markdown("---")

summary_col1, summary_col2 = st.columns(2)
with summary_col1:
    st.subheader("Community Summary")
    st.write(
        f"Community Sustainability Score: {impact['community_sustainability_score']:.2f}"
    )
    st.write(
        f"Estimated Cost Savings: ${impact['total_cost_savings']:.2f}"
    )
with summary_col2:
    st.subheader("Top Contributors")
    for person in leaderboard[:5]:
        st.markdown(
            f"<div class='leaderboard-row'>#{person['rank']} {person['name']} — Score {person['sustainability_score']:.1f}</div>",
            unsafe_allow_html=True,
        )

st.markdown("### Impact Breakdown")
impact_col1, impact_col2 = st.columns(2)
with impact_col1:
    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Carbon Reduction",
                    "Energy Savings",
                    "Water Savings",
                    "Waste Reduction",
                ],
                values=[
                    impact["total_carbon_reduction"],
                    impact["total_energy_saved"],
                    impact["total_water_saved"],
                    impact["total_waste_reduced"],
                ],
                hole=0.35,
                marker_colors=["#22c55e", "#38bdf8", "#a78bfa", "#f97316"],
            )
        ]
    )
    pie_fig.update_layout(template="plotly_dark", margin={"l": 10, "r": 10, "t": 30, "b": 10})
    st.plotly_chart(pie_fig, use_container_width=True)
with impact_col2:
    bar_fig = go.Figure(
        data=[
            go.Bar(
                x=[entry["name"] for entry in leaderboard[:6]],
                y=[entry["carbon_reduction"] for entry in leaderboard[:6]],
                marker_color="#4ade80",
                name="Carbon Reduction",
            )
        ]
    )
    bar_fig.update_layout(
        template="plotly_dark",
        title="Top Carbon Reduction Contributors",
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
    )
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("### Trend Analysis")
trend_col1, trend_col2 = st.columns(2)
with trend_col1:
    line_fig = px.line(
        x=trends["months"],
        y=trends["community_score"],
        labels={"x": "Month", "y": "Community Score"},
        template="plotly_dark",
    )
    line_fig.update_layout(title="Community Sustainability Score Trend")
    st.plotly_chart(line_fig, use_container_width=True)

    line_energy = px.line(
        x=trends["months"],
        y=trends["energy_saved"],
        labels={"x": "Month", "y": "Energy Saved (kWh)"},
        template="plotly_dark",
    )
    line_energy.update_layout(title="Energy Savings Trend")
    st.plotly_chart(line_energy, use_container_width=True)

with trend_col2:
    line_carbon = px.line(
        x=trends["months"],
        y=trends["carbon_reduction"],
        labels={"x": "Month", "y": "Carbon Reduction (kg)"},
        template="plotly_dark",
    )
    line_carbon.update_layout(title="Carbon Reduction Trend")
    st.plotly_chart(line_carbon, use_container_width=True)

    line_water = px.line(
        x=trends["months"],
        y=trends["water_saved"],
        labels={"x": "Month", "y": "Water Saved (L)"},
        template="plotly_dark",
    )
    line_water.update_layout(title="Water Savings Trend")
    st.plotly_chart(line_water, use_container_width=True)

st.markdown("### Leaderboard")
leaderboard_df = px.data.tips() if False else None

for person in leaderboard:
    st.markdown(
        f"""
        <div class='leaderboard-row'>
            <strong>#{person['rank']}</strong> {person['name']} |
            Score: {person['sustainability_score']:.1f} |
            Carbon Reduction: {person['carbon_reduction']:.1f} kg |
            Energy Saved: {person['energy_saved']:.1f} kWh
        </div>
        """,
        unsafe_allow_html=True,
    )
