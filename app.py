import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Streamlit app ---
st.title("🤣 Witty AI Meme Generator")

# Meme templates
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",       # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg",    # Change My Mind
    "https://i.imgflip.com/26am.jpg",      # Distracted Boyfriend
    "https://i.imgflip.com/1ur9b0.jpg",    # Drake Hotline Bling
    "https://i.imgflip.com/3si4.jpg",      # Futurama Fry
    "https://i.imgflip.com/1bij.jpg",      # Leonardo DiCaprio Cheers
    "https://i.imgflip.com/2fm6x.jpg",     # Success Kid
    "https://i.imgflip.com/4t0m5.jpg",     # Running Away Balloon
    "https://i.imgflip.com/30b1gx.jpg"     # Gru’s Plan
]

# Input from user
topic = st.text_input("Enter a topic/concept for a funny meme:")

if topic:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # --- Witty meme prompt ---
        prompt = (
            f"Make 3 short, witty, meme-style captions about '{topic}'. "
            "Use sarcasm, exaggeration, or wordplay. Keep each under 10 words."
        )

        response = model.generate_content(prompt)
        # Take the first line as the caption
        meme_text = response.text.strip().split("\n")[0]

        # --- Pick a random meme image ---
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # --- Prepare font ---
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 70)
        except:
            font = ImageFont.load_default()

        # --- Add extra space below image ---
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 100), "white")
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)

        # --- Centered text ---
        bbox = draw.textbbox((0, 0), meme_text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) / 2
        y = H + 20
        draw.text((x, y), meme_text, font=font, fill="black")

        st.image(new_img, caption="Your Witty AI Meme!", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
