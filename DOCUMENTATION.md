##                                                                                      Anxiety Relief Platform Documentation

## 1. Project Overview
The Anxiety Relief Platform is a Streamlit-based web application designed to help users manage anxiety and mental health. This app leverages Anthropic’s Claude API to deliver personalized tips based on user input, along with features like relaxation exercises, visualizations, and mental health-related games.



## 2. Features

AI-Powered Recommendations: Integrates Claude AI to offer personalized anxiety management advice.
Interactive UI: Features relaxation exercises, games, breathing techniques, and daily challenges.
Data Visualization: Shows the effectiveness of calming activities through interactive charts.
Accessible Design: User-friendly interface with custom styling for a calming user experience.
Logging & Exception handling: Improves debugging and error tracking.


## 3. Libraries and Dependencies

The application requires the following Python libraries:

streamlit: Builds the app's user interface.
plotly.express: Creates interactive data visualizations.
requests: Fetches data for animations and external API interactions.
anthropic: Interacts with Claude AI for personalized recommendations.
streamlit_lottie: Integrates Lottie animations.
pandas: Handles dataframes for data visualization.
base64: Encodes images and animations.

To install the dependencies:

```bash

pip install streamlit pandas plotly requests anthropic streamlit_lottie
```

## 4. Claude AI Integration

Claude API is used to provide tailored anxiety management recommendations based on user input, such as mood, stress level, and recent events.

Example usage:

```bash
client = anthropic.Client(api_key=claude_api_key)

def anxiety_management_guide(mood, feeling_description, stress_level, recent_events):
    message = client.messages.create(
        prompt=f"User's mood: {mood}, stress level: {stress_level}. Recent events: {recent_events}",
        model="claude-v1"
    )
    return message['completion']
```

## 5. Application Structure

## 5.1 Navigation Menu
The app has three main sections:

Home: Breathing exercises, personalized tips, and mental health resources.
Calm Space: Includes interactive tools like daily challenges, soothing sounds, and mood-boosting games.
About & Feedback: Information about the app, the team, and a feedback form for users.
```bash
selected = option_menu(
    menu_title="Main Menu", options=["Home", "Calm Space", "About & Feedback"]
)
```

## 5.2 Home Page
The Home section includes a form for users to submit their mood and stress level. Claude AI provides personalized suggestions based on their input.

Example code for the home page:

```bash
if selected == "Home":
    st.title("Welcome to the Anxiety Relief Platform")
    if st.button('Start Guided Breathing'):
        st.balloons()
        st.write("Inhale deeply... Exhale slowly... Repeat.")
```
        
## 5.3 Calm Space
In the Calm Space section, users can choose activities like meditation, yoga, and journaling, and receive instructions.

```bash
if selected == "Calm Space":
    st.header("Calm Space: Select Your Activity")
    selected_activity = st.selectbox(
        "Choose a relaxation activity", ["Meditation", "Yoga", "Breathing"]
    )
```
    
## 5.4 Data Visualization
Users can view data on the effectiveness of various anxiety-reducing activities through a bar chart created using Plotly.

```bash
data = {
    'Activity': ['Meditation', 'Yoga', 'Breathing', 'Journaling', 'Music'],
    'Calmness_Level': [85, 78, 90, 75, 88]
}
df = pd.DataFrame(data)
fig = px.bar(df, x='Activity', y='Calmness_Level', title="Calmness Levels by Activity")
st.plotly_chart(fig)
```

## 6. Custom Styling

The app uses custom CSS for an enhanced user experience, such as animated backgrounds and styled buttons.

```bash
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(90deg, #f3ec78, #af4261);
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
```
    
## 7. How to Contribute

To contribute:

Fork the repository.
Create a new branch for your feature.
Make your changes and ensure they pass tests.
Submit a pull request with a detailed explanation of your changes.

## 8. License

This project is licensed under the GPU License [LICENSE](LICENSE.MD).

## 9. Acknowledgments

Special thanks to the GSSoC Team and all the contributors who helped develop this project.
