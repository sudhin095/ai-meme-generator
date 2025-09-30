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

# --- Expanded meme templates ---
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",       # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg",    # Change My Mind
    "https://i.imgflip.com/26am.jpg",      # Distracted Boyfriend
    "https://i.imgflip.com/1ur9b0.jpg",    # Drake Hotline Bling
    "https://i.imgflip.com/3si4.jpg",      # Futurama Fry
    "https://i.imgflip.com/1bij.jpg",      # Leonardo DiCaprio Cheers
    "https://i.imgflip.com/2fm6x.jpg",     # Success Kid
    "https://i.imgflip.com/4t0m5.jpg",     # Running Away Balloon
    "https://i.pinimg.com/originals/21/5b/9f/215b9f09a6a045f849f6d944b60eb92f.jpg",  # Jethalal meme
    "https://i.imgflip.com/5c1.jpg",       # Monkey Puppet
    "https://i.imgflip.com/3si3.jpg",      # Frog meme
    "https://i.pinimg.com/originals/6b/2e/85/6b2e85d47c7c8f1e4a1c07c3e1b8d0e2.jpg",  # Indian student meme
    "https://i.pinimg.com/originals/8e/3a/77/8e3a77f6d5c0f3a02f2d7f7b6d5f0b4f.jpg",  # Indian reaction meme
    "https://i.imgflip.com/2hgfw.jpg",     # Drake Approving / Disapproving
]

# --- Input from user ---
topic = st.text_input("Enter a concept/topic for a smart Indian-style meme:")

# --- Zoom slider ---
zoom_factor = st.slider("Zoom In / Out", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# --- Session state to preserve the same meme ---
if "generated_meme" not in st.session_state:
    st.session_state.generated_meme = None
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None

if topic:
    try:
        if st.session_state.generated_meme is None:
            model = genai.GenerativeModel("gemini-2.5-flash-lite")

            # --- Smart prompt ---
            prompt = (
                f"Understand the concept '{topic}' and generate 5 short, punchy, funny meme captions. "
                "Make them simple, relatable to Indian culture, include emojis if relevant, and do not number them. "
                "Output captions separated by new lines."
            )

            response = model.generate_content(prompt)
            captions = [c.strip() for c in response.text.strip().split("\n") if c.strip()]
            if not captions:
                captions = ["Hmm, couldn't think of a meme 😅", "This one is tricky! 🤔"]

            meme_text = random.choice(captions)  # pick one caption randomly
            img_url = random.choice(meme_images)
            img = Image.open(BytesIO(requests.get(img_url).content))

            # --- Add text above image ---
            W, H = img.size
            new_img = Image.new("RGB", (W, H + 180), "white")
            draw = ImageDraw.Draw(new_img)

            try:
                font = ImageFont.truetype("arial.ttf", 140)  # Bigger font for readability
            except:
                font = ImageFont.load_default()

            # --- Center the text ---
            bbox = draw.textbbox((0, 0), meme_text, font=font)
            text_w = bbox[2] - bbox[0]
            x = (W - text_w) / 2
            y = 30
            draw.text((x, y), meme_text, font=font, fill="black")

            # Paste original meme below the text
            new_img.paste(img, (0, 180))

            # Save in session state
            st.session_state.generated_meme = new_img
            st.session_state.generated_text = meme_text

        # --- Display with zoom ---
        display_width = int(st.session_state.generated_meme.width * zoom_factor)
        st.image(st.session_state.generated_meme, caption="Your AI Meme!", width=display_width)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
