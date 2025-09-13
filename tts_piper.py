import wave
from piper import PiperVoice
from pydub import AudioSegment
from pydub.playback import play

voice = PiperVoice.load("audio\en_US-hfc_female-medium.onnx", use_cuda=True)

def tts_piper(text: str):
    with wave.open("audio\output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    sound = AudioSegment.from_wav("audio\output.wav")
    play(sound)

if __name__ == '__main__':
    tts_piper('Hello, world!')
