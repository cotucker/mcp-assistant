import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Define the text and voice characteristics
tts_payload = {
    "text": "Hi, I am a robot.",
    "voice_id": 20305,    # Replace with your chosen voice ID
    "language": 1,      # English
    "gender": 1,        # Male voice
    "age": 30           # Adult voice characteristic
}

# Set up your API credentials
headers = {
    "x-api-key": os.getenv("X_API_KEY"),  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Step 1: Submit your text-to-speech request
response = requests.post(
    "https://client.camb.ai/apis/tts",
    json=tts_payload,
    headers=headers
)

# Check if the request was successful
response.raise_for_status()
task_data = response.json()
task_id = task_data["task_id"]
print(f"Speech task created! Task ID: {task_id}")

# Step 2: Check progress until complete
while True:
    status_response = requests.get(
        f"https://client.camb.ai/apis/tts/{task_id}",
        headers=headers
    )
    status_data = status_response.json()
    status = status_data["status"]
    print(f"Status: {status}")

    if status == "SUCCESS":
        run_id = status_data["run_id"]
        break
    elif status == "FAILED":
        print("Task failed!")
        break

    # Wait before checking again
    time.sleep(2)

# Step 3: Download your audio file
if status == "SUCCESS":
    print(f"Speech ready! Run ID: {run_id}")
    audio_response = requests.get(
        f"https://client.camb.ai/apis/tts-result/{run_id}",
        headers=headers,
        stream=True
    )

    # Save the audio file
    with open("speech.wav", "wb") as audio_file:
        for chunk in audio_response.iter_content(chunk_size=1024):
            if chunk:
                audio_file.write(chunk)

    print("✨ Generated speech was saved as 'speech.wav'")
import requests
import time

# Define the text and voice characteristics
tts_payload = {
    "text": "Hi, I am a robot.",
    "voice_id": 20305,    # Replace with your chosen voice ID
    "language": 1,      # English
    "gender": 1,        # Male voice
    "age": 30           # Adult voice characteristic
}

# Set up your API credentials
headers = {
    "x-api-key": "76a02c29-59c6-45da-beca-52b73d537d8a",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Step 1: Submit your text-to-speech request
response = requests.post(
    "https://client.camb.ai/apis/tts",
    json=tts_payload,
    headers=headers
)

# Check if the request was successful
response.raise_for_status()
task_data = response.json()
task_id = task_data["task_id"]
print(f"Speech task created! Task ID: {task_id}")

# Step 2: Check progress until complete
while True:
    status_response = requests.get(
        f"https://client.camb.ai/apis/tts/{task_id}",
        headers=headers
    )
    status_data = status_response.json()
    status = status_data["status"]
    print(f"Status: {status}")

    if status == "SUCCESS":
        run_id = status_data["run_id"]
        break
    elif status == "FAILED":
        print("Task failed!")
        break

    # Wait before checking again
    time.sleep(2)

# Step 3: Download your audio file
if status == "SUCCESS":
    print(f"Speech ready! Run ID: {run_id}")
    audio_response = requests.get(
        f"https://client.camb.ai/apis/tts-result/{run_id}",
        headers=headers,
        stream=True
    )

    # Save the audio file
    with open("speech.wav", "wb") as audio_file:
        for chunk in audio_response.iter_content(chunk_size=1024):
            if chunk:
                audio_file.write(chunk)

    print("✨ Generated speech was saved as 'speech.wav'")