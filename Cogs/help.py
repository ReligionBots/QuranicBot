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


def setup(bot):
    bot.add_cog(Help(bot))
