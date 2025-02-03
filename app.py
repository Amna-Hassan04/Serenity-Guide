import base64
import datetime
import time

#from pymongo import MongoClient
import streamlit as st
import plotly.express as px
import pandas as pd
import requests, random
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
import logging
import sys
#from affirmation_widget import display_affirmation_widget

st.set_page_config(page_title="SereniFi", page_icon=":relieved:", layout="wide")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logging.info("Application started.")

def global_error_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Call the default handler for KeyboardInterrupt
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Set the global error handler
sys.excepthook = global_error_handler

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
        background-color: rgb(4, 170, );
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
    logging.info(f"Entering get_img_as_base64 with file: {file}")
    try:
        with open(file, "rb") as f:
            data = f.read()
        encoded_data = base64.b64encode(data).decode()
        logging.info(f"Successfully encoded file: {file}")
        return encoded_data
    except Exception as e:
        logging.error(f"Error in get_img_as_base64 with file {file}: {e}")
        raise
    finally:
        logging.info(f"Exiting get_img_as_base64 with file: {file}")
        
# Animated background
page_bg_img = f"""
<style>
/* Animated background gradient */
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(-45deg, #f7b1ab, #fbd6c8, #d7ecef, #b7dfe5);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stSidebar"] > div:first-child {{
background: linear-gradient(-45deg, #f7b1ab, #fbd6c8, #d7ecef, #b7dfe5);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0); /* Transparent header */
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
    logging.info(f"Fetching Lottie animation from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        logging.info(f"Successfully fetched Lottie animation from URL: {url}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching Lottie animation from URL {url}: {e}")
        st.error("Failed to fetch Lottie animation. Please try again later.")
        return None


#Footer Function to show footer and bottom nav
def show_footer():
    st.write("---")
    
    # Define the HTML for the footer
    footer_html = """
    <style>
        .footer {
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            color: #333;
        }
        .social-icons {
            margin-top: 5px; /* Space above icons */
        }
        .social-icons a {
            margin: 0 10px; /* Spacing between icons */
            color: #333; /* Icon color */
            text-decoration: none; /* Remove underline from links */
            font-size: 20px; /* Icon size */
        }
        .social-icons a:hover {
            color: #007bff; /* Change color on hover */
        }
        .footer-links {
            margin-top: 10px;
            font-size: 14px; /* Link font size */
        }
        .footer-links a {
            margin: 0 15px; /* Space between links */
            color: #333;
            text-decoration: none;
        }
        .footer-links a:hover {
            text-decoration: underline; /* Underline on hover */
        }
        .newsletter {
            margin-top: 10px;
        }
        .newsletter input {
            padding: 5px;
            font-size: 14px;
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 0.5);
            border: 1px solid #000;
        }
        .newsletter button {
            padding: 5px 10px;
            font-size: 14px;
            margin-left: 5px;
            cursor: pointer;
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 0.5);
            border: 1px solid #000;
        }
        .newsletter button:hover {
            background-color: rgba(0, 123, 255, 0.3); 
        }
    </style>
    
    <!-- Load Font Awesome from CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

    <div class="footer">
        <p>© 2024 SereniFi. All rights reserved.</p>
        <div class="social-icons">
            <a href="https://www.linkedin.com/in/amna-hassan-143b76202/" target="_blank">
                <i class="fab fa-linkedin" title="LinkedIn"></i>
            </a>
            <a href="https://github.com/Amna-Hassan04/Serenity-Guide" target="_blank">
                <i class="fab fa-github" title="GitHub"></i>
            </a>
            <a href="https://www.facebook.com" target="_blank">
                <i class="fab fa-facebook" title="Facebook"></i>
            </a>
            <a href="https://www.twitter.com" target="_blank">
                <i class="fab fa-twitter" title="Twitter"></i>
            </a>
            <a href="https://www.instagram.com" target="_blank">
                <i class="fab fa-instagram" title="Instagram"></i>
            </a>
        </div>
        <div class="footer-links">
            <a class = "foot-links" href="#" target="_blank">Terms and Conditions</a>
            <a class = "foot-links" href="#" target="_blank">Privacy Policy</a>
            <a class = "foot-links" href="#" target="_blank">About Us</a>
            <a class = "foot-links" href="#" target="_blank">Contact Us</a>
        </div>
        <div class = "Acknowledgements">
            <p>Hackathon Project created by Amna Hassan, Anushka Pote, Madhuri K, Pearl Vashistha. <br>
            Maintained and Features added by Contributors. 
            </p>
        </div>
    </div>
    """
    
    # Render the HTML in the footer
    st.markdown(footer_html, unsafe_allow_html=True)

# Main function to control page navigation
def main():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Calm Space", "FAQs"],
        icons=["house-door-fill", "cloud-sun-fill", "chat-dots-fill", "question-circle-fill"],
        menu_icon="sun",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "4!important",
                "background-color": "#333",
                "border-radius": "5px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "min-width": "100px",
                "max-width": "100%",
            },
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "-10 20px ",

                "--hover-color": "#ddd",
                "border-radius": "10px",
                "color": "#fff",
                "background-color": "rgba(0, 0, 0, 0.8)",
                "transition": "background-color 0.3s ease, transform 0.2s"
            },
            "nav-link-selected": {
                "background-color": "#04AA6D",
                "color": "#fff",
                "font-size": "14px",
            }
        }
    )

    if selected == "Home":
        show_main_page()
    elif selected == "Calm Space":
        show_calm_space()
    elif selected == "About & Feedback":
        show_about_and_feedback()
    elif selected == "FAQs":
        show_FAQs_page()


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

    # Quick Tip for Mental Health Section
    st.subheader("Quick Tip for Mental Health")
    if st.button("Get a Tip"):
        tips = [
            "Take deep breaths to relax.",
            "Go for a walk in nature.",
            "Write down three things you're grateful for.",
            "Take a moment to stretch your body.",
            "Listen to your favorite calming music."
        ]
        st.write(f"**Tip:** {random.choice(tips)}")

    st.write("---")

    # Lottie animation
    lottie_url_breathing = "https://lottie.host/89b3ab99-b7ee-4764-ac3a-5fe1ef057bde/WaOPmT23PU.json"
    lottie_json_breathing = load_lottie_url(lottie_url_breathing)

    if lottie_json_breathing:
        st_lottie(lottie_json_breathing, speed=1, width=300, height=300, key="breathing-animation")

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

    show_footer()

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

    logging.info("Displaying podcast collection description")
    st.write("Explore our collection of insightful podcasts that empower you with expert advice, inspiring stories, and practical tools to enhance your mental well-being.")

    try:
        logging.info("Displaying Spotify podcasts HTML component")
        components.html(spotify_html_podcasts, height=415)
    except Exception as e:
        logging.error(f"Error displaying Spotify podcasts HTML component: {e}")
        st.error("Failed to load podcasts. Please try again later.")

    logging.info("Displaying music playlist description")
    st.write("Dive into our curated playlists featuring calming and therapeutic music designed to soothe your mind and uplift your spirit, creating a harmonious backdrop for your mental health journey.")

    try:
        logging.info("Displaying Spotify songs HTML component")
        components.html(spotify_html_songs, height=415)
    except Exception as e:
        logging.error(f"Error displaying Spotify songs HTML component: {e}")
        st.error("Failed to load music playlists. Please try again later.")

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
        logging.info("Play button clicked")
        try:
            # Rendering the audio player and JS in the app
            with col3:
                logging.info(f"Playing sound: {selected_sound}")
                st.audio(sound_options[selected_sound], format="audio/mp3", loop=loopcheckbox)
        except Exception as e:
            logging.error(f"Error playing sound: {selected_sound}, Error: {e}")
            st.error("Failed to play the selected sound. Please try again later.")

    try:
        logging.info("Displaying Spotify playlist")
        spotifyPlaylist()
    except Exception as e:
        logging.error(f"Error displaying Spotify playlist: {e}")
        st.error("Failed to load Spotify playlist. Please try again later.")

def interactive_journal():
    logging.info("Rendering interactive journal")

    if 'journal_entries' not in st.session_state:
        logging.info("Initializing journal_entries in session state")
        st.session_state.journal_entries = []

    journal_input = st.text_area("📝 Daily Journal", placeholder="Write down your thoughts...")
    if st.button("Save Entry"):
        logging.info("Save Entry button clicked")
        try:
            st.session_state.journal_entries.append({
                "date": datetime.datetime.now(),
                "entry": journal_input
            })
            logging.info("Journal entry saved")
            st.success("Journal entry saved!")
        except Exception as e:
            logging.error(f"Error saving journal entry: {e}")
            st.error("Failed to save journal entry. Please try again later.")

    # Display past journal entries
    if st.checkbox("Show Past Entries"):
        logging.info("Show Past Entries checkbox selected")
        st.write("### Past Journal Entries:")
        for entry in st.session_state.journal_entries:
            logging.info(f"Displaying journal entry from {entry['date'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**{entry['date'].strftime('%Y-%m-%d %H:%M:%S')}**: {entry['entry']}")

def mood_boosting_mini_games():
    st.markdown("Relax with a fun mini-game to distract your mind. Choose the game you want:")
    
    # Define button style with off-black background and off-white text color
    button_style = """
        <style>
        .button {
            background-color: #1a1a1a;  /* off-black */
            color: #f5f5f5;  /* off-white */
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .button a {
            color: #f5f5f5;  /* off-white text */
            text-decoration: none;  /* remove underline */
        }
        .button a:hover {
            color: #f5f5f5;  /* off-white text on hover */
        }
        .button:hover {
            background-color: #333;  /* slightly lighter on hover */
        }
        </style>
    """
    
    # Apply the button style to the Streamlit app
    st.markdown(button_style, unsafe_allow_html=True)

    # Create a table with multiple game buttons
    st.markdown('''
        <table>
            <tr>
                <td><a href="https://g.co/kgs/o4uSVto" target="_blank"><div class="button">Play Pacman</div></a></td>
                <td><a href="https://kidshelpline.com.au/games/thinking-brain" target="_blank"><div class="button">Play Thinking Brain</div></a></td>
                <td><a href="https://www.google.com/search?q=snake+game" target="_blank"><div class="button">Play Snake Game</div></a></td>
                <td><a href="https://agar.io/" target="_blank"><div class="button">Play Agar.io</div></a></td>
            </tr>
            <tr>
                <td><a href="https://trex-runner.com/" target="_blank"><div class="button">Play T-Rex Game</div></a></td>
                <td><a href="https://slither.io/" target="_blank"><div class="button">Play Slither.io</div></a></td>
                <td><a href="https://www.google.com/search?q=solitaire" target="_blank"><div class="button">Play Solitaire</div></a></td>
                <td><a href="https://mahjon.gg/" target="_blank"><div class="button">Play Mahjong</div></a></td>
            </tr>
            <tr>
                <td><a href="https://sudoku.com/" target="_blank"><div class="button">Play Sudoku</div></a></td>
                <td><a href="https://www.crazygames.com/game/fireboy-and-watergirl-the-forest-temple" target="_blank"><div class="button">Play Fireboy & Watergirl</div></a></td>
                <td><a href="https://checkers.online/" target="_blank"><div class="button">Play Checkers</div></a></td>
                <td><a href="https://krunker.io/" target="_blank"><div class="button">Play Krunker.io</div></a></td>
            </tr>
        </table>
        <br>
    ''', unsafe_allow_html=True)

#Simon Game Challenge

def simon_game_challenge():
    st.markdown("## Simon Game Challenge")

    # Description, Instructions, and Play Game button in a table format
    st.markdown("""
    <style>
        .game-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .game-table th, .game-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }
        .game-table th {
            font-weight: bold;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            color: white;
            background-color: white;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
        }
        .button:hover {
            background-color: black ;
            font-color: red;
        }
    </style>

    <table class="game-table">
        <tr>
            <th>Description</th>
            <th>Instructions</th>
            <th>Play Game</th>
        </tr>
        <tr>
            <td>
                The Simon Game Challenge tests your memory and focus as you follow an
                increasingly complex sequence of flashing colors and sounds. 
                Each level adds a new step to the pattern, which you must repeat perfectly to advance. 
                One mistake ends the game.
            </td>
            <td>
                <ul>
                    <li><b>Press any key</b> on your keyboard to start the game.</li>
                    <li>Watch as <b>one block will light up</b> or make a sound. Click that block to match the sequence.</li>
                    <li>The sequence will get longer with each level. Follow it correctly to advance.</li>
                    <li>If you make a mistake, the game will end, and your <b>final score</b> will display.</li>
                </ul>
            </td>
            <td style="text-align: center;">
                <a href="https://sanyadureja.github.io/Simon-Game-JavaScript-jQuery/" target="_blank" class="button">
                    Simon Game Challenge
                </a>
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

