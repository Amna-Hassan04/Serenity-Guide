import base64
import datetime
import time
from pymongo import MongoClient
import streamlit as st
import plotly.express as px
import pandas as pd
import requests, random
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
#AI Integration
import anthropic
import datetime
# CSS for Scroll to Top Button
scroll_to_top = """
    <style>
    #scrollButton {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 99;
        font-size: 18px;
        border: none;
        outline: none;
        background-color: rgb(4, 170, 109);
        color: white;
        cursor: pointer;
        padding: 10px;
        border-radius: 10px;
        opacity: 0.7;
    }

    #scrollButton:hover {
        background-color: rgb(4, 170, 109);
        opacity: 1;
    }
    </style>
"""



#Changes made by --Charvi Arora 
#Added security
# Load environment variables from .env file
load_dotenv()
# Retrieve the API key
claude_api_key = os.getenv("CLAUDE_API_KEY")

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

    
# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="SereniFi", page_icon=":relieved:", layout="centered")
st.markdown(scroll_to_top, unsafe_allow_html=True)
def scroll_to_top_button():
    st.markdown('<a id="scrollButton" title="Go to top" href="#top">↑ Top</a>', unsafe_allow_html=True)
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)

scroll_to_top_button()

# Data for mental health (sampled)
data = {
    'Activity': ['Meditation', 'Yoga', 'Breathing', 'Journaling', 'Music'],
    'Calmness_Level': [85, 78, 90, 75, 88]
}

df = px.data.tips()  # Use your actual anxiety relief data

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

# Main function to control page navigation
def main():

    selected = option_menu(
        menu_title=None,
        options=["Home", "Calm Space", "About & Feedback"],
        icons=["house-door-fill", "cloud-sun-fill", "chat-dots-fill"],
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
            "nav-link-selected": {"background-color": "#04AA6D", "color": "#fff","font-size": "14px",}
        }
    )

    if selected == "Home":
        show_main_page()
    elif selected == "Calm Space":
        show_calm_space()
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
    
    #|------MongoDb for Quick Tips For Mental Health Section for inserting and retreiving the tips------|
    #Setting MongoDb connection
    mongodb_uri = os.getenv("MONGODB_URI")
    client=MongoClient(mongodb_uri)
    db = client['serenity_guide_db']
    tips_collection = db['mental_health_tips']

    # Uncomment the following line to populate the database with tips in the format below:
    # tips = []
    # tips_collection.insert_one({"tip": "Take deep breaths to relax."}) 


    st.subheader("Quick Tip for Mental Health")
    all_tips = [] 
    if st.button("Get a Tip"):
        all_tips = list(tips_collection.find({}, {"_id": 0, "tip": 1}))
    
        if all_tips:
            random_tip = random.choice(all_tips)
            st.write(f"Tip: {random_tip['tip']}")
        else:
            st.write("No tips available.")
            st.write(f"Tip: {random.choice(tips)}")
    #!--------------------------------------------------------------------------------------------------|

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
    st.markdown('<p style="text-align: center;">© 2024 SereniFi. All rights reserved.</p>', unsafe_allow_html=True)

