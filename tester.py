import speech_recognition as sr
from gtts import gTTS
import os
import requests
from bardapi import Bard
import time
import re
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

res = requests.get("http://192.168.1.44:5001/api")
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
                text = recog.recognize_google(audio,language='th-TH')
                end_time = time.time()
                time_taken = (end_time - start_time)*1000
                print(f'speech to text  :{time_taken:2f} ms')
                print(text)

                bard = Bard(token = msg)
                start_time = time.time()
                result=bard.get_answer(f"{text}โดยให้ Bard เปลี่ยนบทบาทเป็นคุณหมอหญิงที่มีอายุ 30ปี ใจดี อายุกรรมและตอบแบบสรุปให้สั้นมากที่สุดเท่าที่ทำได้ โดยวิธีการพิมต้องไม่เกิน 3 บรรทัด")['content']
                cln = re.sub(r'\([^)]*\)|\*|\:|\ๆ','',result)
                end_time =  time.time()
                time_taken = (end_time - start_time)*1000
                print(f'Bard API :{time_taken:2f} ms')
                print(cln)

                start_time = time.time()
                tts = gTTS(text=cln, lang=lan, slow=False)
                sound = AudioSegment.from_file(BytesIO(tts.save()),format="mp3")
                play(sound)
                end_time = time.time()
#                sound.save('test.mp3')
#                os.system('cvlc --play-and-exit test.mp3')
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

