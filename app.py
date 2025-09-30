import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 AI Meme Generator with Zoom")

# Meme templates
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",       # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg",    # Change My Mind
    "https://i.imgflip.com/26am.jpg",      # Distracted Boyfriend
    "https://i.imgflip.com/1ur9b0.jpg",    # Drake Hotline Bling
    "https://i.imgflip.com/3si4.jpg",      # Futurama Fry
]

# Input topic
topic = st.text_input("Enter a concept/topic for a smart Indian-style meme:")

# Zoom slider (display size)
zoom_factor = st.slider("Zoom In / Out", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

if topic:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # Generate captions
        prompt = (
            f"Understand the concept '{topic}' and generate 3 short, punchy, funny meme captions. "
            "Keep it very simple, relatable to Indian culture, under 12 words each. "
            "Include emojis if relevant. Output captions separated by new lines."
        )
        response = model.generate_content(prompt)
        captions = response.text.strip().split("\n")
        meme_text = random.choice(captions)

        # Pick a random meme image
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # Add text above the image
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 150), "white")
        draw = ImageDraw.Draw(new_img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)  # Bigger font
        except:
            font = ImageFont.load_default()

        # Center the text
        bbox = draw.textbbox((0, 0), meme_text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) / 2
        y = 20
        draw.text((x, y), meme_text, font=font, fill="black")

        # Paste original image below the text
        new_img.paste(img, (0, 150))

        # Display image with zoom (via width scaling)
        display_width = int(new_img.width * zoom_factor)
        st.image(new_img, caption="Your AI Meme!", width=display_width)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
