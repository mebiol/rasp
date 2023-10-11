import speech_recognition as sr
from gtts import gTTS
import os
import time
import openai
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.getenv('PASSWORD')
# model = 'gpt-3.5-turbo'

# print(sr.Microphone.list_microphone_names ())

def transcribe_mic():
    recog = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    lan = 'th'
    while True:
        print('Listening...')
        try:
            with mic as source:
                audio = recog.listen(source, timeout=5)  # Set a timeout to prevent hanging
                if audio is not None:
                        print("Processing...")
                        text = recog.recognize_google(audio, language='th-TH')
                        print(text)
                        sound = gTTS(text=text, lang=lan, slow=False)
                        sound.save('test.mp3')
                        os.system('test.mp3')
                else:
                        continue
        except sr.WaitTimeoutError:
            print('No speech detected. Listening again...')
            continue
        except sr.UnknownValueError:
            print('Speech recognition could not understand audio')
        except sr.RequestError as e:
            print(f'Could not request result from Google Speech Recognition service: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')

def main():
    transcribe_mic()

if __name__ == "__main__":
    main()

