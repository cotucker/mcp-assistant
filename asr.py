import speech_recognition as sr

def asr():
    while True:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio_text = r.listen(source)
                try:
                    print(r.recognize_google(audio_text))
                except:
                    print("Sorry, I did not get that")

        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asr()
