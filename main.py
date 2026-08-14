
import io
import time
from gtts import gTTS

# 1. Read the contents of your text file
# Replace 'your_file.txt' with the actual path to your file
try:
    with open("seed_of_destiny_14_8_2026_8919.txt", "r", encoding="utf-8") as file:
        text_to_read = file.read()
except FileNotFoundError:
    print("Error: The file 'your_file.txt' was not found.")
    print("Falling back to placeholder text for this run...")
    text_to_read = "Please create a text file named your file dot txt to read your own content."

# 2. Check if the file is empty to avoid gTTS errors
if not text_to_read.strip():
    text_to_read = "The text file is empty."

# 3. Initialize the byte stream buffer and write the TTS data

tts = gTTS(text=text_to_read, lang="ha")
tts.save("voice.mp3")


