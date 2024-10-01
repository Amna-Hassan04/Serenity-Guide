import base64
import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import random
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# AI Integration
import anthropic

# Retrieve API key from Hugging Face secrets
claude_api_key = "your-api-key"  # Replace with your actual ClaudeAI API key

# Initialize ClaudeAI client
client = anthropic.Client(api_key=claude_api_key)

def anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events):
    messages = [
        {
            "role": "user",
            "content": f"Task: Help me manage my anxiety. I'm feeling {mood}. Here's what I'm experiencing: {feeling_description}. My current stress level is {current_stress_level}, and these are some recent events that might have contributed: {recent_events}."
        }
    ]
    
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            temperature=0.2,
            messages=messages
        )
        return response["choices"][0]["text"]
    
    except Exception as e:
        # Handle the error gracefully
        st.error(f"An error occurred while fetching advice: {str(e)}")
        return "Unable to provide personalized advice at this moment."


# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="Anxiety Relief App", page_icon=":relieved:", layout="centered")

# Data for mental health (sampled)
data = {
    'Activity': ['Meditation', 'Yoga', 'Breathing', 'Journaling', 'Music'],
    'Calmness_Level': [85, 78, 90, 75, 88]
}

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Animated background
page_bg_img = f"""
<style>
/* Animated background gradient */
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stSidebar"] > div:first-child {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

.main .block-container {{
    max-width: 900px;  /* Increase the width of the centered section */
    padding: 2rem 1rem;  /* Adjust padding for a more spacious look */
}}

@keyframes gradientBG {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def soothing_sounds():
    st.header("🎵 Calm Down with Soothing Sounds")
    sound_options = {
        "Rain": "https://www.soundjay.com/nature/rain-01.mp3",
        "Ocean Waves": "https://www.soundjay.com/nature/ocean-waves-01.mp3",
        "Forest": "https://www.soundjay.com/nature/forest-01.mp3"
    }
    selected_sound = st.selectbox("Choose a sound to relax:", list(sound_options.keys()))
    if st.button("Play Sound"):
        st.audio(sound_options[selected_sound])

# Main function to control page navigation
def main():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Calm Space", "Personalized Management", "About & Feedback"],
        icons=["house-door-fill", "cloud-sun-fill", "person-fill", "chat-dots-fill"],
        menu_icon="sun",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#333", "border-radius": "10px", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#ddd",
                "border-radius": "10px",
                "color": "#fff",
                "background-color": "rgba(0, 0, 0, 0.8)",  # More opaque background
                "transition": "background-color 0.3s ease, transform 0.2s"
            },
            "nav-link-selected": {"background-color": "#04AA6D", "color": "#fff", "transform": "scale(1.1)"}
        }
    )

    if selected == "Home":
        show_main_page()
    elif selected == "Calm Space":
        show_calm_space()
    elif selected == "Personalized Management":
        show_personalized_management()
    elif selected == "About & Feedback":
        show_about_and_feedback()

def show_main_page():
    st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
    <h1 class="centered-title">Welcome to SereniFi</h1>
    """, unsafe_allow_html=True
)

    st.markdown('<h3 class="pulse" style="text-align: center;">Feel Calm, Centered, and Peaceful</h3>', unsafe_allow_html=True)

    st.image("https://images.pexels.com/photos/185801/pexels-photo-185801.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Breathe and Relax", use_column_width=True)

    st.write("---")

    # Interactive content
    st.markdown("""
    ### Welcome to Your Oasis of Calm

    Imagine a sanctuary where you can escape the hustle and bustle of everyday life—this is your space to recharge and rejuvenate. Embracing mental health is not just about addressing issues; it's about nurturing your inner self and fostering a sense of tranquility.

    **Discover Your Path to Peace:**
    - **Mindful Breathing:** Click below to start a guided breathing exercise that helps calm your mind instantly.
    - **Relaxation Techniques:** Explore various methods to integrate relaxation into your daily routine.
    - **Personalized Tips:** Answer a quick survey to receive tailored advice for enhancing your well-being.

    **Engage with Us:**
    - Share your favorite relaxation techniques or feedback on how our platform helps you.

    Your path to a serene and fulfilling life starts here. Let’s embark on this journey together—take the first step today!
    """)

    # Interactive Widgets
    if st.button('Start Guided Breathing'):
        st.balloons()
        st.write("**Guided Breathing Exercise:** Inhale deeply through your nose for 4 seconds, hold for 4 seconds, and exhale slowly through your mouth. Repeat this process a few times to feel the calming effect.")

    st.write("---")

    # Survey for Personalized Tips
    st.subheader("Personalized Tips for You")
    with st.form(key='personalized_tips_form'):
        mood = st.radio("What's your current anxiety level?", ["Low", "Moderate", "High", "Overwhelmed"])
        submit_button = st.form_submit_button("Get Tips")
        if submit_button:
            tips = {
                "Low": "Keep up the great work! Stay consistent with mindfulness techniques.",
                "Moderate": "Take a moment to practice deep breathing.",
                "High": "Pause and try a guided meditation.",
                "Overwhelmed": "It's important to step away and take a break."
            }
            st.write(f"**Tip:** {tips[mood]}")

    st.write("---")

    st.markdown("""
    ### Embrace Your Journey to Wellness

    Taking care of your mental health is an ongoing journey that requires attention and effort. It's essential to recognize the value of setting aside time for yourself amidst your busy schedule. Activities such as mindfulness, relaxation exercises, and engaging in hobbies can significantly improve your overall well-being. 

    Remember, mental health is not just the absence of mental illness but a state of complete emotional, psychological, and social well-being. Incorporating small, positive changes into your daily routine can lead to a more balanced and fulfilling life. Embrace these practices with an open heart and notice the positive impact they have on your day-to-day life. 
    """)

    st.video("https://www.youtube.com/watch?v=inpok4MKVLM", start_time=10)

    st.write("---")

    st.markdown('<h4 style="text-align: center;">The Importance of Mental Health</h4>', unsafe_allow_html=True)
    
    st.write("Mental health is just as important as physical health, but often overlooked. It affects how we think, feel, and act in our daily lives. Prioritizing mental well-being can help us manage stress, connect with others, and make healthier choices.")

    # Interactive section for viewers
    st.subheader("Let's Explore How Mental Health Affects You")
    
    # User input on mental health habits
    daily_mindfulness = st.radio("How often do you practice mindfulness or self-care?", ["Daily", "Weekly", "Occasionally", "Rarely"])
    
    if daily_mindfulness == "Daily":
        st.success("Amazing! Regular self-care routines greatly enhance mental wellness.")
    elif daily_mindfulness == "Weekly":
        st.info("Great start! Try increasing your self-care sessions to enhance its benefits.")
    elif daily_mindfulness == "Occasionally":
        st.warning("It's good you're trying! Consistency can help you feel more balanced.")
    else:
        st.error("Mental health is crucial! Start small by incorporating simple self-care practices.")
    
    st.write("---")

    # Tip for improving mental health
    st.subheader("Quick Tip for Mental Health")
    if st.button("Get a Tip"):
        tips = [
            "Take a few minutes to practice deep breathing daily.",
            "Keep a gratitude journal to focus on the positive.",
            "Engage in physical activity to boost your mood.",
            "Take breaks when you're feeling overwhelmed.",
            "Connect with loved ones and share how you're feeling."
        ]
        st.write(f"Tip: {random.choice(tips)}")

    lottie_url_breathing = "https://lottie.host/89b3ab99-b7ee-4764-ac3a-5fe1ef057bde/WaOPmT23PU.json"
    
    lottie_json_breathing = load_lottie_url(lottie_url_breathing)
    
    if lottie_json_breathing:
        st.markdown(
            """
            <style>
            .lottie-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                background: none;
            }
            .lottie-item {
                margin: 0 10px;  /* Add space between animations */
            }
            .lottie-animation {
                background: transparent;  /* Make the background of the animation transparent */
            }
            </style>
            <div class="lottie-container">
            """, unsafe_allow_html=True)

        st.markdown('<div class="lottie-item lottie-animation">', unsafe_allow_html=True)
        st_lottie(lottie_json_breathing, speed=1, width=300, height=300, key="breathing-animation")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Introduction to the Data Visualization
    st.markdown("""
    ### Explore the Impact of Different Activities

    Understanding which activities can best help in reducing anxiety is essential for making informed decisions about your mental wellness. 

    Use this visualization to see which activities might work best for you and consider incorporating them into your daily routine. Remember, what works for one person may differ for another, so it's important to explore and find what resonates with you.
    """)

    # Interactive Section: Activity Preferences
    st.subheader("Which Activities Do You Prefer?")
    activities = st.multiselect(
        "Select the activities you enjoy or want to try:",
        options=df['Activity'],
        default=df['Activity']
    )

    if activities:
        st.write("You selected:", ", ".join(activities))
        selected_data = df[df['Activity'].isin(activities)]
        fig_selected = px.bar(selected_data, x='Activity', y='Calmness_Level', title="Selected Activities Effectiveness")
        st.plotly_chart(fig_selected)

    st.write("---")
    st.markdown('<p style="text-align: center;">© 2024 Anxiety Relief Platform. All rights reserved.</p>', unsafe_allow_html=True)

