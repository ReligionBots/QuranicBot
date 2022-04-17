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
        self.languages = ut.readJSON(ut.directory['transJSON'])
        self.data = ut.readJSON(ut.directory['helpJSON'])
        
    def setInitEmbed(self,ctx,data, bit):
        new_data = data['chapter_details']['chapter']
        url_1, url_2, icon_url = f"https://quran.com/{new_data['id']}", "https://quran.com/", "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        embed = discord.Embed(
            title=f" Surah {new_data['name_simple']}", url=url_1, color=ctx.author.color)
        num_verses = new_data['verses_count']
        if bit:
            embed.set_author(name=f"Holy Quran  (Translation by: {data['translation_details'][0]['name']})",
                         url=url_2, icon_url=icon_url)
        else:
            embed.set_author(name=f"Holy Quran",
                             url=url_2, icon_url=icon_url)
        # print("here 1")
        embed.set_footer(text=f"Number of Ayahs In The Surah: {num_verses}")
        embed.timestamp = dt.datetime.now().astimezone()
        return embed
    

    def textCleansing(self, text):
        count, index, start, end,new_text, new_str_1= 0, 0, None, None,"", ""
        text += " "  # this for index correction
        new_text = text
        for i in range(len(text)):
            if count > 0:
                if text[i] == ">" and not index == 2:
                    index += 1
                    end = i
                elif index == 2:
                    new_str_1 = text[start:end+1]
                    print(new_str_1)
                    # print(new_str_1)
                    new_text = new_text.replace(new_str_1, " ")
                    count, index = 0, 0
                    pass
            elif text[i] == "<":
                start = i
                count += 1
        print(new_text)
        return new_text

    
    
    def errorEmbed(self, title, error):
        return discord.Embed(title=title, description=error, color=0xFFBA01)
    

    async def requestLan(self, ctx, language, chapter):
        # if chapter_details['status'] == 404:
        #     await ctx.message.reply(embed=self.errorEmbed("Call Error", "Sorry, there was an error with the call."))
        #     return

        languages = self.languages
        lang_details = []
        for i in language:
            for j in languages:
                logics = (j['lang_all_lower'] == i.lower(),
                        j['iso_code'] == i.lower())
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

    def compareId(self,id, data):
        for i in data['translation_details']:
            if id == i['id']:
                return True
        return False
    
    
    @commands.command(pass_context=True)
    async def tQuran(self, ctx, *args):
        collect = []
        arg_num = len(args)
        nums = args[0].split(":") # splitting up chapter and ayahs
        if arg_num >= 2 and arg_num < 10:      
            for i in range(len(args)):
                if args[i][0].isnumeric() and i == 0:
                    continue
                elif args[i][0].isalpha() and i > 0:
                    collect.append(args[i])
                else:
                    await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter the translation or numbers correctly."))
            
            if '-' in args[0] and arg_num == 2:
                ayahs = nums[1].split("-")
                start = int(ayahs[0])
                end = int(ayahs[1])
                if (end - start) > 15 or (end - start) < 0:
                    await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please let the range of ayahs not more than 15."))
                    return 
                lang_data = await self.requestLan(ctx, collect, nums[0])

                embed = self.setInitEmbed(ctx,lang_data, 1)

                for j in lang_data['verses']:

                    if j['verse_number'] >= start and j['verse_number'] <= end:
                        for l in j['translations']:
                            text = self.textCleansing(l['text'])
                            embed.add_field(
                                name=f"{nums[0]}:{j['verse_number']}", value=f"{text}", inline=False)
                await ctx.send(embed=embed)
                
            elif args[0][0].isnumeric() and args[1][0].isalpha():
                if ":" in args[0]:
                     
                    lang_data = await self.requestLan(ctx, collect, nums[0])

                    embed = self.setInitEmbed(ctx,lang_data, 0)
                    num = int(nums[1])
                    for j in lang_data['verses']:
                        
                        if j['verse_number'] == num:
                            index = 0
                            for l in j['translations']:
                                text = self.textCleansing(l['text'])
                                for i in lang_data['translation_details']:
                                    if l['resource_id'] == i['id']:
                                        trans_name = i['name']
                                embed.add_field(
                                    name=f"{args[0]}", value=f"{text}\n\n __*Translation By: {trans_name}*__", inline=False)
                                index += 1
                            break
                    await ctx.send(embed=embed)
                    
                else:
                    await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter The Surah and Ayah correctly."))

            else:
                await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter the translation or numbers correctly."))
        else:
            await ctx.message.reply(embed=self.errorEmbed("Wrong Entering", "Please Enter the translation or numbers correctly."))
        
        @commands.command(pass_context=True)
        async def languages(self, ctx, string: str):        
            value = ""
            embed = self.setInitEmbed(ctx)
            for i in self.data['helpFull']['languages_data']:
                embed.add_field(name=f"code: {i['lang_code']}", value=f"name: {i['lang_name']}", inline=True)
            embed.timestamp = dt.datetime.now().astimezone()
            await ctx.send(embed=embed)
            pass

def setup(bot):
    bot.add_cog(Translations(bot))
