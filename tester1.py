import speech_recognition as sr
from gtts import gTTS
import os
import requests
from bardapi import Bard
import time
import re

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

res = requests.get("http://192.168.1.36:5001/api")
data = res.json()
msg = data['msg']

def transcribe_mic(msg):
    while True:
        try:
            with mic as source:
                print("Adjusting for ambient noise...")
                recog.adjust_for_ambient_noise(source, duration=1)
                print("Listening for speech...")
                start_time = time.time()
                audio = recog.listen(source, timeout=3)
                text = recog.recognize_google(audio,language='th-TH')
                end_time = time.time()
                time_taken = (end_time - start_time)*1000
                print(f'speech to text  :{time_taken:2f} ms')
                print(text)

                bard = Bard(token = msg)
                start_time = time.time()
                result=bard.get_answer(text)['content']
                cln = re.sub(r'\([^)]*\)|\*|\:|\ๆ','',result)
                end_time =  time.time()
                time_taken = (end_time - start_time)*1000
                print(f'Bard API :{time_taken:2f} ms')
                print(cln)

                start_time = time.time()
                audio = bard.speech(cln)
                with open('test1.ogg','wb') as f:
                    f.write(bytes(audio['audio']))
                end_time = time.time()
                os.system('cvlc --play-and-exit test1.ogg')
                time_taken = (end_time - start_time)*1000
                print(f'text to speech :{time_taken:2f} ms')

        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for audio source...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    transcribe_mic(msg)

if __name__ == "__main__":
    main()
