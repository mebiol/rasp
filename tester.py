import speech_recognition as sr
from gtts import gTTS
import requests
from bardapi import Bard
import time
import os

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

res = requests.get("http://192.168.1.35:5001/api")
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
                audio = recog.listen(source, timeout=2)
                text = recog.recognize_google(audio, language='th-TH')
                end_time = time.time()
                time_taken = (end_time - start_time) * 1000
                print(f'speech to text: {time_taken:.2f} ms')
                print(text)

                bard = Bard(token=msg)
                start_time = time.time()
                result = bard.get_answer(f"ลองนึกภาพคุณเป็นหมออายุ 30 ปีผู้ใจดี เพศหญิง ตอบคำถามต่อไปนี้ให้สั้น 2 บรรทัด{text}")['content']
                cln = result.split('\n')
                clns = cln[0]
                end_time = time.time()
                time_taken = (end_time - start_time) * 1000
                print(f'Bard API: {time_taken:.2f} ms')
                print(clns)

                start_time = time.time()
                sound = gTTS(text=clns, lang=lan, slow=False)
                sound.save('test.mp3')
                os.system('cvlc --play-and-exit test.mp3')
                time_taken = (end_time - start_time)*1000
                print(f'text to speech :{time_taken:2f} ms')

        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for an audio source...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    transcribe_mic(msg)

if __name__ == "__main__":
    main()