import streamlit as st
import logging
import time

def show_calm_space():
    # Set page layout to wide
    
    st.title("Calm Space")
    st.write("Engage in a breathing exercise to calm your mind.")

    # Section: Daily Affirmations in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(175, 158, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>💬 Daily Affirmations</h3>
                <p>Start your day with positive affirmations to center your thoughts.</p>
                <!-- Uncomment when function is available -->
                <!-- display_affirmation_widget() -->
            </div>
            """, unsafe_allow_html=True
        )

    # Section: Quick Tips for Positivity in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(165, 175, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>🌟 Quick Tips for Positivity</h3>
                <ul>
                    <li>Take a deep breath and count to 5.</li>
                    <li>Focus on what you can control, not on what you can't.</li>
                    <li>Take a moment to reflect on something you're grateful for.</li>
                    <li>Smile at yourself in the mirror.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )

    st.write("---")

    # Section: Daily Challenge Suggestions in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(168, 175, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>🎯 Daily Challenge Suggestions</h3>
                <p>Choose a challenge to engage with today:</p>
            
            """, unsafe_allow_html=True
        )

        challenges = {
            "Meditation": "Try a 10-minute guided meditation session today. Find a quiet space and focus on your breath.",
            "Yoga": "Follow a 15-minute yoga routine to stretch and relax your body. Check out a video for guidance.",
            "Breathing": "Engage in deep breathing exercises for 5 minutes. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale slowly.",
            "Journaling": "Spend 10 minutes writing down your thoughts and feelings. Reflect on your day and your emotions.",
            "Music": "Listen to calming music or nature sounds for 20 minutes. Allow the sounds to help you relax and unwind."
        }
        
        selected_challenge = st.selectbox("Choose an activity for your daily challenge:", options=list(challenges.keys()))
        if selected_challenge:
            logging.info(f"Challenge started: {selected_challenge}")
            st.write(f"**Today's Challenge:** {challenges[selected_challenge]}")
            st.write("Remember, consistency is key to building habits and improving your mental well-being.")

            # Progress Bar Feature
            if st.button("Start Progress"):
                progress_bar = st.progress(0)
                challenge_time = {
                    "Meditation": 600,
                    "Yoga": 900,
                    "Breathing": 300,
                    "Journaling": 600,
                    "Music": 1200
                }[selected_challenge]

                for i in range(challenge_time):
                    time.sleep(1)
                    progress_bar.progress((i + 1) / challenge_time)
                st.success("Ding! Ding! Time UP!")
            
    st.write("---")

    # Section: Daily Anxiety Check in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(175, 172, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>🧠 Daily Anxiety Check</h3>
                <p>Check in with your emotions and start managing your anxiety.</p>
            </div>
            """, unsafe_allow_html=True
        )

        mood = st.selectbox("How are you feeling today?", ["Anxious", "Stressed", "Overwhelmed", "Calm", "Other"])
        feeling_description = st.text_area("What exactly are you feeling?", placeholder="Describe your feelings here...")
        current_stress_level = st.slider("Current Stress Level (1 to 10)", 1, 10, value=5)
        recent_events = st.text_area("Recent Events", placeholder="Describe any recent events that may have contributed to your anxiety or stress...")

        if st.button("Submit"):
            logging.info("Mood form submitted")
            st.write("Thank you for sharing. Let’s find some exercises to help you.")
            guidance = anxiety_management_guide(mood, feeling_description, current_stress_level, recent_events)
            st.write(guidance)

    st.write("---")

    # Section: Mood-Boosting Games in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(168, 175, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>🎮 Mood-Boosting Games</h3>
                <p>Take a break and play games to reduce your anxiety.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Mini Games"):
                logging.info("Mood boosting game started")
                st.write("Launching a quick mood-boosting game...")
                mood_boosting_mini_games()

        with col2:
            if st.button("Simon Game Challenge"):
                logging.info("Simon game challenge started")
                st.write("Starting the Simon Game Challenge!")
                simon_game_challenge()

    st.write("---")

    # Section: Soothing Sounds in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(168, 175, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>🎶 Soothing Sounds</h3>
                <p>Relax with calming sounds to ease your mind.</p>
            </div>
            """, unsafe_allow_html=True
        )

        soothing_sounds()

    st.write("---")

    # Section: Interactive Journaling in a box
    with st.container():
        st.markdown(
            """
            <div style="border: 2px solidrgb(168, 175, 76); border-radius: 8px; padding: 20px; background-color: #e8f5e9;">
                <h3>📓 Interactive Journaling</h3>
                <p>Reflect and release your emotions with journaling.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.write("")

        if st.button("Submit Journal Entry"):
            st.success("Journal entry: It's important to reflect and release your emotions.")
            interactive_journal()

    # Footer Section
    show_footer()
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
        logging.info("'Submit Feedback' button clicked")
        if feedback_activity:
            logging.info("Feedback activity provided")
            st.success("Thank you for sharing your experience! Your feedback is valuable and appreciated.")
        else:
            logging.info("No feedback activity provided")
            st.warning("Please provide feedback before submitting.")   

    st.write("---")
    
    # Our Advertising Partners
    st.subheader("Our Advertising Partners")
    st.write("Check out our partners in mental wellness products and services:")
    st.write("- **Mindfulness App**: An app offering guided meditations and mindfulness exercises.")
    st.write("- **Relaxation Techniques Guide**: A comprehensive guide to various relaxation techniques and their benefits.")
    
    st.write("---")
    
    # Call to Action
    st.subheader("Get Involved")
    
    # Using st.markdown with HTML to style the links
    st.markdown("""
    <p>
    Interested in supporting our mission? There are several ways you can get involved:
    <ul>
    <li><strong>Volunteer</strong>: Join our team of volunteers to help others benefit from our platform.</li>
    <li><strong>Donate</strong>: Support our efforts by contributing to our cause.</li>
    <li><strong>Share</strong>: Spread the word about our platform to help us reach more people in need.</li>
    </ul>
    </p>
    <p>
    For more information, visit our <a href="#" style="color: #101010; text-decoration: underline; text-decoration-color: white;">website</a> 
    or contact us at <a href="mailto:info@anxietyrelief.com" style="color: #101010; text-decoration: underline; text-decoration-color: white;">info@anxietyrelief.com</a>.
    </p>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # Subscribe for Updates
    st.subheader("Subscribe for Updates")
    st.write("Stay updated with our latest features, activities, and wellness tips.")

    email = st.text_input("Enter your email address:")
    if st.button("Subscribe"):
        logging.info("'Subscribe' button clicked")
        if email:
            logging.info(f"Subscription email provided: {email}")
            st.success("Thank you for subscribing! You'll receive updates and tips directly to your inbox.")

    
        else:
            logging.info("No email provided for subscription")
            st.warning("Please enter your email address to subscribe.")

    st.write("---")
    st.markdown('<p style="text-align: center;">© 2024 SereniFi. All rights reserved.</p>', unsafe_allow_html=True)    

import streamlit as st

def show_resources():
    st.title("Mental Health Resources")

    # Sidebar menu for personalized self-care routine
    st.sidebar.title("Personalized Self-Care Routine")
    
    # Initialize a session state to store activities
    if 'activities' not in st.session_state:
        st.session_state.activities = []

    # Create a form to collect user inputs for the routine
    with st.sidebar.form(key='self_care_form'):
        st.subheader("Create Your Self-Care Routine")
        
        # User inputs
        activity = st.text_input("Self-Care Activity")
        duration = st.number_input("Duration (in minutes)", min_value=1, max_value=120)
        frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
        
        # Submit button
        submit_button = st.form_submit_button(label='Add Activity')

        if submit_button:
            logging.info("Submit button clicked")
            try:
                # Append the activity to the session state
                st.session_state.activities.append((activity, duration, frequency))
                logging.info(f"Added activity: {activity}, duration: {duration}, frequency: {frequency}")
                st.success(f"Added '{activity}' for {duration} minutes {frequency}!")
            except Exception as e:
                logging.error(f"Error adding activity: {e}")
                st.error("Failed to add activity. Please try again later.")
                
    # Mental Health Articles
    st.header("Mental Health Articles")

    # Add custom CSS for hover effect
    st.markdown("""
        <style>
        .hover-effect img {
            transition: transform 0.2s ease; /* Animation */
        }
        .hover-effect img:hover {
            transform: scale(1.1); /* Zoom in */
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns for side-by-side images
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<a href="https://www.medicalnewstoday.com/articles/323454#symptoms" class="hover-effect">'
            '<img src="https://files.oaiusercontent.com/file-XQXu69JDDd7GRnNedvL1Ld32?se=2024-10-15T10%3A18%3A18Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D8067e13f-e01a-4f98-bb8b-3032dfd8842c.webp&sig=HZ53OvoLQPLoord2sM7aM3iRJZeSVRgueC2u1owUWYY%3D" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<a href="https://www.snhu.edu/about-us/newsroom/health/what-is-self-care" class="hover-effect">'
            '<img src="https://files.oaiusercontent.com/file-chhKTLGaIokEFRTf9aEh4lAc?se=2024-10-15T10%3A15%3A01Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D8c89f7ff-469c-4777-9adf-d5bc5898c1f1.webp&sig=TD4oofQ1tP7MI6OyCIK39rHiUjb1B2LjLx2%2Bj9NxAHM%3D" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<a href="https://www.helpguide.org/mental-health/depression/coping-with-depression" class="hover-effect">'
            '<img src="https://files.oaiusercontent.com/file-oSz9p3oO0nr9Kl34h6M02W7h?se=2024-10-15T10%3A01%3A31Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D42222272-d7ea-487d-84ee-7a5b57eefca4.webp&sig=8SCuBVJkYA2c5CGjynpFlkchayZ5L2PIrdwGVkXEO84%3D" width="100%" />'
            '</a>', unsafe_allow_html=True
        )


    # Self-Care Tips
    st.header("Self-Care Tips")

    # Adding the Self-Care Ideas image
    st.image("https://cdn.shopify.com/s/files/1/0400/8574/9923/files/Self_Care_Ideas_grande.png?v=1591248756", 
             caption="Self-Care Ideas", use_column_width=True)

    # Adding the second image
    st.image("https://pmhsredandblack.com/wp-content/uploads/2019/01/for-Olivias-article-895x900.jpg", 
             caption="Additional Self-Care Resource", use_column_width=True)

    # Add the YouTube video below the images
    st.video("https://www.youtube.com/watch?app=desktop&v=LY4i5CSn7AA")

    # Display user-added self-care activities
    if st.session_state.activities:
        st.subheader("Your Self-Care Routine")
        for activity, duration, frequency in st.session_state.activities:
            st.markdown(f"- **Activity**: {activity}, **Duration**: {duration} minutes, **Frequency**: {frequency}")

    # Guides & E-books
    st.header("Guides & E-books")

    # Add custom CSS for hover effect
    st.markdown("""
        <style>
        .guide-hover img {
            transition: transform 0.2s ease; /* Animation */
        }
        .guide-hover img:hover {
            transform: scale(1.1); /* Zoom in */
        }
        </style>
    """, unsafe_allow_html=True)

    # Create a container for the images
    guide_col1, guide_col2, guide_col3 = st.columns(3)

    with guide_col1:
        st.markdown(
            '<a href="https://www.gnyha.org/wp-content/uploads/2020/06/Building-Resilience-UCD.pdf" class="guide-hover">'
            '<img src="https://storage.vivago.ai/image/p_b42d7fea-8ae2-11ef-978e-0ab00016590f.jpg?width=512" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    with guide_col2:
        st.markdown(
            '<a href="https://www.mindful.org/an-introduction-to-mindful-gratitude/" class="guide-hover">'
            '<img src="https://storage.vivago.ai/image/p_72510c1e-8ae6-11ef-8e7f-4ed4b81f76cb.jpg?width=512" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    with guide_col3:
        st.markdown(
            '<a href="https://iris.who.int/bitstream/handle/10665/205887/B5084.pdf" class="guide-hover">'
            '<img src="https://storage.vivago.ai/image/p_d1074afe-8ae4-11ef-924c-9afd28bf6444.jpg?width=512" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    # Podcast/Audio Library
    st.header("Podcast/Audio Library")


    # Add custom CSS for hover effect
    st.markdown("""
        <style>
        .podcast-hover img {
            transition: transform 0.2s ease; /* Animation */
        }
        .podcast-hover img:hover {
            transform: scale(1.1); /* Zoom in */
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns for side-by-side podcast images
    podcast_col1, podcast_col2, podcast_col3 = st.columns(3)

    # The Anxiety Coaches Podcast
    with podcast_col1:
        st.markdown(
            '<a href="https://player.fm/series/the-anxiety-coaches-podcast" class="podcast-hover">'
            '<img src="https://cdn.player.fm/images/230641/series/Ut7N671x7htRnKjm/256.jpg" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    # The Self-Esteem and Confidence Mindset
    with podcast_col2:
        st.markdown(
            '<a href="https://podcasts.apple.com/gb/podcast/the-self-esteem-and-confidence-mindset/id1497438573" class="podcast-hover">'
            '<img src="https://is1-ssl.mzstatic.com/image/thumb/Podcasts116/v4/a0/f5/c5/a0f5c592-4e41-de36-e9fe-3981dcaf986e/mza_17991338792145651433.jpg/300x300bb.webp" width="100%" />'
            '</a>', unsafe_allow_html=True
        )

    # Spotify Podcast - Overcoming Anxiety
    with podcast_col3:
        st.markdown(
            '<a href="https://open.spotify.com/show/5M5D6lihTbDs8aRnb6xazq" class="podcast-hover">'
            '<img src="https://i.scdn.co/image/ab6765630000ba8ac3cc83aee70191fa17f56934" width="100%" />'
            '</a>', unsafe_allow_html=True
        )
def show_FAQs_page():
    st.title("Frequently Asked Questions (FAQs)")
    
    st.markdown("""
    <style>
    .faq-question {
        font-size: 18px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 10px;
    }
    .faq-answer {
        font-size: 16px;
        color: #555555;
        line-height: 1.6;
    }
    .faq-header {
        font-size: 24px;
        font-weight: bold;
        color: #2C3E50;
    }
    .additional-questions {
        font-size: 18px;
        font-weight: bold;
        color: #2C3E50;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="faq-header">Welcome to the SereniFi FAQ Section!</div>', unsafe_allow_html=True)
    st.write("""
    Here you'll find answers to some of the most common questions about our platform, services, and how to make the most of your experience.
    """)

    st.write("---")

    with st.expander("1. What is SereniFi?"):
        st.markdown('<div class="faq-question">What is SereniFi?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">SereniFi is a mental wellness platform dedicated to promoting mental well-being through interactive tools and resources. Our goal is to help individuals manage anxiety, stress, and improve their overall mental health.</div>', unsafe_allow_html=True)

    with st.expander("2. How can SereniFi help with anxiety?"):
        st.markdown('<div class="faq-question">How can SereniFi help with anxiety?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">SereniFi offers a variety of activities, guided meditations, relaxation techniques, and resources designed to reduce stress and anxiety. We also provide tools to track your progress and find what works best for you.</div>', unsafe_allow_html=True)

    with st.expander("3. Is SereniFi free to use?"):
        st.markdown('<div class="faq-question">Is SereniFi free to use?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Yes, SereniFi offers free access to most of its tools and resources. Some premium features might require a subscription, but we ensure that the essential tools for mental wellness are always available to everyone at no cost.</div>', unsafe_allow_html=True)

    with st.expander("4. Can I use SereniFi on my mobile device?"):
        st.markdown('<div class="faq-question">Can I use SereniFi on my mobile device?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Absolutely! SereniFi is designed to be mobile-friendly, so you can access all features and resources from your smartphone or tablet, no matter where you are.</div>', unsafe_allow_html=True)

    with st.expander("5. How do I provide feedback or get support?"):
        st.markdown('<div class="faq-question">How do I provide feedback or get support?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">We value your feedback and encourage you to share your thoughts. You can visit our \'About Us & Feedback\' page to submit your feedback or email us directly at <a href="mailto:info@anxietyrelief.com">info@anxietyrelief.com</a>.</div>', unsafe_allow_html=True)

    with st.expander("6. Is my data safe with SereniFi?"):
        st.markdown('<div class="faq-question">Is my data safe with SereniFi?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Your privacy is our top priority. We use state-of-the-art encryption and data protection measures to ensure that your information remains safe and confidential.</div>', unsafe_allow_html=True)

    with st.expander("7. Can I customize my wellness plan on SereniFi?"):
        st.markdown('<div class="faq-question">Can I customize my wellness plan on SereniFi?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Yes, you can tailor your wellness activities and resources according to your needs and preferences. SereniFi allows you to choose the techniques and exercises that work best for you.</div>', unsafe_allow_html=True)

    with st.expander("8. How do I join the SereniFi community?"):
        st.markdown('<div class="faq-question">How do I join the SereniFi community?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">You can join the SereniFi community by signing up on our platform. You\'ll gain access to support groups, forums, and events where you can connect with others on their mental wellness journey.</div>', unsafe_allow_html=True)

    with st.expander("9. What types of mental health professionals contribute to SereniFi?"):
        st.markdown('<div class="faq-question">What types of mental health professionals contribute to SereniFi?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Our platform is supported by a diverse team of mental health professionals, including psychologists, wellness coaches, and therapists, who provide insights and guidance on our resources and tools.</div>', unsafe_allow_html=True)

    with st.expander("10. Are the activities on SereniFi backed by scientific research?"):
        st.markdown('<div class="faq-question">Are the activities on SereniFi backed by scientific research?</div>', unsafe_allow_html=True)
        st.markdown('<div class="faq-answer">Yes, our activities and techniques are grounded in evidence-based practices. We aim to provide methods that are scientifically proven to reduce anxiety and improve mental wellness.</div>', unsafe_allow_html=True)

    st.write("---")

    st.markdown('<div class="additional-questions">Have More Questions?</div>', unsafe_allow_html=True)
    st.write("""
    If you have any other questions that aren't listed here, feel free to reach out to us at [info@anxietyrelief.com](mailto:info@anxietyrelief.com). We're here to help you get the most out of SereniFi!!
    """)

    st.write("---")
    st.markdown('<p style="text-align: center; font-size: 14px; color: #888888;">© 2024 SereniFi. All rights reserved.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()