from deepgram import SpeakOptions, DeepgramClient
import os
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()
deepgram = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))
options = SpeakOptions(model="aura-2-helena-en")

def tts_deepgram(text: str):
    deepgram.speak.rest.v("1").save(
        "audio\output.mp3",
        {"text": text},
        options
    )
    sound = AudioSegment.from_mp3('audio\output.mp3')
    play(sound)


if __name__ == '__main__':
    tts_deepgram('Hello, world!')

