import streamlit as st

# Main App Title
st.title("SereniFi Guide")

# Tabs for Navigation
tab1, tab2, tab3 = st.tabs(["Calm Space", "Monitoring (Beta)", "About and Feedback"])

# Calm Space Tab Content
with tab1:
    st.header("Calm Space")
    # Existing content for Calm Space
    st.write("Welcome to your Calm Space.")

# Monitoring (Beta) Tab Content
with tab2:
    st.header("Monitoring (Beta)")
    st.write("Connect your heart rate and stress monitoring device below.")
    
    # Instructions for connecting a monitoring device
    st.markdown("""
    **Steps to Connect:**
    1. Enable Bluetooth on your device.
    2. Select your wearable device from the available options below.
       - Example Device 1
       - Example Device 2
    3. Once connected, real-time monitoring data will display here.
    """)

    # Example placeholders for real-time data
    st.metric(label="Heart Rate", value="72 bpm")
    st.metric(label="Stress Level", value="Low")

# About and Feedback Tab Content
with tab3:
    st.header("About and Feedback")
    # Content for About and Feedback
    st.write("This section provides information and allows feedback.")

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
        for _ in range(100):  # Finite loop for demonstration
            heart_rate, stress_level = simulate_data()
            heart_rate_display.metric("Heart Rate", f"{heart_rate} BPM")
            stress_level_display.metric("Stress Level", f"{stress_level}/10")
            time.sleep(1)