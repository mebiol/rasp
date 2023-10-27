import speech_recognition as sr
from gtts import gTTS
import requests
from bardapi import Bard
import time
import os
import re

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

res = requests.get("http://192.168.1.42:5001/api")
data = res.json()
msg = data['msg']

def transcribe_mic(msg): 
    #count = 0  # Initialize the count variable 
    while True:
        try:
            with mic as source:
                print("Adjusting for ambient noise...")
                recog.adjust_for_ambient_noise(source, duration=1)
                print("Listening for speech...")
                start_time = time.time()
                audio = recog.listen(source, timeout=2)
                text = recog.recognize_google(audio, language='th-TH')
                end_time = time.time()
                time_taken = (end_time - start_time) * 1000
                print(f'speech to text: {time_taken:.2f} ms')
                print(text) 
                bard = Bard(token=msg)
                start_time = time.time()

                # Check if it's the first time, if so, include the prefix
                #if count == 0:
                result = bard.get_answer(f"You are a kind female doctor names Tanya. Respond to the following: {text} Explain the most important way you can help me. The answer should be no more than 20 words.")['content'] 
#                result = bard.get_answer(f"Explain the most important way you can help me. The answer should be no more than 20 words,in Thai.Now, as Dr.Tanya,I would respond in Thai: {text}")['content']
                cln = re.sub(r'\([^)]*\)|\*|\:','',result)
                end_time = time.time()
                time_taken = (end_time - start_time) * 1000
                print(f'Bard API: {time_taken:.2f} ms')
                print(cln)

                start_time = time.time()
                sound = gTTS(text=cln, lang=lan, slow=False)
                sound.save('test.mp3')
                os.system('cvlc --play-and-exit test.mp3')
                time_taken = (end_time - start_time)*1000
                print(f'text to speech :{time_taken:2f} ms')

        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for an audio source...")
        except requests.ConnectionError as e:
            print(f"Connection error occurred:{e}")
            msg=None
        except Exception as e:
            print(f"An error occurred: {str(e)}")



def main():
    transcribe_mic(msg)

if __name__ == "__main__":
    main()
