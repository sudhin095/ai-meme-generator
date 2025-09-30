import streamlit as st
from google.generativeai import Client
import random

# Initialize the Google Generative AI client
client = Client()

# List available models that support generateContent
available_models = client.list_models()
valid_models = [
    model.name for model in available_models.models
    if "generateContent" in model.supported_methods
]

if not valid_models:
    st.error("No models supporting generateContent are available.")
    st.stop()

# Pick the first valid model
model_to_use = valid_models[0]
st.info(f"Using model: {model_to_use}")

# Meme image templates
meme_images = [
    "https://i.imgflip.com/9ehk.jpg",    # One Does Not Simply
    "https://i.imgflip.com/1otk96.jpg"   # Change My Mind
]

# Input from user
concept = st.text_input("✨ Enter a topic/concept to make a meme:")

if concept:
    try:
        # Generate meme caption/text
        response = client.generate_content(
            model=model_to_use,
            prompt=f"Create a short funny meme caption about: {concept}"
        )
        meme_text = response.result[0].content[0].text.strip()

        # Pick a random meme image
        meme_image = random.choice(meme_images)

        # Display meme
        st.image(meme_image, use_column_width=True)
        st.markdown(f"**Meme Caption:** {meme_text}")

    except Exception as e:
        st.error(f"Error generating meme: {e}")
