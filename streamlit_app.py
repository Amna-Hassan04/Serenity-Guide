import streamlit as st
import random
import time

st.set_page_config(page_title="SereniFi Guide IoT Dashboard", layout="centered")

st.title("SereniFi Guide IoT Monitoring Dashboard")
st.write("This dashboard monitors real-time heart rate and stress level data.")

# Display placeholders for real-time data
heart_rate_display = st.empty()
stress_level_display = st.empty()
status_display = st.empty()

def simulate_data():
    """Simulate heart rate and stress level data"""
    heart_rate = random.randint(60, 100)
    stress_level = random.randint(1, 10)
    return heart_rate, stress_level

# Real-time update loop
status_display.write("Monitoring real-time data...")

while True:
    # Simulate or fetch data (replace this with actual IoT data fetching if available)
    heart_rate, stress_level = simulate_data()

    # Display the data in real-time
    heart_rate_display.metric("Heart Rate", f"{heart_rate} BPM")
    stress_level_display.metric("Stress Level", f"{stress_level}/10")

    # Refresh data every second
    time.sleep(1)
ss