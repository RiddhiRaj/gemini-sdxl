
# AI Assistant with Google Gemini and Stable Diffusion XL

This project is a Streamlit-based web application that leverages Google's Gemini AI models and Stable Diffusion XL for various AI functionalities including chatbot interaction, image captioning, and text-to-image generation.

## Features

- **ChatBot**: Interact with the Google Gemini-Pro model to have natural language conversations.
- **Image Captioning**: Automatically generate captions for uploaded images using the Gemini Vision model.
- **Text-to-Image**: Generate images based on text prompts using the Stable Diffusion XL model.

## Requirements

- Python 3.7+
- Streamlit
- Python Libraries:
  - `dotenv`
  - `streamlit_option_menu`
  - `PIL`
  - `google-generativeai`
  - `octoai`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RiddhiRaj/gemini.git
   cd gemini
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory of your project and add your API keys:

   ```
   api_key=your_google_api_key
   OCTOAI_TOKEN=your_octoai_token
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Usage

### ChatBot

1. Select the "ChatBot" option from the sidebar.
2. Start chatting with the Google Gemini-Pro model.

### Image Captioning

1. Select the "Image Captioning" option from the sidebar.
2. Upload an image (jpg, png, jpeg).
3. Click on "Generate Caption" to automatically generate and display the caption.

### Text-to-Image

1. Select the "Text to Image" option from the sidebar.
2. Enter a prompt in the text input field.
3. Click "Generate Image" to create an image based on the provided prompt.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.