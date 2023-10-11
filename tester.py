import speech_recognition as sr
from gtts import gTTS
import os

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

def transcribe_mic():
    while True:
        try:
            with mic as source:
                print("Adjusting for ambient noise...")
                recog.adjust_for_ambient_noise(source, duration=1)
                print("Listening for speech...")
                audio = recog.listen(source, timeout=3)
                text = recog.recognize_google(audio, language='th-TH')
                print(text)
                sound = gTTS(text=text, lang=lan, slow=False)
                sound.save('test.mp3')
                os.system('cvlc --play-and-exit test.mp3')
        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except AssertionError:
            print("No audio source available. Waiting for audio source...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    transcribe_mic()

if __name__ == "__main__":
    main()
