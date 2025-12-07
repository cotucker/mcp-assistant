import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='ctranslate2')

from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(device="cpu", model="tiny.en")

    while True:
        recorder.text(process_text)
