import streamlit as st
import google.generativeai as genai
import random

# --- Configure Gemini API key ---
# Make sure you have GEMINI_API_KEY in Streamlit secrets
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
        # --- List all available models and convert generator to list ---
        models = list(genai.list_models())
        valid_models = [m.name for m in models if "generateContent" in m.supported_methods]

        if not valid_models:
            st.error("No models supporting generateContent are available.")
        else:
            model_to_use = valid_models[0]  # Pick the first valid model
            st.info(f"Using model: {model_to_use}")

            # --- Generate meme caption ---
            response = genai.generate_content(
                model=model_to_use,
                prompt=f"Create a short funny meme caption about: {concept}"
            )
            meme_text = response.result[0].content[0].text.strip()

            # --- Pick a random meme image ---
            meme_image = random.choice(meme_images)

            # --- Display meme ---
            st.image(meme_image, use_column_width=True)
            st.markdown(f"**Meme Caption:** {meme_text}")

    except Exception as e:
        st.error(f"Error generating meme: {e}")
