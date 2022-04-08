import json
import http.client as ht
import requests as req

# # all_translations = json.loads(data.decode('utf-8'))
data = req.get("https://api.quran.com/api/v4/resources/translations")
json_data = json.loads(data.text)
print(json_data['translations'][0])

data_1 = req.get("https://api.quran.com/api/v4/resources/languages")
json_data_1 = json.loads(data_1.text)
print(json_data_1)

languages = json_data_1['languages']
translations = json_data['translations']

dictionary =[]

for i in translations:
    for j in languages:
        if i['language_name'].lower() == j['name'].lower():
            code = j['iso_code']
            break
        
    dictionary.append(
        {   "id": i['id'],
            "name": i['name'],
            "author_name": i['author_name'],
            "slug": i['slug'],
            "lang_first_upper": i['language_name'].capitalize(),
            "lang_all_lower": i['language_name'],
            "iso_code": code
        }
    )

with open("QuranicBot/Data/JSON/translations.json", "w") as f:
    json.dump(dictionary, f)





