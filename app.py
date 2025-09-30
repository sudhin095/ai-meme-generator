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
    "https://i.pinimg.com/originals/your-jethalal-image.jpg",  # Jethalal meme
    "https://i.imgflip.com/4t0m5.jpg",     # Monkey Puppet
    "https://i.imgflip.com/4t0m5.jpg",     # Frog meme
]

# Input from user
topic = st.text_input("Enter a concept/topic for a smart Indian-style meme:")

if topic:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # --- Smart, concept-aware prompt ---
        prompt = (
            f"Understand the concept '{topic}' deeply and generate 3 witty, punchy, and culturally relatable Indian meme captions. "
            "Make them funny, under 12 words each, simple to read, and include relevant emojis if it enhances humor. "
            "The captions should clearly reflect the concept and be instantly understandable. Output captions separated by new lines."
        )

        response = model.generate_content(prompt)
        captions = response.text.strip().split("\n")
        meme_text = random.choice(captions)  # pick one caption randomly

        # --- Pick a random meme image ---
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # --- Prepare font dynamically ---
        draw = ImageDraw.Draw(img)
        max_font_size = 200  # Increased maximum font size
        min_font_size = 50
        font_size = max_font_size

        while True:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
                break
            bbox = draw.textbbox((0, 0), meme_text, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= img.width - 40 or font_size <= min_font_size:
                break
            font_size -= 5

        # --- Add space above image ---
        W, H = img.size
        new_img = Image.new("RGB", (W, H + font_size + 60), "white")
        draw = ImageDraw.Draw(new_img)

        # --- Place text above the image ---
        bbox = draw.textbbox((0, 0), meme_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (W - text_width) / 2
        y = 20
        draw.text((x, y), meme_text, font=font, fill="black")

        new_img.paste(img, (0, font_size + 60))

        st.image(new_img, caption="Your Smart AI Meme!", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
