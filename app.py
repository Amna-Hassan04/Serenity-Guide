import os
import streamlit as st
import anthropic
import random
import datetime

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

# Additional Features
def get_quick_tip():
    tips = [
        "🌞 Take a deep breath and count to five. You got this! ✨",
        "💪 It's okay to feel this way; give yourself permission to rest. You've earned it! 🛌",
        "🍃 Step outside for a moment of fresh air and reset. 🌳",
        "✍️ Write down one thing you're grateful for today. It'll boost your mood! 😊",
        "🕰 Focus on the present moment. Let go of the past and future for now. 🌸",
        "🚀 Remember, small steps can lead to big changes. Keep going! 🌟"
    ]
    return random.choice(tips)

def daily_challenge(specific_need):
    challenges = {
        "Anxious": "Write down your anxious thoughts and then tear the paper up.",
        "Stressed": "Take a 10-minute walk outside and focus on your surroundings.",
        "Overwhelmed": "Break your tasks into smaller, manageable steps and tackle one at a time.",
        "Calm": "Maintain your calm state by doing a relaxing activity like reading or drawing.",
        "Other": "Try a new hobby or revisit an old one that brings you joy."
    }
    challenge = challenges.get(specific_need, "Spend 5 minutes meditating to start your day.")
    return challenge

def soothing_sounds():
    st.header("🎵 Calm Down with Soothing Sounds")
    sound_options = {
        "Rain": "https://pixabay.com/sound-effects/light-rain-109591/",
        "Ocean Waves": "https://pixabay.com/sound-effects/ocean-waves-112906/",
        "Forest": "https://pixabay.com/sound-effects/forest-163012/"
    }
    selected_sound = st.selectbox("Choose a sound to relax:", list(sound_options.keys()))
    if st.button("Play Sound"):
        st.audio(sound_options[selected_sound])

def interactive_journal():
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []

    journal_input = st.text_area("📝 Daily Journal", placeholder="Write down your thoughts...")
    if st.button("Save Entry"):
        st.session_state.journal_entries.append({
            "date": datetime.datetime.now(),
            "entry": journal_input
        })
        st.success("Journal entry saved!")

    # Display past journal entries
    if st.checkbox("Show Past Entries"):
        st.write("### Past Journal Entries:")
        for entry in st.session_state.journal_entries:
            st.write(f"**{entry['date'].strftime('%Y-%m-%d %H:%M:%S')}**: {entry['entry']}")

def mood_boosting_mini_games():
    st.header("🎮 Mood-Boosting Mini Games")
    st.markdown("Relax with a fun mini-game to distract your mind.")
    st.markdown("[Play Pacman](https://www.google.co.in/search?q=pacman&sca_esv=aaaa9a10aaa1b9d1&sca_upv=1&sxsrf=ADLYWIJzV0yNeS6YptYfZn5AEFUKvBUtSw%3A1725304252827&ei=vA3WZqCaMrLy4-EPiZmBwAw&ved=0ahUKEwig6PmY-6SIAxUy-TgGHYlMAMgQ4dUDCBA&uact=5&oq=pacman&gs_lp=Egxnd3Mtd2l6LXNlcnAiBnBhY21hbjIQEC4YgAQYsQMYQxiDARiKBTIOEC4YgAQYkQIYsQMYigUyEBAAGIAEGLEDGEMYgwEYigUyExAuGIAEGLEDGEMYgwEY1AIYigUyChAuGIAEGEMYigUyChAAGIAEGEMYigUyBRAAGIAEMg0QABiABBixAxhDGIoFMggQABiABBixAzIFEAAYgAQyHxAuGIAEGLEDGEMYgwEYigUYlwUY3AQY3gQY4ATYAQFI3hZQ5A5Y8BRwAXgBkAEAmAHlAaABiwqqAQMyLTa4AQPIAQD4AQGYAgegAp8LwgIKEAAYsAMY1gQYR8ICBBAjGCfCAgoQIxiABBgnGIoFwgILEAAYgAQYkQIYigXCAg4QABiABBixAxiDARiKBcICCxAAGIAEGLEDGIMBwgIOEC4YgAQYkQIY1AIYigXCAhAQLhiABBhDGMcBGIoFGK8BmAMAiAYBkAYGugYGCAEQARgUkgcFMS4wLjagB5Vj&sclient=gws-wiz-serp)")
    st.markdown("[Play Thinking Brain](https://kidshelpline.com.au/games/thinking-brain)")
    st.markdown("[Play Snake Game](https://www.google.co.in/search?si=ACC90nwm_DCLUGduakF5oU94y1HpDc2j-V_TsJpED11KWNYygOhydoKqqSH9t8iyybygqTEoKMZa&biw=1536&bih=695&dpr=1.25)")

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

    st.markdown(
        f'<marquee style="color: #2ECC71; font-size: 18px;">💡 Quick Tip: {get_quick_tip()}</marquee>',
        unsafe_allow_html=True
    )

    st.header("🏆 Daily Challenges")
    specific_need = mood  
    challenge = daily_challenge(specific_need)
    st.markdown(f"**Today's Challenge:** {challenge}")

    # Reward Mechanism
    completed = st.checkbox("Mark as Completed")
    if completed:
        st.markdown("🌟 Well done! You've earned a star! Keep up the great work! 🌟")
        
    soothing_sounds()
    mood_boosting_mini_games()
    interactive_journal()
    
if __name__ == "__main__":
    main()
