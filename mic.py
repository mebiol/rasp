import speech_recognition as sr

print(sr.Microphone.list_microphone_names())
mic = sr.Microphone(4)
recog = sr.Recognizer()

with mic as source:
   print('listen')
   recog.adjust_ambient_noise(source,duration=1)
   audio=recog.listen(source)
   text = recog.recognize_google(audio,language='th-TH')
   print(text)
