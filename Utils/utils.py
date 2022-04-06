import json
import string_utils
import requests as req
from discord.ext import commands


directory = {
    "extJSON": "QuranicBot/Data/JSON/extensions.json",
}

# directory = {
#     "prefixJSON": "./Data/JSON/prefixes.json",
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
        textLines = text.read();
        return textLines


def readJSON(directory):
    with open(directory, "r") as pre:
        return json.load(pre)

# a function for updating JSON files


def updateJSON(directory, newData):
    with open(directory, "w") as oldData:
        json.dump(newData, oldData)

# a function for getting server prefix


def getPrefix(client, message):
    getReq = req.get("http://localhost:3003/pre/get")
    prefixes = json.loads(getReq.text)
    for i in prefixes:
        if i['guild'] == str(message.guild.id):
            return i['prefix']

    return prefixes[0]['prefix']

# a function for creating server prefixes


def prefixCreation(ctx, prefix):
    data = readJSON(directory['prefix'])
    prefixes = data['prefixes']
    if not " " in prefix:
        index = 0
        for i in prefixes:
            if str(ctx.guild.id) == i['guild']:
                if prefix != i['prefix']:
                    data['prefixes'][index]['prefix'] = prefix

                    updateJSON(directory['prefix'], data)
                    status = {
                        "status": 1,
                        "data": commands.Bot(command_prefix=prefix)
                    }
                    return status
                elif prefix == i['prefix']:
                    status = {
                        "status": 1,
                        "data": commands.Bot(command_prefix=i['prefix'])
                    }
                    return status
                else:
                    continue
            index = index + 1

        gid = str(ctx.guild.id)
        guildData = {
            "id": len(prefixes),
            "guild": gid,
            "prefix": prefix
        }
        data['prefixes'].append(guildData)
        updateJSON(directory['prefix'], data)
        print("here")
        status = {
            "status": 1,
            "data": commands.Bot(command_prefix=prefix)
        }
        return status
    else:
        status = {
            "status": 0,
            "data": f"Sorry, you used the wrong context, try again"
        }
        return status
