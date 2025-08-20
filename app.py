import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set wide layout
st.set_page_config(page_title="Annual Savings Dashboard", layout="wide")

# Input section
st.header("🔢 Input Parameters")
input_cols = st.columns(2)
with input_cols[0]:
    production = st.number_input("Production (MT/day)", value=50)
    energy_per_ton = st.number_input("Avg. Energy Consumption (kWh/Ton)", value=1300)
    energy_tariff = st.number_input("Energy Tariff (₹/kWh)", value=6.5)
    yarn_price = st.number_input("Yarn Price (₹/kg)", value=140)
    net_profit = st.number_input("Net Profit (₹/kg)", value=7)
    downgrade_loss = st.number_input("Downgrade Loss (₹/kg)", value=35)

with input_cols[1]:
    avg_doff_weight = st.number_input("Avg. Doff Weight (kg)", value=5)
    paper_tube_price = st.number_input("Avg. Paper-tube price (₹)", value=8)
    energy_reduction_pct = st.number_input("Energy Consumption Reduction %", value=1.0) / 100
    downtime_reduction_pct = st.number_input("Downtime Reduction %", value=1.0) / 100
    downgrade_reduction_pct = st.number_input("Downgrade Reduction %", value=0.5) / 100
    even_improvement_pct = st.number_input("Even % Improvement", value=3.0) / 100

# Calculations
utilization_increase_pct = downtime_reduction_pct + downgrade_reduction_pct
downgrade_savings = production * 1000 * 365 * downgrade_loss * downgrade_reduction_pct / 100000
energy_savings = production * 365 * energy_per_ton * energy_tariff * energy_reduction_pct / 100000
downtime_savings = production * 365 * downtime_reduction_pct * net_profit * 1000 / 100000
consumables_savings = production * 1000 * 365 * even_improvement_pct * paper_tube_price / avg_doff_weight / 100000
total_savings = downgrade_savings + energy_savings + downtime_savings + consumables_savings

# Display results in 3x2 grid
st.header("📊 Calculated Annual Savings")
grid_cols = st.columns(3)
with grid_cols[0]:
    st.metric("Downgrade Savings (₹ lakh)", f"{downgrade_savings:.1f}")
    st.metric("Energy Savings (₹ lakh)", f"{energy_savings:.1f}")
with grid_cols[1]:
    st.metric("Downtime Savings (₹ lakh)", f"{downtime_savings:.1f}")
    st.metric("Consumables Savings (₹ lakh)", f"{consumables_savings:.1f}")
with grid_cols[2]:
    st.metric("Utilization % Increase", f"{utilization_increase_pct * 100:.2f}%")
    st.metric("Total Savings (₹ lakh)", f"{total_savings:.1f}")

# Waterfall Chart
st.subheader("📉 Savings Breakdown - Waterfall Chart")
fig = go.Figure(go.Waterfall(
    name="Savings",
    orientation="v",
    measure=["relative", "relative", "relative", "relative", "total"],
    x=["Downgrade", "Energy", "Downtime", "Consumables", "Total"],
    textposition="outside",
    text=[
        f"{downgrade_savings:.1f}",
        f"{energy_savings:.1f}",
        f"{downtime_savings:.1f}",
        f"{consumables_savings:.1f}",
        f"{total_savings:.1f}"
    ],
    y=[
        downgrade_savings,
        energy_savings,
        downtime_savings,
        consumables_savings,
        total_savings
    ],
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    increasing={"marker": {"color": "darkgrey"}},
    decreasing={"marker": {"color": "darkgrey"}},
    totals={"marker": {"color": "darkorange"}},
    insidetextfont={"color": "white", "size": 12, "family": "Arial"},
    outsidetextfont={"color": "white", "size": 12, "family": "Arial"}
))

fig.update_layout(title="Waterfall Chart of Savings", waterfallgap=0.3)
st.plotly_chart(fig, use_container_width=True)
