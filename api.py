import requests
from bardapi import Bard
import os
res = requests.get("http://192.168.1.38:5001/api")


data = res.json()
msg = data['msg']

bard=Bard(token=msg)
result=bard.get_answer("วันนี้ วันที่เท่าไหร่")['content']
audio = bard.speech(result,lang='th-TH')
with open("bard_res.mp3","wb") as f:
   f.write(audio['audio'])
os.system('cvlc --play-and-exit bard_res.mp3')
