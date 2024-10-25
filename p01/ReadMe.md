import base64

s="Hello"
se = base64.b64encode(s.encode('utf-8'))
sd = (base64.b64decode(se))
print(se,s)



import requests

url = 'http://localhost:8080/touch'
myobj = {'name': 'sample.txt'}

x = requests.post(url, json = myobj)

print(x.text)