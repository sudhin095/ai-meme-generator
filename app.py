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

# Meme image templates (more popular memes added)
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",       # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg",    # Change My Mind
    "https://i.imgflip.com/26am.jpg",      # Distracted Boyfriend
    "https://i.imgflip.com/1ur9b0.jpg",    # Drake Hotline Bling
    "https://i.imgflip.com/3si4.jpg",      # Futurama Fry
    "https://i.imgflip.com/1bij.jpg",      # Leonardo DiCaprio Cheers
    "https://i.imgflip.com/2fm6x.jpg",     # Success Kid
    "https://i.imgflip.com/9ehy.jpg",      # Batman Slapping Robin
    "https://i.imgflip.com/4t0m5.jpg",     # Running Away Balloon
    "https://i.imgflip.com/30b1gx.jpg"     # Gru’s Plan
]

# Input from user
concept = st.text_input("✨ Enter a topic/concept to make a meme:")

if concept:
    try:
        # --- Initialize Gemini model ---
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        # --- Improved prompt for clearer captions ---
        prompt = f"""
        Generate a short, witty, and funny meme caption about "{concept}".
        Make it instantly understandable, punchy, and suitable for a meme image.
        Keep it under 15 words and limit to 1-2 lines.
        """

        # --- Generate meme caption ---
        response = model.generate_content(prompt)
        meme_text = response.text.strip()

        # --- Pick a random meme image ---
        meme_image_url = random.choice(meme_images)
        img_data = requests.get(meme_image_url).content
        img = Image.open(BytesIO(img_data))

        # --- Set up font (bigger font) ---
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 70)  # bigger font
        except:
            font = ImageFont.load_default()

        # --- Wrap text manually ---
        max_chars_per_line = 25
        words = meme_text.split()
        lines = []
        line = ""
        for word in words:
            if len(line + " " + word) <= max_chars_per_line:
                line += " " + word
            else:
                lines.append(line.strip())
                line = word
        lines.append(line.strip())

        # --- Create new canvas with extra space for text below ---
        W, H = img.size
        extra_height = (len(lines) * 80) + 40  # extra room for bigger text
        new_img = Image.new("RGB", (W, H + extra_height), "white")
        new_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(new_img)

        # --- Draw text below the image ---
        y_text = H + 20
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = (W - w) / 2
            draw.text(
                (x, y_text),
                line,
                font=font,
                fill="black"
            )
            y_text += bbox[3] - bbox[1] + 20  # spacing

        # --- Show final meme ---
        st.image(new_img, caption="✨ Your AI-Generated Meme", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
