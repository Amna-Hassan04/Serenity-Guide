import streamlit as st
import random
import datetime
import time
import json
from datetime import datetime, timedelta

class AffirmationWidget:
    def __init__(self):
        # Dictionary of affirmations by theme
        self.affirmations = {
            "confidence": [
                "I am capable of achieving anything I set my mind to.",
                "I trust my abilities and inner wisdom.",
                "I radiate confidence, self-respect, and inner harmony.",
                "I am worthy of respect and acceptance.",
                "My potential to succeed is infinite.",
                "I choose to be confident and self-assured.",
                "I am enough, just as I am."
            ],
            "relaxation": [
                "I choose to feel calm and peaceful.",
                "I release all tension and embrace tranquility.",
                "I am surrounded by peaceful energy.",
                "My mind is calm, my body is relaxed.",
                "I breathe in peace and exhale stress.",
                "I deserve to rest and feel at peace.",
                "Tranquility flows through me with each breath."
            ],
            "productivity": [
                "I am focused and productive in all I do.",
                "I complete my tasks efficiently and effectively.",
                "I use my time wisely and purposefully.",
                "I am motivated and driven to achieve my goals.",
                "I take action towards my dreams.",
                "I am organized and accomplish my priorities.",
                "My productivity increases each day."
            ]
        }

    def get_affirmation(self, theme):
        """Get a random affirmation from the selected theme"""
        return random.choice(self.affirmations[theme])

def display_affirmation_widget():
    st.markdown("""
    <style>
    .affirmation-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f8ff;
        margin: 10px 0;
        text-align: center;
    }
    .affirmation-text {
        font-size: 24px;
        color: #2c3e50;
        font-weight: bold;
        margin: 20px 0;
    }
    .theme-selector {
        margin: 20px 0;
    }
    .refresh-interval {
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🌟 Daily Affirmations")

    # Initialize the widget
    if 'affirmation_widget' not in st.session_state:
        st.session_state.affirmation_widget = AffirmationWidget()
    
    # Initialize last update time
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

    # Theme selection
    theme = st.selectbox(
        "Choose your affirmation theme:",
        ["confidence", "relaxation", "productivity"],
        key="theme_selector"
    )

    # Refresh interval selection
    refresh_interval = st.slider(
        "Select refresh interval (minutes):",
        min_value=1,
        max_value=60,
        value=5,
        key="refresh_interval"
    )

    # Enable notifications
    notifications_enabled = st.checkbox("Enable push notifications", value=False)

    # Get current affirmation
    if 'current_affirmation' not in st.session_state:
        st.session_state.current_affirmation = st.session_state.affirmation_widget.get_affirmation(theme)

    # Check if it's time to refresh
    current_time = datetime.now()
    time_difference = current_time - st.session_state.last_update
    if time_difference.total_seconds() >= (refresh_interval * 60):
        st.session_state.current_affirmation = st.session_state.affirmation_widget.get_affirmation(theme)
        st.session_state.last_update = current_time

    # Display affirmation
    st.markdown(
        f"""
        <div class="affirmation-container">
            <div class="affirmation-text">
                "{st.session_state.current_affirmation}"
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Manual refresh button
    if st.button("↻ New Affirmation"):
        st.session_state.current_affirmation = st.session_state.affirmation_widget.get_affirmation(theme)
        st.session_state.last_update = current_time

    # Display last update time
    st.markdown(
        f"<div style='text-align: center; color: #666;'>Last updated: {st.session_state.last_update.strftime('%I:%M %p')}</div>",
        unsafe_allow_html=True
    )

    # Save preferences
    if st.button("Save Preferences"):
        preferences = {
            "theme": theme,
            "refresh_interval": refresh_interval,
            "notifications_enabled": notifications_enabled
        }
        st.success("Preferences saved successfully!")

# To use this widget in your Streamlit app:
if __name__ == "__main__":
    display_affirmation_widget()