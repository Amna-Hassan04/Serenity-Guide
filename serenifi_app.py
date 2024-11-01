import streamlit as st
import pyttsx3

# Initialize session state
if 'meditation_duration' not in st.session_state:
    st.session_state.meditation_duration = 0

def speak(text):
    """Function to perform text-to-speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Streamlit app title and introduction
st.title("Serenifi App")
st.write("Welcome to the Serenity Guide!")

# Input for meditation duration
st.session_state.meditation_duration = st.number_input("Set meditation duration (seconds):", min_value=0, value=0)

# Button to start meditation
if st.button("Start Meditation"):
    # Speak out the meditation duration
    speak(f"Starting meditation for {st.session_state.meditation_duration} seconds.")
    # Add your meditation timer logic here (if needed)

# Display the current meditation duration
st.write("Duration: {} seconds".format(st.session_state.meditation_duration))
