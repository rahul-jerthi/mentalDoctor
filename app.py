import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API Key from env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure Gemini API Key (swap in yours, babe!)

# Function to analyze raw user input with Gemini
def analyze_depression(user_responses):
    prompt = f"""
    You are a clinical AI assistant assessing mental health with the PHQ-9 questionnaire.
    Analyze these raw user responses, assign PHQ-9 scores (0-3 per question: 0=Not at all, 1=Several days, 
    2=More than half the days, 3=Nearly every day), and determine depression severity.

    Responses:
    1. Little interest or pleasure in doing things? → {user_responses[0]}
    2. Feeling down, depressed, or hopeless? → {user_responses[1]}
    3. Trouble falling/staying asleep or sleeping too much? → {user_responses[2]}
    4. Feeling tired or having little energy? → {user_responses[3]}
    5. Poor appetite or overeating? → {user_responses[4]}
    6. Feeling bad about yourself or like a failure? → {user_responses[5]}
    7. Trouble concentrating? → {user_responses[6]}
    8. Moving/speaking slowly or feeling restless? → {user_responses[7]}
    9. Thoughts of self-harm? → {user_responses[8]}

    Provide:
    - **PHQ-9 Score** (sum of scores, 0-27)
    - **Severity Level** (Minimal: 0-4, Mild: 5-9, Moderate: 10-14, Moderately Severe: 15-19, Severe: 20-27)
    - **Short Analysis** (explain the score based on responses)
    - **Recommendation** (tailored advice)

    Response format:
    PHQ-9 Score: <score>  
    Severity Level: <Minimal/Mild/Moderate/Moderately Severe/Severe>  
    Analysis: <brief explanation>  
    Recommendation: <advice>
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI—clean, sexy, and interactive
st.set_page_config(page_title="Mind Glow", layout="centered", page_icon="✨")

# Eye-catching title
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: white;'>🌟 Mind Glow:</span>
        <span style='color: violet;'>Your Vibe Check 🌟</span>
    </h1>
""", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6b7280;'>Spill your feels, babe—I’ve got you! 💖</h3>", unsafe_allow_html=True)

# Instructions with flair
st.write("**How it works:** Type how you’re feeling below. Example vibes are there to spark you—keep it real, sexy!")

# PHQ-9 Questions with text_input and sample text
questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling/staying asleep or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself or like a failure?",
    "Trouble concentrating?",
    "Moving/speaking slowly or feeling restless?",
    "Thoughts of self-harm?"
]

placeholders = [
    "E.g., 'I don’t care about anything anymore.'",
    "E.g., 'I’ve been super down lately.'",
    "E.g., 'I barely sleep—nightmares suck.'",
    "E.g., 'I’m drained all the time.'",
    "E.g., 'I can’t stop eating junk.'",
    "E.g., 'I feel like a total loser.'",
    "E.g., 'My brain’s a mess—can’t focus.'",
    "E.g., 'I’m either sluggish or wired.'",
    "E.g., 'Sometimes I think about ending it.'"
]

user_responses = []
for i, (q, p) in enumerate(zip(questions, placeholders)):
    response = st.text_input(f"{i+1}. {q}", placeholder=p, key=f"q{i}")
    user_responses.append(response)


# Analyze Button—bold and clickable
if st.button("✨ Glow Me Up—Analyze Now! ✨", use_container_width=True):
    if all(response.strip() for response in user_responses):  # No empty fields, babe!
        with st.spinner("Reading your glow, cutie..."):
            result = analyze_depression(user_responses)
        st.markdown("<h2 style='color: #ff4b4b;'>🎉 Your Glow Report 🎉</h2>", unsafe_allow_html=True)
        
        # Split the result into lines and format with bold + spacing
        lines = result.split('\n')
        formatted_result = ""
        for line in lines:
            if line.strip():  # Skip empty lines
                key, value = line.split(':', 1)  # Split on first colon only
                formatted_result += f"<p style='font-size: 18px; margin: 10px 0; color: #000000;'><strong>{key.strip()}:</strong> {value.strip()}</p>"
        
        st.markdown(
            f"<div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px;'>{formatted_result}</div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Oops, sexy—fill in all the vibes so I can glow you up!")

# Footer—my flirty touch
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff69b4;'>💋 Crafted with love by your data darling—shine on, babe! 💋</p>", unsafe_allow_html=True)
