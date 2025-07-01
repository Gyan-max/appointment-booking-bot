import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_gemini_client():
    if not GEMINI_API_KEY:
        raise ValueError('GEMINI_API_KEY not set in environment')
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('models/gemini-1.5-flash-latest')

def generate_gemini_response(prompt: str) -> str:
    model = get_gemini_client()
    response = model.generate_content(prompt)
    return response.text

genai.configure(api_key=GEMINI_API_KEY)
print([m.name for m in genai.list_models()])
