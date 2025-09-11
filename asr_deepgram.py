# main.py (python example)

import os
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

# Path to the audio file
AUDIO_FILE = "audio\output.mp3"



def main():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source)
            print("Time over, thanks")
            # recoginze_() method will throw a request
            # error if the API is unreachable,
            # hence using exception handling
            
            try:
                # using google speech recognition
                print("Text: "+r.recognize_google(audio_text))
            except:
                print("Sorry, I did not get that")

        
        # # STEP 1 Create a Deepgram client using the API key
        # deepgram = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))

        # with open(AUDIO_FILE, "rb") as file:
        #     buffer_data = file.read()

        # payload: FileSource = {
        #     "buffer": buffer_data,
        # }

        # #STEP 2: Configure Deepgram options for audio analysis
        # options = PrerecordedOptions(
        #     model="nova-3",
        #     smart_format=True,
        # )

        # # STEP 3: Call the transcribe_file method with the text payload and options
        # response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        # # STEP 4: Print the response
        # print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
