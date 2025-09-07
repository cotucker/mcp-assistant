from deepgram import SpeakOptions, DeepgramClient
import os
from dotenv import load_dotenv

load_dotenv()

deepgram = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))

# Configure speech options
options = SpeakOptions(model="aura-2-helena-en")

# Convert text to speech and save to file
response = deepgram.speak.rest.v("1").save(
    "output.mp3",
    {"text": """
Hi pretty boy
    """},
    options
)