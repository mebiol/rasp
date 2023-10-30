import requests
import IPython
 
#ระบุ api key
Apikey='d42uuQuLvWm13dAjiBmgFkdFPpsnPzvL'
 
# สังเคราะห์เสียง
url = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
headers = {'Apikey':Apikey,'Content-Type' : 'application/json'}
text = 'ไปดีมาดีนะ'
data = {'input_text':text,'speaker': 1, 'phrase_break':0, 'audiovisual':0}
response = requests.post(url, json=data, headers=headers)
print(response.json())
 
# ดาวน์โหลดไฟล์เสียง
resp = requests.get(response.json()['wav_url'],headers={'Apikey':Apikey})
if resp.status_code == 200:
  with open('test.wav', 'wb') as a:
    a.write(resp.content)
    print('Downloaded: ')
    IPython.display.display(IPython.display.Audio('test.wav'))
else:
  print(resp.reason)