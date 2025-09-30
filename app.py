import streamlit as st
import google.generativeai as genai
import random

# Load Gemini API key securely from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Set up Streamlit app
st.title("🤖 AI Meme Generator for Learning")
st.write("Enter a concept and I'll turn it into a meme!")

# Meme templates (can add more URLs or local images)
meme_templates = [
    "https://i.imgflip.com/30b1gx.jpg",  # Drake Hotline Bling
    "https://i.imgflip.com/1bij.jpg",    # Distracted Boyfriend
    "https://i.imgflip.com/26am.jpg",    # Grumpy Cat
    "https://i.imgflip.com/9ehk.jpg",    # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg"   # Change My Mind
]

# Input from user
concept = st.text_input("✨ Enter a topic/concept to make a meme:")

if concept:
    try:
        # Generate meme caption using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(f"Create a short, funny meme caption about: {concept}")
        caption = response.text.strip()

        # Pick a random meme template
        template = random.choice(meme_templates)

        st.image(template, caption=caption)
        st.success("✅ Meme generated!")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
