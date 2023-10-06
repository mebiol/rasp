import speech_recognition as sr
from gtts import gTTS
import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('PASSWORD')
model = 'gpt-3.5-turbo'



def transcribe_mic():
        recog = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        lan='th'
        while True:
                print('Listening...')
                with mic as source:
#                       recog.adjust_for_ambient_noise(source,duration=2)
#                       recog.energy_threshold = 4000
#                       audio = recog.listen(source)
                        audio = recog.listen(source,timeout=3,phrase_time_limit=15)
                try:
                        print("processing...")
                        text = recog.recognize_google(audio,language='th-TH')
                        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                                messages = [{"role":"user",
                                                                "content":f"{text}"}])
                        res_txt = response.choices[0].messages.content
                        print(res_txt)
                        sound = gTTS(text=res_text,lang=lan,slow=False)
                        sound.save('test.mp3')
                        os.system('cvlc --play-and-exit test.mp3')
                except sr.UnknownValueError:
                        time.sleep(2)
                        print('Silence found, shutting up...')
                        continue
                except sr.RequestError as e:
                        print(f'Could not request result from google Speech Recognition service; {e}')
                        continue

def main():
        transcribe_mic()

if __name__ == "__main__":
        main()
