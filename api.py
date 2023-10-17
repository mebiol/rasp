import requests

res = requests.get("http://192.168.1.106:5000/api")
data = res.json()
print(data['msg'])
