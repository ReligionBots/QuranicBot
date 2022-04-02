import os
import json
import discord
from discord.ext import tasks, commands
from Utils import utilFunctions as ut
# from dotenv import load_dotenv


class Philosophy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Philosophy(bot))
