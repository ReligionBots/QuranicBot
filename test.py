import http.client
import requests as req
import json
from Utils import utils as ut

def requestLan(language,chapter):
    languages = ut.readJSON(ut.directory['transJSON'])
    lang_details = None
    for i in languages:
        logics = (i['lang_all_lower'] == language.lower(),
                    i['iso_code'] == language.lower())
        if any(logics):
            lang_details = i
            break
    if lang_details == None:
       return
    try:
        json_data = req.get(
            f"https://api.quran.com/api/v4/chapters/{chapter}")
        chapter_details = json.loads(json_data.text)
    except req.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    allVerses = {
        "verses": [],
        "chapter_details": chapter_details,
        "translation_details": lang_details
    }
    reach, index = False, 1
    while not reach:
        try:
            json_data = req.get(
                f"https://api.quran.com/api/v4/verses/by_chapter/{chapter}?language=en&words=false&translations={lang_details['id']}&page={index}")
            verses = json.loads(json_data.text)
        except req.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

        if len(verses['verses']) == 0:
            reach = True
            break
        else:
            pageVerse = verses['verses']

            for i in pageVerse:
                allVerses['verses'].append(i)
            index += 1

    return allVerses



data = requestLan("ku", 1)

print(data['translation_details'], data['verses'], data['chapter_details'])


for i in range(5):
    print(i)


