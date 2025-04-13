# gemini_helper.py

import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def generate_summary(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"
