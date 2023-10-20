import requests
from bardapi import Bard

res = requests.get("http://192.168.1.36:5001/api")
data = res.json()
msg = data['msg']
print(msg)

bard=Bard(token=msg)
result=bard.get_answer("วันนี้ วันที่เท่าไหร่")['content']
print(result)
