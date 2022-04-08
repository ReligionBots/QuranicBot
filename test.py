import http.client
import requests as req
import json
from Utils import utils as ut


text = "And ˹remember˺ when We said to the angels, “Prostrate before Adam,”<sup foot_note=76385>1</sup> so they all did—but not Iblîs,<sup foot_note=76386>2</sup> who refused and acted arrogantly,<sup foot_note=76387>3</sup> becoming unfaithful."


def deleteWords():

    return 

def textCleansing(text):
    count, index, start, end, new_str_1, new_str_2 =0, 0, None, None, "", ""
    new_text = text
    for i in range(len(text)):
        if count > 0:
            if text[i] == ">" and not index == 2 :
                index += 1
                end = i
            elif index == 2:
                new_str_1 = text[start:end+1]
                print(new_str_1)
                new_text = new_text.replace(new_str_1.strip(), " ")
                count, index = 0, 0
                pass
        elif text[i] == "<":
            start = i
            count += 1
            
    return new_text



new_text = textCleansing(text)

print(new_text)







