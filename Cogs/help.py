import os
import json
import discord
import requests as req
# import http.client
from discord.ext import tasks, commands
from Utils import utils as ut
import datetime
# from dotenv import load_dotenv


class Help(commands.Cog):
    def __init__(self, bot):
    
        self.bot = bot
        self.data = ut.readJSON(ut.directory['helpJSON'])
    
    def setInitEmbed(self,ctx):
        url, icon_url = "https://quran.com", "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        prefix = ut.get_prefix_2(ctx)
        embed = discord.Embed(title=f"Your prefix is: {prefix}",color=ctx.author.color)

        embed.set_author(name=f"Holy Quran",url=url, icon_url=icon_url)
                    
        embed.timestamp = datetime.datetime.now().astimezone()
        return embed

    def handleEmbed(self, title, desc):
        return discord.Embed(title=title, description=desc, color=0xFFBA01)

    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        if not args:
            embed = self.setInitEmbed(ctx)

            for i in self.data['helpIntro']:
                if "help" in i['title']:
                    help_ = ""
                else:
                    help_ = "help"
                embed.add_field(name=f"{help_} {i['title']}", value=i['text'], inline=False)
            await ctx.send(embed=embed)
        else:
            found_1 = False
            # this is for making sure all values are not numeric
            if len(args) == 1 and args[0].isalpha():
                # here we check if the arg is similar to any commands we have
                for i in self.data['helpIntro']:
                    if args[0].strip() == i['title']:
                        print(args[0])
                        key = i['title']
                        found_1 = True
                # then we check if the values we want is found or not
                print(found_1)
                if not found_1:
                    await ctx.send(embed=self.handleEmbed("Wrong Entering", "Please make sure you entered the right commands"))
                    return

                if 'languages' in key:
                    value =""
                    embed = self.setInitEmbed(ctx)
                    for i in self.data['helpFull'][key + '_data']:
                        embed.add_field(name=f"code: {i['lang_code']}", value=f"name: {i['lang_name']}", inline=True)
                    embed.timestamp = datetime.datetime.now().astimezone()
                    await ctx.send(embed=embed)
                    return
                else:   
                    embed = self.setInitEmbed(ctx)
                    for i in self.data['helpFull'][key]:
                     
                        embed.add_field(
                            name=f"{i['title']}", value=f"{i['text']}\n\n~~~  exmaple: **{i['example']}\n\n**", inline=False)
                    await ctx.send(embed=embed)
                    return
            else:
                await ctx.send(embed=self.handleEmbed("Wrong Entering", "Please make sure you entered the right commands"))
                return
       

    @commands.Cog.listener()
    async def on_message(self, message):
        check_mark, prefix = '✅', None
        try:
            prefix = ut.get_prefix_2(message)
            string_1, string_2, string_3 = f"{prefix}tQuran", f"{prefix}Quran", f"{prefix}help"
            msg = message.content
            logics = (
                msg.startswith(string_1),
                msg.startswith(string_2),
                msg.startswith(string_3)
            )
            if any(logics):
                await message.add_reaction(check_mark)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Help(bot))
