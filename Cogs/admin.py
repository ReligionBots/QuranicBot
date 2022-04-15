import os
import json
import discord
import requests as req
# import http.client
from discord.ext import tasks, commands
from Utils import utils as ut
# from dotenv import load_dotenv


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def handleEmbed(self, title, error):
        return discord.Embed(title=title, description=error, color=0xFFBA01)
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        response = ut.prefixCreation(ctx, prefix)
        if response['status'] == 1:
            self.bot = response['data']
            await ctx.send(embed=self.handleEmbed(f"", f"Prefix updated successfully."))
        elif response['status'] == 2:
            self.bot = response['data']
            await ctx.send(embed=self.handleEmbed(f"", f"The old and the new prefix are the same"))
        else:
            await ctx.send(embed=self.handleEmbed(f"", response['data']))



def setup(bot):
    bot.add_cog(Admin(bot))
