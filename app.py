import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Page styling ---
st.set_page_config(page_title="Spector – AI Meme Creator", layout="centered")

st.markdown("""
    <style>
        .main-title {
            font-size: 48px !important;
            text-align: center;
            font-weight: 800;
            color: #ffffff;
            padding: 15px;
            background: linear-gradient(90deg, #3c1053, #ad5389);
            border-radius: 15px;
            margin-bottom: 20px;
        }

        .input-box {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .zoom-box {
            background: #f8f8f8;
            padding: 18px;
            border-radius: 12px;
            box-shadow: inset 0px 0px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .generate-btn button {
            background: linear-gradient(90deg, #6a11cb, #2575fc) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }

        .meme-title {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Title ---
st.markdown("<div class='main-title'>👻 Spector – An AI Meme Creator</div>", unsafe_allow_html=True)

# Meme templates
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",
    "https://i.imgflip.com/1otk96.jpg",
    "https://i.imgflip.com/26am.jpg",
    "https://i.imgflip.com/1ur9b0.jpg",
    "https://i.imgflip.com/3si4.jpg",
    "https://i.imgflip.com/1bij.jpg",
    "https://i.imgflip.com/2fm6x.jpg",
    "https://i.imgflip.com/4t0m5.jpg",
    "https://i.pinimg.com/originals/your-jethalal-image.jpg",
    "https://i.imgflip.com/4t0m5.jpg",
    "https://i.imgflip.com/4t0m5.jpg",
]

# --- Input Section ---
with st.container():
    st.markdown("<div class='input-box'>", unsafe_allow_html=True)
    topic = st.text_input("🎯 Enter a concept/topic for a smart Indian-style meme:")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Zoom Section ---
with st.container():
    st.markdown("<div class='zoom-box'>", unsafe_allow_html=True)
    zoom_factor = st.slider("🔍 Zoom In / Out", 
                            min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Session State ---
if "generated_meme" not in st.session_state:
    st.session_state.generated_meme = None
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None

# Generate Button
st.markdown("<div class='generate-btn'>", unsafe_allow_html=True)
generate_new = st.button("✨ Generate New Image")
st.markdown("</div>", unsafe_allow_html=True)

# --- Meme Generation ---
if topic and (st.session_state.generated_meme is None or generate_new):
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

        W, H = img.size
        new_img = Image.new("RGB", (W, H + 150), "white")
        draw = ImageDraw.Draw(new_img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), meme_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (W - text_width) / 2
        y = 30

        draw.text((x, y), meme_text, font=font, fill="black")
        new_img.paste(img, (0, 150))

        st.session_state.generated_meme = new_img
        st.session_state.generated_text = meme_text

    except Exception as e:
        st.error(f"Error generating meme: {e}")

# --- Display Meme ---
if st.session_state.generated_meme:
    st.markdown("<div class='meme-title'>🖼️ Your Generated Meme</div>", unsafe_allow_html=True)
    display_width = int(st.session_state.generated_meme.width * zoom_factor)
    st.image(st.session_state.generated_meme, width=display_width)
