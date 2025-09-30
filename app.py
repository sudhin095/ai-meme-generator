import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Streamlit app setup ---
st.title("🤖 AI Meme Generator for Learning")

# Meme image templates
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",    # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg"   # Change My Mind
]

# Input from user
concept = st.text_input("✨ Enter a topic/concept to make a meme:")

if concept:
    try:
        # --- Pick a valid Gemini model for text generation ---
        model_to_use = "gemini-1.5-t"
        st.info(f"Using model: {model_to_use}")

        # --- Generate meme caption ---
        response = genai.generate_content(
            model=model_to_use,
            prompt=f"Create a short funny meme caption about: {concept}"
        )
        meme_text = response.result[0].content[0].text.strip()

        # --- Pick a random meme image ---
        meme_image_url = random.choice(meme_images)
        img_data = requests.get(meme_image_url).content
        img = Image.open(BytesIO(img_data))

        # --- Draw caption on image ---
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # Windows/Streamlit Cloud
        except:
            font = ImageFont.load_default()  # fallback

        # Wrap text (simple split by length)
        max_width = 30
        lines = []
        words = meme_text.split()
        line = ""
        for word in words:
            if len(line + " " + word) <= max_width:
                line += " " + word
            else:
                lines.append(line.strip())
                line = word
        lines.append(line.strip())

        # Draw each line centered
        W, H = img.size
        y_text = H - (len(lines) * 50) - 20  # bottom padding
        for line in lines:
            w, h = draw.textsize(line, font=font)
            x = (W - w) / 2
            draw.text((x, y_text), line, font=font, fill="white", stroke_fill="black", stroke_width=2)
            y_text += h + 5

        # --- Show final meme ---
        st.image(img, caption="✨ Your AI-Generated Meme", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
