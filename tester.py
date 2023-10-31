import speech_recognition as sr
from gtts import gTTS
import requests
from bardapi import Bard
import os
import re
import IPython


# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

res = requests.get("http://192.168.1.42:5001/api")
data = res.json()
msg = data['msg']
Apikey = 'd42uuQuLvWm13dAjiBmgFkdFPpsnPzvL'

chosen_system = input("Choose TTS system (vaja/google): ")
chosen_mode = None if chosen_system == "google" else input('Select mode in 0-4: ')

def listen_and_transcribe():
    with mic as source:
        print("Adjusting for ambient noise...")
        recog.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")
        audio = recog.listen(source, timeout=2)
        text = recog.recognize_google(audio, language='th-TH')
        return text 

def synth_vaja(data):
    url = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
    headers = {'Apikey': Apikey, 'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    resp = requests.get(response.json()['wav_url'],headers={'Apikey':Apikey})
    if resp.status_code == 200:
        with open('test.wav', 'wb') as a:
            a.write(resp.content)
            print('Downloaded: ')
            IPython.display.display(IPython.display.Audio('test.wav'))
            os.system('cvlc --play-and-exit test.wav')
    else:
            print(resp.reason)
    return response.json()

def google_tts(text, lang):
    sound = gTTS(text=text, lang=lang, slow=False)
    sound.save('test.mp3')
    os.system('cvlc --play-and-exit test.mp3')

def ask_tts_system(text, lang):
    global chosen_system, chosen_mode

    if chosen_system == 'vaja':
        if chosen_mode == '1':
            data = {'input_text': text, 'speaker': 1, 'phrase_break': 0, 'audiovisual': 0}
        elif chosen_mode == '2':
            data = {'input_text': text, 'speaker': 2, 'phrase_break': 0, 'audiovisual': 0}
        elif chosen_mode == '3':
            data = {'input_text': text, 'speaker': 3, 'phrase_break': 0, 'audiovisual': 0}
        elif chosen_mode == '4':
            data = {'input_text': text, 'speaker': 4, 'phrase_break': 0, 'audiovisual': 0}
        else:
            print("Invalid mode for Vaja. Defaulting to mode 1.")
            data = {'input_text': text, 'speaker': 1, 'phrase_break': 0, 'audiovisual': 0}
        return synth_vaja(data)
    elif chosen_system == 'google':
        return google_tts(text, lang)
    else:
        print("Unknown TTS system. Defaulting to Google.")
        return google_tts(text, lang)

def generate_bard_response(text, token):
    bard = Bard(token=token)
    result = bard.get_answer(f"You are a kind female doctor named Tanya. Respond to the following: {text} Explain the most important way you can help me. The answer should be no more than 20 words.")['content']
    cleaned_result = re.sub(r'\([^)]*\)|\*|\:', '', result)
    return cleaned_result

def transcribe_mic(msg):
    global chosen_system, chosen_mode

    while True:
        try:
            transcribed_text = listen_and_transcribe()
            print(transcribed_text)

            ask_tts_system('กรุณารอสักครู่', lan)

            response = generate_bard_response(transcribed_text, msg)
            print(response)

            ask_tts_system(response, lan)

            # At the end of the loop, ask if the user wants to change the TTS system or mode:
            change_system = input("Do you want to change the TTS system? (yes/no): ").lower()
            if change_system == 'yes':
                chosen_system = input("Choose TTS system (vaja/google): ")
                chosen_mode = None if chosen_system == "google" else input('Select mode in 0-4: ')

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
