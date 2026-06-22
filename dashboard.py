"""
EcoGen AI - Sustainability Dashboard

This page is designed to run independently with sample data so the UI can be
validated before connecting to live database or API sources.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# Configuration
# -----------------------------

st.set_page_config(
    page_title="EcoGen AI Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Sample Data
# -----------------------------

def generate_sample_data() -> pd.DataFrame:
    """
    Create a sample dataset for UI development.

    This avoids dependency on database data during the initial dashboard build.
    """
    dates = pd.date_range(start=datetime.today() - timedelta(days=29), periods=30, freq="D")

    data = pd.DataFrame(
        {
            "date": dates,
            "carbon_footprint": [420, 415, 410, 405, 398, 392, 389, 385, 381, 376, 370, 368, 362, 360, 358, 355, 350, 346, 341, 338, 332, 329, 325, 321, 318, 315, 312, 308, 305, 302],
            "sustainability_score": [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 82, 83, 84, 84, 85, 86, 87, 87, 88, 88, 89, 89, 90, 90, 91, 91, 92, 92, 93],
            "energy_consumption": [240, 236, 230, 228, 223, 220, 217, 215, 210, 208, 205, 202, 200, 198, 196, 194, 191, 188, 186, 184, 181, 179, 176, 174, 171, 169, 166, 164, 161, 159],
            "water_usage": [120, 118, 116, 114, 112, 110, 108, 106, 104, 102, 100, 99, 98, 96, 95, 94, 92, 91, 90, 89, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78],
            "waste_generated": [18, 17.5, 17, 16.8, 16.5, 16.0, 15.7, 15.4, 15.0, 14.8, 14.4, 14.0, 13.8, 13.5, 13.2, 13.0, 12.7, 12.5, 12.2, 12.0, 11.8, 11.5, 11.2, 11.0, 10.8, 10.5, 10.3, 10.0, 9.8, 9.5],
        }
    )

    return data


# -----------------------------
# Helper Functions
# -----------------------------

def format_metric(value: float, suffix: str = "") -> str:
    """Format KPI values for display."""
    return f"{value:,.1f}{suffix}" if suffix else f"{value:,.1f}"


def render_kpi_card(title: str, value: str, delta: str, color: str = "primary") -> None:
    """Render a styled KPI card using Streamlit columns."""
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: #0E1117;
                border: 1px solid #2E3A4F;
                border-radius: 0.8rem;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 0.9rem; color: #9AA4B2;">{title}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: white;">{value}</div>
                <div style="font-size: 0.85rem; color: {color};">{delta}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> object:
    """Create a Plotly line chart."""
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        template="plotly_dark",
        markers=True,
    )
    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> object:
    """Create a Plotly bar chart."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        template="plotly_dark",
    )
    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


# -----------------------------
# Main App
# -----------------------------

def main() -> None:
    """Render the sustainability dashboard page."""
    df = generate_sample_data()

    # Sidebar navigation placeholders
    st.sidebar.title("EcoGen AI")
    st.sidebar.caption("Sustainability Intelligence")
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
    selected_page = st.sidebar.radio("Navigation", nav_options)

    # Header
    st.title("🌱 Sustainability Dashboard")
    st.caption("Overview of environmental impact, scores, and sustainability trends")

    # KPI cards
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    carbon_current = float(latest["carbon_footprint"])
    carbon_prev = float(previous["carbon_footprint"])
    carbon_delta = carbon_prev - carbon_current

    score_current = float(latest["sustainability_score"])
    score_prev = float(previous["sustainability_score"])
    score_delta = score_current - score_prev

    energy_current = float(latest["energy_consumption"])
    energy_prev = float(previous["energy_consumption"])
    energy_delta = energy_prev - energy_current

    water_current = float(latest["water_usage"])
    water_prev = float(previous["water_usage"])
    water_delta = water_prev - water_current

    waste_current = float(latest["waste_generated"])
    waste_prev = float(previous["waste_generated"])
    waste_delta = waste_prev - waste_current

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card(
            "Carbon Footprint (kg CO₂)",
            format_metric(carbon_current),
            f"{'▲' if carbon_delta < 0 else '▼'} {abs(carbon_delta):.1f} vs previous day",
            "#4ADE80" if carbon_delta < 0 else "#F87171",
        )
    with col2:
        render_kpi_card(
            "Sustainability Score",
            f"{score_current:.1f}",
            f"{'▲' if score_delta > 0 else '▼'} {abs(score_delta):.1f} points",
            "#4ADE80" if score_delta > 0 else "#F87171",
        )
    with col3:
        render_kpi_card(
            "Energy Score",
            f"{max(0, min(100, 100 - (energy_current / 3))):.1f}",
            "Improving with efficient usage",
            "#60A5FA",
        )
    with col4:
        render_kpi_card(
            "Water Score",
            f"{max(0, min(100, 100 - (water_current * 0.4))):.1f}",
            "Good water conservation trend",
            "#60A5FA",
        )
    with col5:
        render_kpi_card(
            "Waste Score",
            f"{max(0, min(100, 100 - (waste_current * 3))):.1f}",
            f"{'▲' if waste_delta > 0 else '▼'} {abs(waste_delta):.1f} kg vs previous day",
            "#4ADE80" if waste_delta > 0 else "#F87171",
        )

    # Charts section
    st.subheader("Trend Analysis")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            create_line_chart(
                df,
                x_col="date",
                y_col="carbon_footprint",
                title="Carbon Footprint Trend",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            create_line_chart(
                df,
                x_col="date",
                y_col="energy_consumption",
                title="Energy Consumption Trend",
            ),
            use_container_width=True,
        )

    with chart_col2:
        st.plotly_chart(
            create_line_chart(
                df,
                x_col="date",
                y_col="sustainability_score",
                title="Sustainability Score Trend",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            create_bar_chart(
                df.tail(7),
                x_col="date",
                y_col="waste_generated",
                title="Weekly Waste Generation",
            ),
            use_container_width=True,
        )

    # Bottom summary cards
    st.subheader("Highlights")
    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.info(
            f"Current carbon footprint is **{carbon_current:.1f} kg CO₂**. "
            f"This is **{abs(carbon_delta):.1f} kg** {'lower' if carbon_delta < 0 else 'higher'} than yesterday."
        )

    with summary_col2:
        st.success(
            f"Sustainability score has improved to **{score_current:.1f}**. "
            f"The recent trend is {'positive' if score_delta > 0 else 'slightly declining'}."
        )

    with summary_col3:
        st.warning(
            f"Energy usage is at **{energy_current:.1f} units** and water usage is at **{water_current:.1f} liters**."
        )

    # Show selected sidebar item as context
    st.caption(f"Current section: {selected_page}")


if __name__ == "__main__":
    main()
