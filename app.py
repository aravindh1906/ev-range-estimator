import streamlit as st
from cars_db import EV_DATABASE
from engine import estimate_ev_metrics

st.set_page_config(page_title="EV Range Estimator", page_icon="⚡", layout="wide")

st.title("⚡ Dynamic EV Range & Battery Efficiency Estimator")
st.markdown("Calculate real-world highway/city range considering environmental factors and auxiliary loads.")

# 1. Car Selection
car_names = [f"{car['brand']} - {car['model']}" for car in EV_DATABASE]
selected_car_name = st.selectbox("Select Car Model", car_names)
selected_car = next(c for c in EV_DATABASE if f"{c['brand']} - {c['model']}" == selected_car_name)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔋 Battery & Vehicle State")
    soc = st.slider("Current Battery (%)", min_value=1, max_value=100, value=85, step=1)
    temp = st.slider("Ambient Temperature (°C)", min_value=-15, max_value=50, value=34, step=1)

with col2:
    st.subheader("⚙️ Cabin & Driving Settings")
    ac_on = st.toggle("Air Conditioning (AC)", value=True)
    music_on = st.toggle("Infotainment / Sound System", value=True)
    regen_mode = st.selectbox("Regenerative Braking Level", ["Off", "Standard", "Aggressive"], index=1)

# Computation
metrics = estimate_ev_metrics(
    battery_kwh=selected_car["battery_capacity_kwh"],
    soc_pct=soc,
    base_wh_km=selected_car["base_consumption_wh_km"],
    temp_c=temp,
    ac_on=ac_on,
    music_on=music_on,
    regen_mode=regen_mode.lower()
)

st.divider()

# Output Display
m1, m2, m3, m4 = st.columns(4)
m1.metric("Predicted Real Range", f"{metrics['predicted_range_km']} km")
m2.metric("Effective Consumption", f"{metrics['effective_consumption_wh_km']} Wh/km")
m3.metric("Usable Energy", f"{metrics['available_energy_kwh']} kWh")
m4.metric("Rated Range (100% SOC)", f"{selected_car['factory_range_km']} km")

st.info(f"Factory baseline: **{selected_car['base_consumption_wh_km']} Wh/km** | Pack Size: **{selected_car['battery_capacity_kwh']} kWh**")