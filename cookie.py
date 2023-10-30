import browser_cookie3
import speech_recognition as sr
from bardapi import Bard
import os 
cj = browser_cookie3.firefox()
sec = None

for i in cj:
	if i.name == '__Secure-1PSID':
		sec = i.value
		break

while True:
	i = input('รายละเอียด ')
	bard = Bard(token=sec)
	result = bard.get_answer('ท้องฟ้ามีสีอะไรบ้าง')['content']
	print(result)
	audio = bard.speech(result)
	with open('speech.ogg','wb') as f:
		f.write(bytes(audio['audio']))
