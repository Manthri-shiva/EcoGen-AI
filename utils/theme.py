import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        .stApp{
            background:#020817;
            color:white;
        }

        .hero-card{
            background:linear-gradient(
                135deg,
                #0f172a,
                #082f49
            );
            padding:2rem;
            border-radius:20px;
            border:1px solid #1e40af;
            margin-bottom:1rem;
        }

        .metric-card{
            background:#0b1220;
            padding:1rem;
            border-radius:16px;
            border:1px solid #1e3a8a;
            text-align:center;
        }

        .recommendation-card{
            background:#111827;
            padding:1rem;
            border-radius:16px;
            border-left:5px solid #22c55e;
            margin-bottom:1rem;
        }

        .status-badge{
            background:#14532d;
            color:white;
            padding:6px 14px;
            border-radius:20px;
            display:inline-block;
            font-size:14px;
        }

        h1,h2,h3{
            color:white;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )