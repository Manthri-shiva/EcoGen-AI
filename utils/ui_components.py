import streamlit as st


def hero_section(
    title: str,
    subtitle: str,
    emoji: str = "🌱"
):
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{emoji} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(
    label: str,
    value: str
):
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{value}</h3>
            <p>{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def recommendation_card(
    title: str,
    description: str
):
    st.markdown(
        f"""
        <div class="recommendation-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str):
    st.markdown(
        f"""
        <div class="status-badge">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )