import os
import json
import discord
import requests as req
# import http.client
from discord.ext import tasks, commands
from Utils import utils as ut
# from dotenv import load_dotenv


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def handleEmbed(self, title, error):
        return discord.Embed(title=title, description=error, color=0xFFBA01)
    
    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        
        pass

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
