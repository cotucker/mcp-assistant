import whisper
import torch

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

print(device)


model = whisper.load_model("tiny", in_memory=True)
result = model.transcribe("audio\output0.mp3")
print(result["text"])





