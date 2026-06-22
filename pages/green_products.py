import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from products.green_product_engine import (
    estimate_carbon_savings,
    recommend_products,
)


st.set_page_config(
    page_title="EcoGen AI Green Products",
    page_icon="🪴",
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
    .product-card {
        background: linear-gradient(180deg, #10213f, #0b1633);
        border: 1px solid #1e3a8a;
        border-radius: 0.9rem;
        padding: 0.9rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("🪴 Green Product Recommendation Engine")
st.write(
    "Discover eco-friendly products that align with your sustainability profile and savings goals."
)

with st.sidebar:
    st.header("Recommendation Inputs")
    carbon_footprint = st.number_input(
        "Carbon Footprint (kg CO₂)",
        min_value=0.0,
        value=1800.0,
        step=50.0,
    )
    electricity_usage = st.number_input(
        "Electricity Usage (units)",
        min_value=0.0,
        value=320.0,
        step=10.0,
    )
    water_consumption = st.number_input(
        "Water Consumption (liters)",
        min_value=0.0,
        value=6500.0,
        step=100.0,
    )
    sustainability_score = st.slider(
        "Sustainability Score",
        min_value=0,
        max_value=100,
        value=72,
    )
    selected_category = st.selectbox(
        "Category Filter",
        [
            "All",
            "LED Bulbs",
            "Smart Plugs",
            "Solar Panels",
            "Water Saving Devices",
            "Energy Efficient Appliances",
            "Waste Management Products",
        ],
    )

    if st.button("Generate Recommendations", use_container_width=True):
        try:
            st.session_state.product_recommendations = recommend_products(
                carbon_footprint=carbon_footprint,
                electricity_usage=electricity_usage,
                water_consumption=water_consumption,
                sustainability_score=sustainability_score,
            )
            st.session_state.carbon_estimate = estimate_carbon_savings(
                carbon_footprint=carbon_footprint,
                electricity_usage=electricity_usage,
                water_consumption=water_consumption,
                sustainability_score=sustainability_score,
            )
            st.success("Recommendations generated successfully.")
        except Exception as exc:
            st.error(f"Unable to generate recommendations: {exc}")


if "product_recommendations" not in st.session_state:
    st.session_state.product_recommendations = []
if "carbon_estimate" not in st.session_state:
    st.session_state.carbon_estimate = {}


if st.session_state.product_recommendations:
    recommendations = st.session_state.product_recommendations

    # Summary KPI cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Estimated Carbon Savings",
            f"{st.session_state.carbon_estimate.get('carbon_footprint_adjustment', 0):.1f} kg",
        )
    with col2:
        st.metric(
            "Electricity Savings",
            f"{st.session_state.carbon_estimate.get('electricity_savings', 0):.1f} kg",
        )
    with col3:
        st.metric(
            "Water Savings",
            f"{st.session_state.carbon_estimate.get('water_savings', 0):.1f} kg",
        )
    with col4:
        st.metric(
            "Recommended Products",
            len(recommendations),
        )

    # Top recommended products section
    st.subheader("Top Recommended Products")
    for product in recommendations[:3]:
        with st.container():
            st.markdown(
                f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p><strong>Category:</strong> {product['category']}</p>
                    <p><strong>Estimated Cost:</strong> ${product['estimated_cost']}</p>
                    <p><strong>Annual Savings:</strong> ${product['annual_cost_savings']}</p>
                    <p><strong>ROI:</strong> {product['roi']}%</p>
                    <p><strong>Impact Score:</strong> {product['impact_score']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Filtered cards
    st.subheader("Product Recommendations")
    filtered = [
        product
        for product in recommendations
        if selected_category == "All" or product["category"] == selected_category
    ]

    for product in filtered:
        with st.container():
            st.markdown(
                f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p><strong>Category:</strong> {product['category']}</p>
                    <p><strong>Estimated Cost:</strong> ${product['estimated_cost']}</p>
                    <p><strong>Annual Cost Savings:</strong> ${product['annual_cost_savings']}</p>
                    <p><strong>Carbon Reduction Potential:</strong> {product['carbon_reduction_potential']} kg</p>
                    <p><strong>ROI:</strong> {product['roi']}%</p>
                    <p><strong>Sustainability Impact Score:</strong> {product['impact_score']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Visualization: ROI comparison chart
    st.subheader("ROI Comparison")
    roi_df = {
        "Product": [item["name"] for item in filtered],
        "ROI (%)": [item["roi"] for item in filtered],
    }
    roi_fig = px.bar(
        roi_df,
        x="Product",
        y="ROI (%)",
        color="ROI (%)",
        template="plotly_dark",
    )
    roi_fig.update_layout(
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
    )
    st.plotly_chart(roi_fig, use_container_width=True)

    # Savings visualization
    st.subheader("Savings Visualization")
    savings_df = {
        "Product": [item["name"] for item in filtered],
        "Annual Savings ($)": [item["annual_cost_savings"] for item in filtered],
        "Carbon Reduction Potential (kg)": [item["carbon_reduction_potential"] for item in filtered],
    }
    savings_fig = go.Figure()
    savings_fig.add_trace(
        go.Bar(
            x=savings_df["Product"],
            y=savings_df["Annual Savings ($)"],
            name="Annual Savings ($)",
            marker_color="#4ade80",
        )
    )
    savings_fig.add_trace(
        go.Bar(
            x=savings_df["Product"],
            y=savings_df["Carbon Reduction Potential (kg)"],
            name="Carbon Reduction Potential (kg)",
            marker_color="#60a5fa",
        )
    )
    savings_fig.update_layout(
        barmode="group",
        template="plotly_dark",
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
    )
    st.plotly_chart(savings_fig, use_container_width=True)
else:
    st.info(
        "Use the sidebar controls and click 'Generate Recommendations' to see product suggestions."
    )
