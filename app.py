import os
import streamlit as st
import anthropic

# Retrieve API key from Hugging Face secrets
claude_api_key = os.getenv("CLAUDE_API_KEY")

# Initialize ClaudeAI client
client = anthropic.Client(api_key=claude_api_key)

def anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events):
    # Construct the message for ClaudeAI
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=250,
        temperature=0.2,
        system=f"You are a helpful mental health assistant that helps users manage their anxiety based on their mood, feelings, stress level, and recent events. Provide recommendations for exercises and techniques to reduce anxiety based on the user's mood, {mood}, their feelings described as: {feeling_description}, their current stress level of {current_stress_level}, and recent events: {recent_events}.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Task: Help me manage my anxiety. I'm feeling {mood}. Here's what I'm experiencing: {feeling_description}. My current stress level is {current_stress_level}, and these are some recent events that might have contributed: {recent_events}\n\nConsiderations:\nProvide tailored anxiety-reduction exercises.\nConsider the user's mood, stress level, feelings, and recent events.\nOffer practical and effective techniques.\nEnsure the suggestions are easy to follow."
                    }
                ]
            }
        ]
    )

    raw_context = message.content
    itinerary = raw_context[0].text
    return itinerary

# Streamlit App
def main():
    # App Title and Description with Emojis
    st.markdown('<h1 class="title">🧘‍♂️ Serenity Guide 🌿</h1>', unsafe_allow_html=True)
    st.markdown('<p class="description">Find your calm with Serenity Guide. 🌸 This app helps you manage anxiety by offering personalized exercises and techniques. Share your current mood, stress level, and recent events to receive tailored guidance. 💡</p>', unsafe_allow_html=True)
    
    # Warning Box
    st.warning("⚠️ Serenity Guide is not a substitute for professional mental health care. If you are in crisis, please seek help from a qualified healthcare provider or contact emergency services.")

    # Sidebar Inputs
    st.sidebar.header("📝 Share Your Current State:")
    
    mood = st.sidebar.selectbox("How are you feeling today?", ["Anxious", "Stressed", "Overwhelmed", "Calm", "Other"])
    feeling_description = st.sidebar.text_area("What exactly are you feeling?", placeholder="Describe your feelings here...")
    current_stress_level = st.sidebar.slider("Current Stress Level (1 to 10)", 1, 10, value=5)
    recent_events = st.sidebar.text_area("Recent Events", placeholder="Describe any recent events that may have contributed to your anxiety or stress...")

    if st.sidebar.button("Submit"):
        st.write("Thank you for sharing. Let’s find some exercises to help you.")
        guidance = anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events)
        st.write(guidance)

if __name__ == "__main__":
    main()