def show_personalized_management():
    st.header("📝 Personalized Anxiety Management")

    # Input form for user data
    with st.form(key='anxiety_management_form'):
        mood = st.selectbox("How are you feeling?", ["Anxious", "Stressed", "Overwhelmed", "Calm"])
        feeling_description = st.text_area("Describe your feelings:", placeholder="I feel...")
        current_stress_level = st.slider("Stress Level (1 to 10)", 1, 10, 5)
        recent_events = st.text_area("Any recent events contributing to your stress or anxiety?")
        submit_button = st.form_submit_button("Get Personalized Advice")

        if submit_button:
            st.write("Generating your personalized plan...")
            advice = anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events)
            st.write(f"**Personalized Advice:** {advice}")

def show_calm_space():
    st.title("Calm Space")
    st.write("Engage in a breathing exercise to calm your mind.")
    
    st.subheader("Quick Tips for Positivity")
    quick_tips = [
        "Take a deep breath and count to 5.",
        "Focus on what you can control, not on what you can't.",
        "Take a moment to reflect on something you're grateful for.",
        "Smile at yourself in the mirror."
    ]
    st.write("\n".join(f"- {tip}" for tip in quick_tips))

    st.write("---")

    # Interactive Section: Daily Challenge Suggestions
    st.subheader("Daily Challenge Suggestions")
    challenges = {
        "Meditation": "Try a 10-minute guided meditation session today. Find a quiet space and focus on your breath.",
        "Yoga": "Follow a 15-minute yoga routine to stretch and relax your body. Check out a video for guidance.",
        "Breathing": "Engage in deep breathing exercises for 5 minutes. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale slowly.",
        "Journaling": "Spend 10 minutes writing down your thoughts and feelings. Reflect on your day and your emotions.",
        "Music": "Listen to calming music or nature sounds for 20 minutes. Allow the sounds to help you relax and unwind."
    }

    selected_challenge = st.selectbox("Choose an activity for your daily challenge:", options=list(challenges.keys()))

    if selected_challenge:
        st.write(f"**Today's Challenge:** {challenges[selected_challenge]}")
        st.write("Set a reminder to complete this challenge today. Remember, consistency is key to building habits and improving your mental well-being.")

    st.write("---")

    st.subheader("Daily Anxiety Check")
    # Sidebar Inputs
    st.subheader("📝 Share Your Current State:")
    
    mood = st.selectbox("How are you feeling today?", ["Anxious", "Stressed", "Overwhelmed", "Calm", "Other"])
    feeling_description = st.text_area("What exactly are you feeling?", placeholder="Describe your feelings here...")
    current_stress_level = st.slider("Current Stress Level (1 to 10)", 1, 10, value=5)
    recent_events = st.text_area("Recent Events", placeholder="Describe any recent events that may have contributed to your anxiety or stress...")

    if st.button("Submit"):
        st.write("Thank you for sharing. Let’s find some exercises to help you.")
        guidance = anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events)
        st.write(guidance)
    
    st.subheader("Mood-Boosting Mini Games")
    st.write("Take a break and play a mini-game to reduce your anxiety.")
    if st.button("Start Game"):
        st.write("Launching a quick mood-boosting game...")

    st.write("---")
    soothing_sounds()

    st.write("---")

    st.subheader("Interactive Journaling")
    if st.button("Submit Journal Entry"):
        st.success("Journal entry: It's important to reflect and release your emotions.")

    st.write("---")
    st.markdown('<p style="text-align: center;">© 2024 Anxiety Relief Platform. All rights reserved.</p>', unsafe_allow_html=True)

