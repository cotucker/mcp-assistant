import speech_recognition as sr
from pynput.keyboard import Key, Controller

keyboard = Controller()

def asr():
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)  
                audio_text = r.listen(source, phrase_time_limit=2)
                try:
                    text = r.recognize_google(audio_text)

                    print(text)
                    return text
                except:
                    print("Sory, I did not get that")

        except Exception as e:
            return f"Exception: {e}"

if __name__ == "__main__":
    print(asr())
