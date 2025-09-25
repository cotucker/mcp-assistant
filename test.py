import threading
import time
import wave
from piper import PiperVoice
import simpleaudio as sa
import numpy as np

# Загрузка голоса
voice = PiperVoice.load("audio\\en_US-hfc_female-medium.onnx", use_cuda=True)

# Глобальная переменная для хранения объекта воспроизведения
play_obj = None
play_lock = threading.Lock()

def synthesize_and_play(text: str):
    global play_obj
    # Синтез в WAV
    with wave.open("audio\\output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    # Загрузка аудио через simpleaudio
    wave_read = sa.WaveObject.from_wave_file("audio\\output.wav")
    
    with play_lock:
        play_obj = wave_read.play()

    # Ждём окончания воспроизведения (если не прервано)
    try:
        if play_obj.is_playing():
            play_obj.wait_done()
    except:
        pass  # Игнорируем, если прервано

def stop_playback():
    global play_obj
    with play_lock:
        if play_obj is not None and play_obj.is_playing():
            play_obj.stop()
            print("Воспроизведение остановлено.")
        else:
            print("Нечего останавливать.")

# Запуск воспроизведения в потоке
text_to_say = 'Hello, world! ' * 10
worker = threading.Thread(target=synthesize_and_play, args=(text_to_say,))
worker.start()

# Пример: остановить через 2 секунды
time.sleep(3)
stop_playback()

# Дождитесь завершения потока (опционально)
worker.join()