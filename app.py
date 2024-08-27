import os
import streamlit as st  # Streamlit library for building web applications
from dotenv import load_dotenv  # Load environment variables from .env file to use in the application
from streamlit_option_menu import option_menu  # Custom option menu for Streamlit applications to display icons with options
from PIL import Image  # Python Imaging Library to work with images 
import google.generativeai as genai  # Google Generative AI library for building AI models

from octoai.util import to_file
from octoai.client import OctoAI

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("api_key")
OCTOAI_TOKEN = os.getenv("OCTOAI_TOKEN")

# Initialize OctoAI client
client = OctoAI(api_key=OCTOAI_TOKEN)

# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)

# Load gemini-pro model
def gemini_pro():
    model = genai.GenerativeModel('gemini-pro')
    return model

# Load gemini vision model
def gemini_vision():
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    return model

# Get response from gemini pro vision model
def gemini_vision_response(model, prompt, image):
    response = model.generate_content([prompt, image])
    return response.text

# Get image from Stable Diffusion XL text-to-image generator
def sdxl_text_to_image(prompt):
    image_resp = client.image_gen.generate_sdxl(
        prompt=prompt
    )
    images = image_resp.images

    if images[0].removed_for_safety:
        return None
    ext = '.jpg'
    while os.path.isfile(prompt + ext):
        split = prompt.split()
        suffix = split[-1]
        i = 1
        if (suffix[0], suffix[-1]) == ('(', ')') and suffix[1:-1].isdigit():
            i += int(suffix[1:-1])
            prompt = ' '.join(split[:-1])
            prompt += f' ({i})'
        else:
            break
    file_name = prompt + ext
    to_file(images[0], file_name)
    return file_name

# Set page title and icon
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🧸",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "AI Assistant",
        ["ChatBot", "Image Captioning", "Text to Image"],
        menu_icon="robot",
        icons=["chat-dots-fill", "brush-fill", "image-fill"],
        default_index=0
    )

def roleForStreamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

if user_picked == 'ChatBot':
    model = gemini_pro()

    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = model.start_chat(history=[])

    st.title("🧑🏻‍💻Talk With Gemini")

    # Display the chat history
    for message in st.session_state.chat_history.history:
        with st.chat_message(roleForStreamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Get user input
    user_input = st.chat_input("Message TalkBot:")
    if user_input:
        st.chat_message("user").markdown(user_input)
        response = st.session_state.chat_history.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)

if user_picked == 'Image Captioning':
    model = gemini_vision()

    st.title("✒️Image Captioning")

    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if st.button("Generate Caption") and image:
        load_image = Image.open(image)

        colLeft, colRight = st.columns(2)

        with colLeft:
            st.image(load_image)

        # Generate caption without needing a prompt from the user
        caption_response = gemini_vision_response(model, "", load_image)

        with colRight:
            st.info(caption_response)


elif user_picked == 'Text to Image':
    

    st.title("🔮Text-to-Image Generation")

    model_choice = st.selectbox("Choose Image Generator:", ["Stable Diffusion XL"])

    user_prompt = st.text_input("Enter the prompt for image generation:")

    if st.button("Generate Image") and user_prompt:
        generated_image = sdxl_text_to_image(user_prompt)

        if generated_image:
            st.image(generated_image, caption=f"Generated by {model_choice}")
        else:
            st.error("Image generation failed.")
