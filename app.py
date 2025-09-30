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
        # --- Initialize a Gemini model ---
        model = genai.GenerativeModel("gemini-2.5-flash-lite")  # text generation model

        # --- Improved prompt for clearer captions ---
        prompt = f"""
        Generate a short, witty, and funny meme caption about "{concept}".
        Make it instantly understandable, punchy, and suitable for a meme image.
        Keep it under 15 words and limit to 1-2 lines.
        Examples:
        - "One does not simply ignore homework!"
        - "I don't always code, but when I do, I debug forever."
        Write a new caption similar in style.
        """

        # --- Generate meme caption ---
        response = model.generate_content(prompt)
        meme_text = response.text.strip()

        # --- Pick a random meme image ---
        meme_image_url = random.choice(meme_images)
        img_data = requests.get(meme_image_url).content
        img = Image.open(BytesIO(img_data))

        # --- Draw caption on image ---
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        # --- Wrap text manually ---
        max_chars_per_line = 30
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

        # --- Draw each line centered using textbbox ---
        W, H = img.size
        total_text_height = 0
        line_heights = []

        # Calculate total height
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
            total_text_height += h + 5  # spacing

        y_text = H - total_text_height - 20  # start above bottom

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (W - w) / 2
            draw.text(
                (x, y_text),
                line,
                font=font,
                fill="white",
                stroke_fill="black",
                stroke_width=2
            )
            y_text += h + 5

        # --- Show final meme ---
        st.image(img, caption="✨ Your AI-Generated Meme", use_column_width=True)

    except Exception as e:
        st.error(f"Error generating meme: {e}")
