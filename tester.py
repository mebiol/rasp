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


def listen_and_transcribe():
    with mic as source:
        print("Adjusting for ambient noise...")
        recog.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")
        audio = recog.listen(source, timeout=2)
        text = recog.recognize_google(audio, language='th-TH')
        return text


def generate_bard_response(text, token):
    bard = Bard(token=token)
    result = bard.get_answer(f"You are a kind female doctor named Tanya. Respond to the following: {text} Explain the most important way you can help me. The answer should be no more than 20 words.")['content']
    cleaned_result = re.sub(r'\([^)]*\)|\*|\:', '', result)
    return cleaned_result


def text_to_speech(text, lang):
    sound = gTTS(text=text, lang=lang, slow=False)
    sound.save('test.mp3')
    os.system('cvlc --play-and-exit test.mp3')


def transcribe_mic(msg):
    while True:
        try:
            transcribed_text = listen_and_transcribe()
            print(transcribed_text)

            response = generate_bard_response(transcribed_text, msg)
            print(response)

            text_to_speech(response, lan)

        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for an audio source...")
        except requests.ConnectionError as e:
            print(f"Connection error occurred:{e}")
            msg = None
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main():
    transcribe_mic(msg)


if __name__ == "__main__":
    main()
