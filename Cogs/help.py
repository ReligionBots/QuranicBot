import os
import json
import discord
import requests as req
import http.client
from discord.ext import tasks, commands
from Utils import utils as ut
# from dotenv import load_dotenv


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        check_mark = '✅'
        prefix = ut.get_prefix(message)
        string_1, string_2 = f"{prefix}tQuran", f"{prefix}Quran"
        msg = message.content
        if msg.startswith(string_1) or msg.startswith(string_2):
            await message.add_reaction(check_mark)



def setup(bot):
    bot.add_cog(Help(bot))
