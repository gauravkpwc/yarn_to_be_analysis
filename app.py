import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page layout
st.set_page_config(page_title="Annual Savings Dashboard", layout="wide")

# Create two columns for input and output
input_col, output_col = st.columns([1, 1])

# Input section
with input_col:
    st.header("📊 Input Parameters")
    tab1, tab2, tab3, tab4 = st.tabs(["Downgrade", "Energy", "Downtime", "Consumables"])

    with tab1:
        downgrade_savings = st.number_input("Downgrade Savings (₹)", value=10000)
    with tab2:
        energy_savings = st.number_input("Energy Savings (₹)", value=5000)
    with tab3:
        downtime_savings = st.number_input("Downtime Savings (₹)", value=3000)
    with tab4:
        consumables_savings = st.number_input("Consumables Savings (₹)", value=2000)

# Output section
with output_col:
    st.header("📈 Output Summary")
    total_savings = downgrade_savings + energy_savings + downtime_savings + consumables_savings
    st.metric(label="Total Savings (₹)", value=f"{total_savings:,.2f}")

    # Waterfall chart
    st.subheader("💧 Savings Breakdown - Waterfall Chart")
    fig = go.Figure(go.Waterfall(
        name="Savings",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Downgrade", "Energy", "Downtime", "Consumables", "Total"],
        textposition="outside",
        text=[
            f"₹{downgrade_savings:,.0f}",
            f"₹{energy_savings:,.0f}",
            f"₹{downtime_savings:,.0f}",
            f"₹{consumables_savings:,.0f}",
            f"₹{total_savings:,.0f}"
        ],
        y=[
            downgrade_savings,
            energy_savings,
            downtime_savings,
            consumables_savings,
            total_savings
        ],
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))

    fig.update_layout(
        title="Waterfall Chart of Savings",
        waterfallgap=0.3
    )

    st.plotly_chart(fig, use_container_width=True)

