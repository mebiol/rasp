import speech_recognition as sr
from gtts import gTTS
import requests
import browser_cookie3
from bardapi import Bard
import os
import re
import time
import IPython

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

cj = browser_cookie3.firefox()
secure_1psid_cookie = None

for cookie in cj:
    if cookie.name == '__Secure-1PSID':
        secure_1psid_cookie = cookie.value
        break

Apikey = 'd42uuQuLvWm13dAjiBmgFkdFPpsnPzvL'

chosen_system = input("Choose TTS system (vaja/google): ")
chosen_mode = None if chosen_system == "google" else input('Select mode in 0-4: ')

def play_sound(chosen_system, name):
    """Play the sound based on the chosen system and filename."""
    if chosen_system == 'vaja':
        os.system(f'cvlc --play-and-exit {name}.wav')
    elif chosen_system == 'google':
        os.system(f'cvlc --play-and-exit {name}.mp3')

def listen_and_transcribe():
    with mic as source:
        print("Adjusting for ambient noise...")
        recog.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")
        audio = recog.listen(source, timeout=2)
        print("recog listen")
        text = recog.recognize_google(audio, language='th-TH')
        print("recog google")
        return text

def synth_vaja(data, name, max_retries=10):
    url = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
    headers = {'Apikey': Apikey, 'Content-Type': 'application/json'}
    
    for i in range(max_retries):
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError if the response was an error
            
            if 'wav_url' not in response.json():
                print("Error: 'wav_url' not found in the response!")
                return None
            else:
                status = True
            while status:
                resp = requests.get(response.json()['wav_url'], headers={'Apikey': Apikey})
                if resp.status_code == 200:
                    with open(f'{name}.wav', 'wb') as a:
                        a.write(resp.content)
                        print('Downloaded: ')
                        IPython.display.display(IPython.display.Audio(f'{name}.wav'))
                        status = False 
                        return response.json()
                else:
                    print('----------------------------')
                    print(resp.reason)
                    time.sleep(0.1)  # Exponential backoff

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and i < max_retries - 1:
                print(f"Rate limit exceeded. Retrying... {i}")
                time.sleep(0.1)  # Exponential backoff
            else:
                print(f"Error occurred synth_vaja: {e}")
                return None


def google_tts(text, lang, name):
    sound = gTTS(text=text, lang=lang, slow=False)
    sound.save(f'{name}.mp3')

def ask_tts_system(text, lang, name):
    global chosen_system, chosen_mode
    if chosen_system == 'vaja':
        # simplified using a dictionary to map modes to speakers
        speaker_mapping = {'1': 0, '2': 1, '3': 2, '4': 3}
        speaker = speaker_mapping.get(chosen_mode, 0)
        data = {'input_text': text, 'speaker': speaker, 'phrase_break': 0, 'audiovisual': 0}
        return synth_vaja(data, name)
    elif chosen_system == 'google':
        return google_tts(text, lang, name)
    else:
        print("Unknown TTS system. Defaulting to Google.")
        return google_tts(text, lang, name)

def generate_bard_response(text, token):
    bard = Bard(token=token)
    result = bard.get_answer(f"You are a kind female doctor named Tanya. Respond to the following: {text} Explain the most important way you can help me. The answer should be no more than 20 words.")['content']
    cleaned_result = re.sub(r'\([^)]*\)|\*|\:', '', result)
    return cleaned_result

def transcribe_mic(secure_1psid_cookie):
    global chosen_system, chosen_mode
    ask_tts_system('กรุณารอสักครู่', lan, 'zwait')
    play_sound(chosen_system,'zwait')
    ask_tts_system('มีอะไรอยากถามเพิ่มเติมไหม', lan, 'zagain')
    ask_tts_system('สวัสดี ฉันคือคุณหมอทันย่า อยากถามอะไรไหม', lan, 'zrespond')
    play_sound(chosen_system,'zrespond')    
    while True:
        try:
            transcribed_text = listen_and_transcribe()
            print(transcribed_text)
            play_sound(chosen_system, 'zwait')
            response = generate_bard_response(transcribed_text, secure_1psid_cookie)
            print(response)
            ask_tts_system(response, lan, 'zrespond')
            play_sound(chosen_system,'zrespond')
            play_sound(chosen_system,'zagain')  
        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for an audio source...")
        except requests.ConnectionError as e:
            print(f"Connection error occurred:{e}")
            secure_1psid_cookie = None
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    transcribe_mic(secure_1psid_cookie)

if __name__ == "__main__":
    main()
      