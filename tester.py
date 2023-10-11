import speech_recognition as sr
from gtts import gTTS
import os

# Initialize PyAudio and SpeechRecognition
mic = sr.Microphone(1)
recog = sr.Recognizer()
lan = 'th'

def transcribe_mic():
    with mic as source:
        print("Listening for speech...")
        try:
            audio = recog.listen(source, timeout=3)
            text = recog.recognize_google(audio, language='th-TH')
            print(text)
            sound = gTTS(text=text, lang=lan, slow=False)
            sound.save('test.mp3')
            os.system('cvlc --play-and-exit test.mp3')
        except sr.WaitTimeoutError:
            print("Recognition timed out")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    while True:
        transcribe_mic()

if __name__ == "__main__":
    main()
