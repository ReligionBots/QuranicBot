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
        self.data = ut.readJSON(
            'QuranicBot/Data/JSON/help.json') or ut.readJSON('../Data/JSON/help.json')
    
    def setInitEmbed(self,ctx):
        icon_url = "https://cdn.discordapp.com/avatars/958426940581232660/4e1e08d2e06568022f845afcf7cc7b9a?size=512"
        prefix = ut.get_prefix_2(ctx)
        embed = discord.Embed(title=f"Your prefix is: {prefix}",color=ctx.author.color)

        embed.set_author(name=f"Holy Quran", icon_url=icon_url)
                    
        embed.timestamp = datetime.datetime.now().astimezone()
        return embed

    def handleEmbed(self, title, desc):
        return discord.Embed(title=title, description=desc, color=0xFFBA01)

    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        if not args:
            embed = self.setInitEmbed(ctx)
            
            for i in self.data['helpIntro']:
                embed.add_field(name=i['title'], value=i['text'], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("test")
        # else:
            
        # pass

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
