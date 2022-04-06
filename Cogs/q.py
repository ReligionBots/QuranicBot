import os
import json
import discord
import asyncio
import http.client
import requests as req

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
    
    def setInitEmbed(self,data):
        url_1, url_2, icon_url = "https://something.com", "https://quran.com/", "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        tuple =(44, 47, 51)
        embed = discord.Embed(
            title=f"{data['data']['name']}", url=url_1, color=0x2C2F33)
        name = data['data']['edition']['name']
        embed.set_author(name=f"{name}", url=url_2,icon_url=icon_url)
                    
        embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
                
        return embed
    @commands.command(pass_context=True)
    async def Quran(self, ctx, *args):
        
        # conn = http.client.HTTPSConnection("api.quran.com")
        if args:
            if args[0][0].isnumeric():
                if ":" in args[0]:
                    nums = args[0].split(":")
                   
                    req_data = self.request(nums[0])
                    if len(req_data['data']['ayahs']) < int(nums[1]) - 1:
                        title = f"Wrong Entering"
                        description = f"Wrong Ayah Number Chosen For The Surah"
                        embed = discord.Embed(title=title,description=description, color=discord.Color.blue())
                        await ctx.message.reply(embed=embed)
                        return
                    ayah = req_data['data']['ayahs'][int(nums[1]) - 1]
                    number, text = ayah['number'], ayah['text']
                    # print(len(text))
                    
                    embed = self.setInitEmbed(req_data)
                
                    embed.add_field(name=f"{self.arabicNumber(args[0])}", value=f"{text}", inline=False)
                    await ctx.message.reply(embed=embed)
                    
                elif not ":" in args[0]:
                    if int(args[0]) > 0 and int(args[0]) <= 114:
                        data_len = 0
                        req_data = self.request(args[0])
                        ayahs = req_data['data']['ayahs']
                        
                       
                        # the problem
                        if len(ayahs) > 10:
                            num = len(ayahs) / 10
                            for j in range(2):
                                embed = self.setInitEmbed(req_data)
                                for i in range(len(ayahs)):
                                        number = str(ayahs[i]["numberInSurah"])
                                        text = ayahs[i]["text"]
                                        # allText = allText + " " + text
                                        embed.add_field(name=f"{self.arabicNumber(args[0])}:{self.arabicNumber(number)}", value=f"{text}", inline=False)
                                await ctx.message.reply(embed=embed)
                                asyncio.sleep(1)
                            return
                        else:
                            embed = self.setInitEmbed(req_data)
                            for index in ayahs:
                                number = index["numberInSurah"]
                                text = index["text"]
                                # allText = allText + " " + text
                                embed.add_field(name=f"{self.arabicNumber(args[0])}:{self.arabicNumber(number)}", value=f"{text}", inline=False)

                        await ctx.message.reply(embed=embed)
                    else:
                        embed = discord.Embed(title=f"{self.arabicNumber(args[0])}", url="https://something.com",
                                                            description="Wrong Number Used For Identification", color=discord.Color.blue())
                        await ctx.message.reply(embed=embed)
                # elif len(args[0]) == 1:
                    
        else:
            await ctx.message.reply("Please add the right syntax")
     
    @commands.command(pass_context=True)
    async def testEmbed(self, ctx, *args):

        embed = discord.Embed(title="Test Title", url="https://something.com",
                            description="test description", color=discord.Color.blue())
        embed.set_author(name="RealDrewData", url="https://something.com",
                         icon_url="https://cdn.discordapp.com/avatars/645688850500550677/f91d836817fe21946cf10e6e9ad20ee3?size=512")
        await ctx.message.reply(embed=embed)


def setup(bot):
    bot.add_cog(Quran(bot))
