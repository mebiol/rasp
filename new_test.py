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
    lan = 'th'

    while True:
        print('Listening...')
        with mic as source:
#            recog.adjust_for_ambient_noise(source, duration=2)
            recog.energy_threshold = 4000
            try:
                audio = recog.listen(source, timeout=3)
            except sr.WaitTimeoutError:
                print('No audio detected. Waiting...')
                continue

            if audio is None:
                print('No audio captured. Trying again...')
                continue

            print("Processing...")
            text = recog.recognize_google(audio, language='th-TH')
            print("Recognized text:", text)

            # Send the text to OpenAI GPT-3.5 Turbo
#            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
#            res_text = response.choices[0].message['content']
#            print("Response from GPT-3:", res_text)

            # Convert response to speech
            sound = gTTS(text=text, lang=lan, slow=False)
            sound.save('test.mp3')
            os.system('cvlc --play-and-exit test.mp3')

def main():
    transcribe_mic()

if __name__ == "__main__":
    main()
