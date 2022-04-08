import os
import json
import discord
import requests as req
from discord.ext import tasks, commands
from Utils import utils as ut
import datetime as dt
# from dotenv import load_dotenv


class Translations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def setInitEmbed(self,data):
        url_1, url_2, icon_url = "https://something.com", "https://quran.com/", "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        embed = discord.Embed(
            title=f"{data['chapter_details']['chapter']['name_simple']}", url=url_1, color=0x2C2F33)
        name = data
        embed.set_author(name=f" الكريم القرآن ", url=url_2, icon_url=icon_url)
                    
        embed.set_footer(text=f"Number of Ayahs In The Surah: {len(data)}")
        embed.timestamp = dt.datetime.now().astimezone()
        return embed
        
    def errorEmbed(self, title, error):
        return discord.Embed(title=title, description=error, color=discord.Color.blue())
    
    async def requestLan(self, ctx,language, chapter):
        # if chapter_details['status'] == 404:
        #     await ctx.message.reply(embed=self.errorEmbed("Call Error", "Sorry, there was an error with the call."))
        #     return 

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
            await ctx.message.reply(embed=self.errorEmbed("Call Error", f"{e}"))

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
                await ctx.message.reply(embed=self.errorEmbed("Call Error", f"{e}"))

            if len(verses['verses']) == 0:
                reach = True
                break
            else:
                pageVerse = verses['verses']

                for i in pageVerse:
                    allVerses['verses'].append(i)
                index += 1

        return allVerses



                        
    @commands.command(pass_context=True)
    async def tQuran(self, ctx, *args):
        collect = []
        
        if args and len(args) >= 2:
            if args[0][0].isnumeric() and args[1][0].isalpha():
                if ":" in args[0]:
                    nums = args[0].split(":")
                   
                    for i in range(len(args)):
                        if args[i][0].isnumeric() and i == 0:
                            continue
                        elif args[i][0].isalpha() and i > 0:
                            collect.append(args[i])
                        else:
                            await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter the translation or numbers correctly."))
                   
                    translation_data = []
                    for i in collect:
                        json_data = self.requestLan(ctx,i, nums[0])
                        translation_data.append(json_data)

                    embed = self.setInitEmbed(translation_data[0])
                    for i in translation_data:
                        

                else:
                    await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter The Surah and Ayah correctly."))

            else:
                await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter the translation or numbers correctly."))
        else:
            pass
        


def setup(bot):
    bot.add_cog(Translations(bot))
