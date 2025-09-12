import speech_recognition as sr
from pydub import AudioSegment
import io # Нужен для работы с байтами в памяти

# Инициализируем распознаватель
r = sr.Recognizer()

# Имя выходного файла
output_mp3_file = "recorded_audio.mp3"

# Используем микрофон как источник
with sr.Microphone() as source:
    print("Настрока на фоновый шум... Пожалуйста, помолчите.")
    # Настраиваемся на фоновый шум для лучшего распознавания
    r.adjust_for_ambient_noise(source, duration=1) 
    
    print("Говорите!")
    # Слушаем речь и сохраняем ее в объект AudioData
    audio_text = r.listen(source)
    print("Время вышло, спасибо!")

# --- Блок сохранения в MP3 ---
try:
    print("Сохранение аудио в MP3 файл...")
    # Получаем сырые данные в формате WAV
    wav_data = audio_text.get_wav_data()
    
    # Создаем аудиосегмент из WAV-данных в памяти
    # io.BytesIO позволяет pydub читать байтовую строку как файл
    audio_segment = AudioSegment.from_file(io.BytesIO(wav_data), format="wav")
    
    # Экспортируем аудиосегмент в формат MP3
    audio_segment.export(output_mp3_file, format="mp3")
    
    print(f"Файл успешно сохранен как {output_mp3_file}")

except Exception as e:
    print(f"Ошибка при сохранении файла: {e}")


# --- Блок распознавания речи (остается без изменений) ---
try:
    # Используем Google Speech Recognition для распознавания
    print("Распознавание текста...")
    text = r.recognize_google(audio_text, language="ru-RU") # Укажите язык для лучшего результата
    print("Текст: " + text)
except sr.UnknownValueError:
    print("Извините, не удалось распознать речь")
except sr.RequestError as e:
    print(f"Не удалось запросить результаты у сервиса Google Speech Recognition; {e}")