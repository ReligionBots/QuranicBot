# import http.client
import requests as req
import os
import json
import discord
from Utils import utils as ut
from discord.ext import tasks, commands
from dotenv import load_dotenv
import http.client as ht


# @bot.command()
# async def playyt(ctx, url):
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#     except PermissionError:
#         em8 = discord.Embed(title="Music Is Currently Playing",
#                             description='Please wait for the current playing music to end or use %leave <:_Paimon6:827074349450133524>.\nMusic provided by {ctx.author.mention} <:_Paimon6:827074349450133524>', color=ctx.author.color)
#         await ctx.send(embed=em8)
#         return

#     voiceChannel = discord.utils.get(ctx.guild.voice_channels)
#     await voiceChannel.connect()
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     em6 = discord.Embed(title="Downloading Youtube Music",
#                         description=f'{url}\n\nPlease wait for paimon to setup the music you provide.\nMusic provided by {ctx.author.mention} <:_Paimon6:827074349450133524>', color=ctx.author.color)
#     await ctx.send(embed=em6, delete_after=2)
#     await ctx.message.delete()

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '196',
#         }],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             os.rename(file, "song.mp3")
#     voice.play(discord.FFmpegPCMAudio("song.mp3"))
#     em1 = discord.Embed(title="Now Listening Youtube Music",
#                         description=f'{url}\n\nPlease use %leave first to change music.\nMusic provided by {ctx.author.mention} <:_Paimon6:827074349450133524>', color=ctx.author.color)

#     videoID = url.split("watch?v=")[1].split("&")[0]

#     em1.set_thumbnail(
#         url=f'https://img.youtube.com/vi/{videoID}/default.jpg'.format(videoID=videoID))
#     await ctx.send(embed=em1)







conn = ht.HTTPConnection("tx-01.botgate.xyz", 1059)


def request():
    conn.request("GET", f"/pre/get")
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))



print(request())