#adding spotify playlist feature
def spotifyPlaylist():
    # Embed Spotify API with JavaScript
    spotify_html_podcasts = """

     <style>
      
        /* Styling for the buttons */
        .podcast-button {
            background-color: #1db954; /* Spotify green */
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 20px;
            margin: 10px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Hover effect for buttons */
        .podcast-button:hover {
            background-color: #1aa34a; /* Slightly darker green */
            transform: scale(1.05); /* Small zoom effect */
        }

        /* Active state styling (when clicking the button) */
        .podcast-button:active {
            background-color: #148b3a;
            transform: scale(1);
        }

        /* Fix the container to center align the buttons */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 10px; /* Space between buttons */
        }
    </style>
    
    <script src="https://open.spotify.com/embed/iframe-api/v1" async></script>

    <div id="embed-iframe"></div>
    
    <div class="button-container">
        <!-- Buttons to switch between podcasts -->
        <button class="podcast-button" onclick="loadPodcast('https://open.spotify.com/playlist/77AOjGgwOTmcDiH15lARCh?si=7c76c455e4e74479')">Podcast 1 </button>
        <button class="podcast-button" onclick="loadPodcast('https://open.spotify.com/show/4298EkFJWEK6VAxKARB7bS?si=52e58231da08404a')">Podcast 2</button>
        <button class="podcast-button" onclick="loadPodcast('https://open.spotify.com/show/1QBP6aNv7BsdQWwhqxLcIC?si=d7145f9457ee42b3')">Podcast 3</button>
        <button class="podcast-button" onclick="loadPodcast('https://open.spotify.com/show/69ZUhdV0q2JtibNU2yLTpQ?si=5f6143e2f1744f71')">Podcast 4 </button>
    </div>

    <script type="text/javascript">
    window.onSpotifyIframeApiReady = (IFrameAPI) => {
        let currentController = null;
        const element = document.getElementById('embed-iframe');

        window.loadPodcast = (uri) => {
            const options = { uri: uri };
            if (currentController) {
                currentController.loadUri(uri);  // Update the playlist in the existing controller
            } else {
                IFrameAPI.createController(element, options, (EmbedController) => {
                    currentController = EmbedController;
                });
            }
        };

        // Load the first playlist by default
        loadPodcast('https://open.spotify.com/playlist/77AOjGgwOTmcDiH15lARCh?si=7c76c455e4e74479');
    };
    </script>
    
    """


    # Embed Spotify API with JavaScript
    spotify_html_songs = """

      <style>
      
        /* Styling for the buttons */
        .playlist-button {
            background-color: #1db954; /* Spotify green */
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 20px;
            margin: 10px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Hover effect for buttons */
        .playlist-button:hover {
            background-color: #1aa34a; /* Slightly darker green */
            transform: scale(1.05); /* Small zoom effect */
        }

        /* Active state styling (when clicking the button) */
        .playlist-button:active {
            background-color: #148b3a;
            transform: scale(1);
        }

        /* Fix the container to center align the buttons */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 10px; /* Space between buttons */
        }
    </style>

    <script src="https://open.spotify.com/embed/iframe-api/v1" async></script>

    <div id="embed-iframe"></div>
    
    <div class="button-container">
        <!-- Buttons to switch between playlists -->
        <button  class="playlist-button" onclick="loadPlaylist('https://open.spotify.com/playlist/37i9dQZF1DWXe9gFZP0gtP?si=32e4c036692f4da4')">Stress Relief </button>
        <button class="playlist-button" onclick="loadPlaylist('https://open.spotify.com/playlist/37i9dQZF1DWTC99MCpbjP8?si=1ee785b4c5064848')">Calm</button>
        <button  class="playlist-button" onclick="loadPlaylist('https://open.spotify.com/playlist/37i9dQZF1DXaImRpG7HXqp?si=f4dbafdfb4c94563')">Calming Acoustic</button>
        <button class="playlist-button" onclick="loadPlaylist('https://open.spotify.com/playlist/37i9dQZF1DXcCnTAt8CfNe?si=43381859af3d4869')">Musical Therapy</button>
    </div>

    <script type="text/javascript">
    window.onSpotifyIframeApiReady = (IFrameAPI) => {
        let currentController = null;
        const element = document.getElementById('embed-iframe');

        window.loadPlaylist = (uri) => {
            const options = { uri: uri };
            if (currentController) {
                currentController.loadUri(uri);  // Update the playlist in the existing controller
            } else {
                IFrameAPI.createController(element, options, (EmbedController) => {
                    currentController = EmbedController;
                });
            }
        };

        // Load the first playlist by default
        loadPlaylist('https://open.spotify.com/playlist/37i9dQZF1DWXe9gFZP0gtP?si=32e4c036692f4da4');
    };
    </script>
    """

    st.write("Explore our collection of insightful podcasts that empower you with expert advice, inspiring stories, and practical tools to enhance your mental well-being.")
    # Display the HTML component in Streamlit
    components.html(spotify_html_podcasts, height=415)

    st.write("Dive into our curated playlists featuring calming and therapeutic music designed to soothe your mind and uplift your spirit, creating a harmonious backdrop for your mental health journey.")
    # Display the HTML component in Streamlit
    components.html(spotify_html_songs, height=415)


