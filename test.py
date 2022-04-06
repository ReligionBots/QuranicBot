import http.client
import requests as req
import json


conn = http.client.HTTPSConnection("api.quran.com")
# conn = http.client.HTTPConnection("api.alquran.cloud")
payload = "{}"

conn.request("GET", f"/api/v4/verses/by_chapter/100?language=en&words=true&page=1")

res = conn.getresponse()
data = res.read()
newData = json.loads(data.decode("utf-8"))
printing = ""
index = 0
for i in newData['verses']:
    for j in i['words']:
        printing = printing +" "+ j['translation']['text'] 
    index = index + 1
    
print(f"ayahs: {printing}")
# print(data.text)




