import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Streamlit app ---
st.title("🤖 AI Meme Generator")

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
    "https://i.imgflip.com/30b1gx.jpg",    # Gru’s Plan
    "https://i.pinimg.com/originals/your-jethalal-image.jpg",  # Jethalal meme (replace with direct image URL)
    "https://i.imgflip.com/4t0m5.jpg",     # Monkey Puppet meme (replace with direct image URL)
    "https://i.imgflip.com/4t0m5.jpg"      # Frog meme (replace with direct image URL)
]

# Input from user
topic = st.text_input("Enter a topic/concept for a funny meme:")

if topic:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # --- Simple witty meme prompt ---
        prompt = (
            f"Make 3 very simple, funny captions about '{topic}'. "
            "Keep it under 10 words and easy to understand."
        )

        response = model.generate_content(prompt)
        meme_text = response.text.strip().split("\n")[0]

        # --- Pick a random meme image ---
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # --- Prepare font ---
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        # --- Add space above image ---
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 100), "white")
        draw = ImageDraw.Draw(new_img)

        # --- Place text above the image ---
        bbox = draw.textbbox((0, 0), meme_text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) / 2
        y = 20
        draw.text((x, y), meme_text, font=font, fill="black")

        new_img.paste(img, (0, 100))

        st.image(new_img, caption="Your AI Meme!", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
