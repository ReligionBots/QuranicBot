import json
import discord
import asyncio
import http.client
import datetime
from Utils import utils as ut
# import requests as req

from discord.ext import tasks, commands
# from Utils import utils as ut
# from dotenv import load_dotenv
conn = http.client.HTTPConnection("api.alquran.cloud")

class Quran(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def arabicNumber(self,string):
        number = {
            '0': '٠',
            '1': '١',
            '2': '۲',
            '3': '۳',
            '4': '٤',
            '5': '٥',
            '6': '٦',
            '7': '٧',
            '8': '۸',
            '9': '۹',
        }
        for i, j in number.items():
            string = string.replace(i, j)
        return string
        
    
    def request(self,num):
        conn.request("GET", f"/v1/surah/{num}/ar")
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    
    def setInitEmbed(self,ctx, data):
        new_data = data['data']
        url_1, url_2, icon_url = f"https://quran.com/{new_data['number']}", "https://quran.com/", "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        embed = discord.Embed(
            title=f"{new_data['name']}", url=url_1, color=ctx.author.color)
        name = new_data['edition']['name']
        embed.set_author(name=f"{name}", url=url_2,icon_url=icon_url)
                    
        embed.set_footer(
            text=f"Number of Ayahs In The Surah: {len(new_data['ayahs'])}")
        embed.timestamp = datetime.datetime.now().astimezone()
        return embed
    
    def errorEmbed(self, title, error):
        return discord.Embed(title=title, description=error, color=0xFFBA01)
    

    @commands.command(pass_context=True)
    async def Quran(self, ctx, *args):
        if '-' in args[0]:
            logics = (args[0], '-' in args[0],":" in args[0],args[0][0].isnumeric())
        else:
            pass
        # conn = http.client.HTTPSConnection("api.quran.com")
        if args:
            if args[0][0].isnumeric() and not '-' in args[0]:
                if ":" in args[0]:
                    nums = args[0].split(":")
                    if int(nums[0]) > 114 or int(nums[0]) < 1:
                        await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"Wrong Number Chosen For The Surah"))
                        return
                    req_data = self.request(nums[0])
                    if len(req_data['data']['ayahs']) < int(nums[1]) - 1:
                        await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"Wrong Ayah Number Chosen For The Surah"))
                        return
                    ayah = req_data['data']['ayahs'][int(nums[1]) - 1]
                    text = ayah['text']
                    # print(len(text))
                    
                    embed = self.setInitEmbed(ctx,req_data)
                
                    embed.add_field(name=f"{self.arabicNumber(args[0])}", value=f"{text}", inline=False)
                    await ctx.send(embed=embed)
                    
            elif all(logics):
                string = args[0].split(":")
                ranges = string[1].split("-") # this will split the ayah ranges selected
                surah = string[0]   # this is the surah
                start, end = int(ranges[0]),int(ranges[1])
                if int(surah) > 114 or int(surah) < 1:
                    await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"Wrong Number Chosen For The surah"))
                    return
                
                req_data = self.request(str(surah))
                ayahs = req_data['data']['ayahs']
                ayah_len = len(ayahs)
               
                if ayah_len < start or start > ayah_len:
                    await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"Wrong Ayah Number Chosen For The surah"))
                    return 
                if (end - start) > 15:
                    await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"The Range is limited to 15 because of character size restriction"))
                    return
                else:
                    if end > ayah_len:
                        end = ayah_len  
                    data_len = 0
                    
                    embed = self.setInitEmbed(ctx,req_data)
                    for i in range(start, end):
                        text = ayahs[i]['text']
                        data_len = data_len + len(text)
                        part = self.arabicNumber(str(surah) + ":" + str(i))
                        embed.add_field(
                            name=f"{part}", value=f"{text}", inline=False)
        
                    print(data_len)
                    await ctx.send(embed=embed)
            else:
                await ctx.send(embed=self.errorEmbed(f"Wrong Entering", f"Wrong Ayah Number Chosen For The surah"))
                return
                    
        else:
            await ctx.send(embed=self.errorEmbed("Wrong Entering", "Fields Left Empty."))
     


def setup(bot):
    bot.add_cog(Quran(bot))
