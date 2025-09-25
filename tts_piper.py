import wave, time, threading
import simpleaudio as sa
from piper import PiperVoice

voice = PiperVoice.load("audio\\en_US-hfc_female-medium.onnx", use_cuda=True)

play_obj = None
play_lock = threading.Lock()

def synthesize_and_play(text: str):
    global play_obj

    with wave.open("audio\\output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    wave_read = sa.WaveObject.from_wave_file("audio\\output.wav")
    
    with play_lock:
        play_obj = wave_read.play()

    try:
        if play_obj.is_playing():
            play_obj.wait_done()
    except:
        pass

def stop_playback():
    global play_obj
    with play_lock:
        if play_obj is not None and play_obj.is_playing():
            play_obj.stop()
            print("✨: ...")
        else:
            print("✨: I dont say anything")

def tts_piper(text: str):
    worker = threading.Thread(target=synthesize_and_play, args=(text,))
    worker.start()

if __name__ == '__main__':
    tts_piper('Hello, world!' * 10)
    time.sleep(3)
    stop_playback()
