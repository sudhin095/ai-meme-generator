import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import os
import google.generativeai as genai

# Load Gemini API key securely from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Set up Streamlit app
st.title("🤖 AI Meme Generator for Learning")
st.write("Enter a concept, and I'll generate a meme caption for you!")

concept = st.text_input("Enter a concept:")

if st.button("Generate Meme"):
    if concept:
        # Generate meme caption using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Create a short funny meme caption about: {concept}")
        caption = response.text.strip()

        # Pick a random meme template
        templates = ["drake.jpg", "pikachu.png", "distracted.jpg"]
        template = random.choice(templates)

        img_path = os.path.join("templates", template)
        if not os.path.exists(img_path):
            st.error(f"Template {template} not found! Make sure it's uploaded.")
        else:
            img = Image.open(img_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()

            # Add caption to meme
            textwidth, textheight = draw.textsize(caption, font)
            width, height = img.size
            x = (width - textwidth) / 2
            y = height - textheight - 20
            draw.text((x, y), caption, font=font, fill="white")

            # Display result
            st.image(img, caption=caption)
    else:
        st.warning("Please enter a concept.")

