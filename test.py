# import http.client
import requests as req
import json
from Utils import utils as ut


# text = "And ˹remember˺ when We said to the angels, “Prostrate before Adam,”<sup foot_note=76385>1</sup> so they all did—but not Iblîs,<sup foot_note=76386>2</sup> who refused and acted arrogantly,<sup foot_note=76387>3</sup> becoming unfaithful."

def requestLan(language, chapter):
     # if chapter_details['status'] == 404:
     #     await ctx.message.reply(embed=self.errorEmbed("Call Error", "Sorry, there was an error with the call."))
      #     return

    languages = ut.readJSON(ut.directory['transJSON'])
    lang_details = []
    for i in language:
        for j in languages:
            logics = (j['lang_all_lower'] == i.lower(), j['iso_code'] == i.lower())
            if any(logics):
                lang_details.append(j)
                break
    if len(lang_details) == 0:
        return
    
    try:
        json_data = req.get(f"https://api.quran.com/api/v4/chapters/{chapter}")
        chapter_details = json.loads(json_data.text)
    except req.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    allVerses = {
        "verses": [],
        "chapter_details": chapter_details,
        "translation_details": lang_details
    }
    reach, index = False, 1
    lang_join = allVerses['translation_details']
    while not reach:
        try:
            json_data = req.get(
                f"https://api.quran.com/api/v4/verses/by_chapter/{chapter}?language=en&words=false&translations={','.join(format(l['id']) for l in lang_join)}&page={index}")
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
    print(allVerses['translation_details'])
    return allVerses


lang = ["ku", "en", "tr"]

data = requestLan(lang, 3)




print(f"{data}")



