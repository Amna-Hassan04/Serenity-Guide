import streamlit as st
import random
import time


# Add navigation options in sidebar
selected_tab = st.sidebar.selectbox("Choose a tab", ["Home", "Monitoring (Beta)", "Other Tabs"])

if selected_tab == "Monitoring (Beta)":
    # Add code for Monitoring (Beta) tab


st.title("Monitoring (Beta)")
st.write("This dashboard monitors real-time heart rate and stress level data.")

if selected_tab == "Monitoring (Beta)":
    # Add title and connection instructions
    st.title("Monitoring (Beta)")
    st.subheader("Connect Your Heart Rate and Stress Monitoring Device")

    # Connection instructions
    st.markdown("""
    To connect your device, please follow these steps:
    
    1. **Enable Bluetooth** on your heart rate monitoring device and the device running this app.
    2. **Select Your Device** from the dropdown below and click **Connect**.
    3. Once connected, your heart rate and stress levels will appear in real-time.
    """)

    # Simulated dropdown to select a device (for demonstration purposes)
    device_name = st.selectbox("Select Monitoring Device", ["Device 1", "Device 2", "Device 3"])

    # Simulate a connect button
    if st.button("Connect"):
        st.success(f"Connected to {device_name}!")
        # Simulate real-time data
        st.write("Heart Rate: 72 bpm")
        st.write("Stress Level: Moderate")


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