def show_about_and_feedback():
    st.title("About Us & Feedback")
    
    st.write("""
    **Welcome to Our Anxiety Relief Platform!**
    
    We are dedicated to promoting mental wellness through interactive and accessible tools. Our mission is to provide a supportive environment where individuals can explore effective techniques for managing anxiety and improving overall mental well-being.
    """)
    
    st.write("""
    Our team consists of mental health professionals, wellness coaches, and tech enthusiasts who are passionate about making mental health resources accessible to everyone. We believe that everyone deserves a space to find calm, learn about wellness, and connect with supportive tools and communities.
    """)
    
    st.write("""
    **Our Vision**
    We envision a world where mental wellness is prioritized and accessible to all. Through innovative solutions and a user-centric approach, we aim to create a space where individuals can find the support they need to thrive.
    """)
    
    st.write("""
    **Meet the Team**
    - **Amna Hassan** - Back-end Developer
    - **Anushka Pote** - Wellness Coach
    - **Madhuri K** - Front-end Developer
    - **Pearl Vashishta** - Community Manager
    """)
    
    st.write("---")
    
    # Interactive Feedback on Activities
    st.subheader("Share Your Experience")
    st.write("""
    We'd love to hear how these activities are working for you. Your feedback helps others find effective ways to manage anxiety and improve their mental wellness. Feel free to share your thoughts, experiences, or suggestions.
    """)

    feedback_activity = st.text_area("How have the activities helped you? Share your experience here:")
    if st.button("Submit Feedback"):
        if feedback_activity:
            st.success("Thank you for sharing your experience! Your feedback is valuable and appreciated.")
    
    st.write("---")
    
    # Our Advertising Partners
    st.subheader("Our Advertising Partners")
    st.write("Check out our partners in mental wellness products and services:")
    st.write("- **Mindfulness App**: An app offering guided meditations and mindfulness exercises.")
    st.write("- **Relaxation Techniques Guide**: A comprehensive guide to various relaxation techniques and their benefits.")
    
    st.write("---")
    
    # Call to Action
    st.subheader("Get Involved")
    st.write("""
    Interested in supporting our mission? There are several ways you can get involved:
    - **Volunteer**: Join our team of volunteers to help others benefit from our platform.
    - **Donate**: Support our efforts by contributing to our cause.
    - **Share**: Spread the word about our platform to help us reach more people in need.

    For more information, visit our [website](#) or contact us at [info@anxietyrelief.com](mailto:info@anxietyrelief.com).
    """)

    st.write("---")
    
    # Subscribe for Updates
    st.subheader("Subscribe for Updates")
    st.write("Stay updated with our latest features, activities, and wellness tips.")
    email = st.text_input("Enter your email address:")
    if st.button("Subscribe"):
        if email:
            st.success("Thank you for subscribing! You'll receive updates and tips directly to your inbox.")

    st.write("---")
    st.markdown('<p style="text-align: center;">© 2024 Anxiety Relief Platform. All rights reserved.</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
