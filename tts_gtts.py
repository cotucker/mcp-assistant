from gtts import gTTS
tts = gTTS("""
Current Weather for Minsk, Belarus:
Temperature: 23.1°C
Feels like: 24.9°C
Wind: 11.5 kph E
Humidity: 53%
Condition: Partly cloudy
Pressure: 1024.0 mb
""")
tts.save('hello.mp3')