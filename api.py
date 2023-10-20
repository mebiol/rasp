import requests
from bardapi import Bard

res = requests.get("http://192.168.1.41:5001/api")


data = res.json()
msg = data['msg']

bard=Bard(token=msg)
result=bard.get_answer("วันนี้ วันที่เท่าไหร่")['content']
print(result)
