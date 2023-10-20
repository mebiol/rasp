import speech_recognition as sr

mic = sr.Microphone(1)
recog = sr.Recognizer()
lan='th'

try:
	with mic as source:
		recog.adjust_for_ambient_noise(source,duration=1)
		audio=recog.listen(source,timeout=1)
		txt=recog.recognize_google(audio,language='th-TH')
		print(txt)
except AssertionError:
	print('nah')
