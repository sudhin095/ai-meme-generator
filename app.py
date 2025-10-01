import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configure Gemini API key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Streamlit app ---
st.title("👻 Spector – An AI Meme Creator")

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

# --- Input from user ---
topic = st.text_input("Enter a concept/topic for a smart Indian-style meme:")

# --- Zoom slider ---
zoom_factor = st.slider("Zoom In / Out", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# --- Session state to preserve meme and caption ---
if "generated_meme" not in st.session_state:
    st.session_state.generated_meme = None
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None

# --- Generate New Meme Button ---
generate_new = st.button("Generate New Image")

# --- Generate meme if needed ---
if topic and (st.session_state.generated_meme is None or generate_new):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # --- Smarter, concept-aware prompt ---
        prompt = (
            f"Understand the concept '{topic}' and generate 5 short, punchy, funny meme captions. "
            "Make them simple, relatable to Indian culture, and include emojis if relevant. "
            "Do not number the captions. Output captions separated by new lines."
        )

        response = model.generate_content(prompt)

        # --- Clean captions ---
        captions = [c.strip() for c in response.text.strip().split("\n") if c.strip()]
        if not captions:
            captions = ["Hmm, couldn't think of a meme 😅", "This one is tricky! 🤔"]

        meme_text = random.choice(captions)  # pick one caption randomly

        # --- Pick a random meme image ---
        img_url = random.choice(meme_images)
        img = Image.open(BytesIO(requests.get(img_url).content))

        # --- Add space above image for caption ---
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 150), "white")
        draw = ImageDraw.Draw(new_img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)  # bigger font
        except:
            font = ImageFont.load_default()

        # --- Center the text above the image ---
        bbox = draw.textbbox((0, 0), meme_text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) / 2
        y = 30
        draw.text((x, y), meme_text, font=font, fill="black")

        # Paste original image below the text
        new_img.paste(img, (0, 150))

        # --- Save in session state to preserve meme on zoom ---
        st.session_state.generated_meme = new_img
        st.session_state.generated_text = meme_text

    except Exception as e:
        st.error(f"Error generating meme: {e}")

# --- Display meme with zoom ---
if st.session_state.generated_meme:
    display_width = int(st.session_state.generated_meme.width * zoom_factor)
    st.image(st.session_state.generated_meme, caption="Your AI Meme!", width=display_width)
