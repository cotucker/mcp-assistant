from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import logging

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
logging.basicConfig(level=logging.INFO)
logging.info(f"GEMINI_API_KEY: {GEMINI_API_KEY}")

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Explain how AI works in a few words",
)
print(response)