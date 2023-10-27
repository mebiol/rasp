import pyaudio
import speech_recognition as sr

import browser_cookie3
from bardapi import Bard    

from gtts import gTTS 
import re
import os

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()

# Define the URL and get the browser cookie
url = 'https://bard.google.com/'
cj = browser_cookie3.firefox()
secure_1psid_cookie = None

for cookie in cj:
    if cookie.name == '__Secure-1PSID':
        secure_1psid_cookie = cookie.value
        break

while True:
    with mic as source:
        print("Listening for speech...")
        audio = recog.listen(source)
    try:
        text = recog.recognize_google(audio, language='th-TH')
        bard = Bard(token=secure_1psid_cookie)
        result = bard.get_answer(text)['content']
        cleaned_text = re.sub(r'\([^)]*\)|\*|\:|\ๆ', '', result)
        print(cleaned_text)
        sound = gTTS(text=cleaned_text)
        sound.save('exam.mp3')
        os.system('cvlc --play-and-exit exam.mp3')
    except sr.WaitTimeoutError:
        print("Recognition timed out")
    except Exception as e:
        print(f"An error occurred: {str(e)}")