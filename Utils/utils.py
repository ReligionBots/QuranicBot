import json
import string_utils
import requests as req
from discord.ext import commands
#import http.client as ht

directory = {
    "extJSON": "./Data/JSON/extensions.json",
    "transJSON": "./Data/JSON/translations.json"
}

# directory = {
#     "extJSON": "QuranicBot/Data/JSON/extensions.json",
#     "transJSON": "QuranicBot/Data/JSON/translations.json"
# }



#     "extJSON": "./Data/JSON/extensions.json",
#     "rapsJSON": "./Data/JSON/raps.json"
#     "rapsText": "./Data/Text/rap.txt"
# }

# a function to make the string not having the unnecessary symbols


def strPurify(string):
    if '"' in string:
        return string.replace('"', '\"')


# creating random strings
def randString():
    string = "0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    spliced = string_utils.shuffle(string)
    return spliced[0:18]

# make in it a function in case there was more data to be added


def values(string):
    if "raps" in string:
        newString = 'rapId'
    elif "rap" in string:
        newString = 'lyricId'
    return newString

# creating new ids, and see if they are similar to previous ones or not


def generateId(rapIds, string):

    # returning the part needed to be reed from the array
    newString = values(string)

    #choosing the random string
    newId = randString()

    # see if the length of the array we want to add the values to, is 0 or not
    # and return the values depending on that
    if len(rapIds[string]) == 0:
        return newId
    else:
        value1 = rapIds[string]
        for data in value1:
            if newId == data[newString]:
                continue
            else:
                return newId


# a function for reading text files
def readTextLines(directory):
    with open(directory, "r") as pre:
        text = pre
        textLines = text.readlines()
        return textLines

# a function for reading JSON files


def readText(directory):
    with open(directory, "r") as pre:
        text = pre
        textLines = text.read()
        return textLines


def readJSON(directory):
    with open(directory, "r") as pre:
        return json.load(pre)

# a function for updating JSON files


def updateJSON(directory, newData):
    with open(directory, "w") as oldData:
        json.dump(newData, oldData)

# a function for getting server prefix


# def request():
#     conn = ht.HTTPConnection("tx-01.botgate.xyz", 1059, timeout=10)
#     conn.request("GET", f"/pre/get/")
#     res = conn.getresponse()
#     data = res.read()
#     return json.loads(data.decode("utf-8"))


def get_prefix_1(client, message):
    preifxes = ""
    url = "http://tx-01.botgate.xyz:1059/pre/get/"
    try:
        prefixes = req.get(url=url, timeout=10)
    except Exception as error:
        print(error)
    prefixes_json = json.loads(prefixes.text)

    for i in prefixes_json:
        if i['guild'] == str(message.guild.id):
            return i['prefix']

    return prefixes_json[0]['prefix']


def get_prefix_2(message):
    preifxes = ""
    url = "http://tx-01.botgate.xyz:1059/pre/get/"
    try:
        prefixes = req.get(url=url, timeout=10)
    except Exception as error:
        print(error)
    prefixes_json = json.loads(prefixes.text)

    for i in prefixes_json:
        if i['guild'] == str(message.guild.id):
            return i['prefix']

    return prefixes_json[0]['prefix']




# a function for creating server prefixes


def prefixCreation(ctx, prefix):
    url = "http://tx-01.botgate.xyz:1059/pre/get/"
    data = req.get(url=url, timeout=10)
    data = json.loads(data.text)
    prefixes = data
    if not " " in prefix:
        index = 0
        for i in prefixes:
            if str(ctx.guild.id) == i['guild']:
                if prefix != i['prefix']:
                    string_1 = {'prefix': prefix}
                    url = f"http://tx-01.botgate.xyz:1059/pre/update/{ctx.guild.id}/{json.dumps(string_1)}/"
                    req.patch(url=url, timeout=10)
                    
                    status = {
                        "status": 1,
                        "data": commands.Bot(command_prefix=prefix)
                    }
                    return status
                elif prefix == i['prefix']:
                    status = {
                        "status": 2,
                        "data": commands.Bot(command_prefix=i['prefix'])
                    }
                    return status
                else:
                    continue
            index = index + 1
        try:
            gid = str(ctx.guild.id)
            guild_data = {'guild': gid,'prefix':prefix}
            url = f"http://tx-01.botgate.xyz:1059/pre/post/{json.dumps(guild_data)}"
            req.post(url=url, timeout=10)
            print("here")
            status = {
                "status": 1,
                "data": commands.Bot(command_prefix=prefix)
            }
        except Exception as error:
            status = {
                "status": 0,
                "error": error,
                "data": f"Sorry, there was an error, try again"
            }
            print(error)
        return status
    else:
        status = {
            "status": 0,
            "data": f"Sorry, you used the wrong context, try again"
        }
        return status