def soothing_sounds():
    st.subheader("🎵 Calm Down with Soothing Sounds")
    #Contributions made by Himanshi-M
    sound_options = {
        "Rain": "https://cdn.pixabay.com/audio/2022/05/13/audio_257112ce99.mp3",
        "Ocean Waves": "https://cdn.pixabay.com/audio/2022/06/07/audio_b9bd4170e4.mp3",
        "Forest": "https://cdn.pixabay.com/audio/2022/03/10/audio_4dedf5bf94.mp3",
        "Birds Chirping":"https://cdn.pixabay.com/audio/2022/03/09/audio_c610232c26.mp3",
        "River Flowing":"https://cdn.pixabay.com/audio/2024/07/30/audio_319893354c.mp3",
        "White Noise":"https://cdn.pixabay.com/audio/2022/03/12/audio_b4f7e5a4ff.mp3",
        "Pink Noise": "https://cdn.pixabay.com/audio/2023/10/07/audio_df9c190caf.mp3"
    }
    selected_sound = st.selectbox("Choose a sound to relax:", list(sound_options.keys()))
    # Organizing the button, checkbox and volume slider on the same row
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        playbutton=st.button("Play Sound")
    with col2:
        # Looping Checkbox
        loopcheckbox = st.checkbox("Loop Sound")

    if playbutton:
        # Rendering the audio player and JS in the app
        with col3:
            st.audio(sound_options[selected_sound], format="audio/mp3", loop=loopcheckbox)
    
    spotifyPlaylist()

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
    st.markdown("Relax with a fun mini-game to distract your mind. Choose the game yo want:")
    st.markdown("[Play Pacman](https://www.google.co.in/search?q=pacman&sca_esv=aaaa9a10aaa1b9d1&sca_upv=1&sxsrf=ADLYWIJzV0yNeS6YptYfZn5AEFUKvBUtSw%3A1725304252827&ei=vA3WZqCaMrLy4-EPiZmBwAw&ved=0ahUKEwig6PmY-6SIAxUy-TgGHYlMAMgQ4dUDCBA&uact=5&oq=pacman&gs_lp=Egxnd3Mtd2l6LXNlcnAiBnBhY21hbjIQEC4YgAQYsQMYQxiDARiKBTIOEC4YgAQYkQIYsQMYigUyEBAAGIAEGLEDGEMYgwEYigUyExAuGIAEGLEDGEMYgwEY1AIYigUyChAuGIAEGEMYigUyChAAGIAEGEMYigUyBRAAGIAEMg0QABiABBixAxhDGIoFMggQABiABBixAzIFEAAYgAQyHxAuGIAEGLEDGEMYgwEYigUYlwUY3AQY3gQY4ATYAQFI3hZQ5A5Y8BRwAXgBkAEAmAHlAaABiwqqAQMyLTa4AQPIAQD4AQGYAgegAp8LwgIKEAAYsAMY1gQYR8ICBBAjGCfCAgoQIxiABBgnGIoFwgILEAAYgAQYkQIYigXCAg4QABiABBixAxiDARiKBcICCxAAGIAEGLEDGIMBwgIOEC4YgAQYkQIY1AIYigXCAhAQLhiABBhDGMcBGIoFGK8BmAMAiAYBkAYGugYGCAEQARgUkgcFMS4wLjagB5Vj&sclient=gws-wiz-serp)")
    st.markdown("[Play Thinking Brain](https://kidshelpline.com.au/games/thinking-brain)")
    st.markdown("[Play Snake Game](https://www.google.co.in/search?si=ACC90nwm_DCLUGduakF5oU94y1HpDc2j-V_TsJpED11KWNYygOhydoKqqSH9t8iyybygqTEoKMZa&biw=1536&bih=695&dpr=1.25)")


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
        st.write("Remember, consistency is key to building habits and improving your mental well-being.")

        #Progress Bar Feature added by suhaib-lone
        if st.button("Start Progress"):
            progress_bar=st.progress(0)
            if selected_challenge == "Meditation" or selected_challenge == "journaling":
                challenge_time=600
            elif selected_challenge == "Yoga":
                challenge_time=900
            elif selected_challenge == "Breathing":
                challenge_time=300
            else:
                challenge_time=1200
            for i in range(challenge_time):
                time.sleep(1)
                progress_bar.progress((i+1)/challenge_time)
            st.success("Ding! Ding! Time UP!")



    st.write("---")

    st.subheader("Daily Anxeity Check")
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
        mood_boosting_mini_games()

    st.write("---")
    soothing_sounds()

    st.write("---")

    st.subheader("Interactive Journaling")
    if st.button("Submit Journal Entry"):
        st.success("Journal entry: It's important to reflect and release your emotions.")
        interactive_journal()



    st.write("---")
    st.markdown('<p style="text-align: center;">© 2024 SereniFi. All rights reserved.</p>', unsafe_allow_html=True)




def show_about_and_feedback():
    st.title("About Us & Feedback")
    
    st.write("""
    **Welcome to SereniFi!**
    
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
    st.markdown('<p style="text-align: center;">© 2024 SereniFi. All rights reserved.</p>', unsafe_allow_html=True)





if __name__ == "__main__":
    main()
