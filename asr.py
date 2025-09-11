import speech_recognition as sr
from pynput.keyboard import Key, Controller

keyboard = Controller()

def asr():
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio_text = r.listen(source)
                try:
                    print(r.recognize_google(audio_text))
                    keyboard.press(Key.enter)
                    return r.recognize_google(audio_text)
                except:
                    print("Sorry, I did not get that")

        except Exception as e:
            return f"Exception: {e}"

if __name__ == "__main__":
    print(asr())
