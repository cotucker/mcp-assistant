from deepgram import (
    SpeakWSOptions,
    SpeakWebSocketEvents,
    DeepgramClient
)
import os
from dotenv import load_dotenv

load_dotenv()


deepgram = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))

# Create websocket connection
connection = deepgram.speak.websocket.v("1")

# Handle audio data
@connection.on(SpeakWebSocketEvents.AudioData, on_audio_data)
async def on_audio_data(data: bytes):
    """Handle audio data received from the server."""
    print(f"Received audio data: {data}")
    # Save audio data to a file
    with open("output.wav", "ab") as f:
        f.write(data)

connection = deepgram.speak.websocket.v("1")

# Configure streaming options
options = SpeakWSOptions(
    model="aura-2-thalia-en",
    encoding="linear16",
    sample_rate=16000
)
 
# Start connection and send text
connection.start(options)
connection.send_text("Hello, this is a text to speech example.")
connection.flush()
connection.wait_for_complete()

# Close when done
connection.finish()