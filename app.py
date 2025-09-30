import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 AI Meme Generator with Zoom (Persistent)")

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

# Input topic
topic = st.text_input("Enter a concept/topic for a smart Indian-style meme:")

# Zoom slider
zoom_factor = st.slider("Zoom In / Out", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# --- Function to generate meme ---
def generate_meme(topic):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        prompt = (
            f"Understand the concept '{topic}' and generate 5 short, punchy, funny meme captions. "
            "Make them simple, relatable to Indian culture, and include emojis if relevant. "
            "Do not number the captions. Output captions separated by new lines."
        )

        response = model.generate_content(prompt)
        captions = [c.strip() for c in response.text.strip().split("\n") if c.strip()]
        if not captions:
            captions = ["Hmm, couldn't think of a meme 😅", "This one is tricky! 🤔"]

        meme_text = random.choice(captions)
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # --- Add text above image ---
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 150), "white")
        draw = ImageDraw.Draw(new_img)

        try:
            font = ImageFont.truetype("arial.ttf", 140)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), meme_text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) / 2
        y = 30
        draw.text((x, y), meme_text, font=font, fill="black")

        new_img.paste(img, (0, 150))
        return new_img

    except Exception as e:
        st.error(f"Error generating meme: {e}")
        return None

# --- Generate meme only once per topic ---
if topic:
    if "meme_img" not in st.session_state or st.session_state.get("last_topic") != topic:
        st.session_state.meme_img = generate_meme(topic)
        st.session_state.last_topic = topic

    # Display with zoom
    if st.session_state.meme_img:
        display_width = int(st.session_state.meme_img.width * zoom_factor)
        st.image(st.session_state.meme_img, caption="Your AI Meme!", width=display_width)
