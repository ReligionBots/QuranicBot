import os
import json
import discord
from Utils import utils as ut
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# here we are opeing the extensions file to get the extension details
extData = ut.readJSON(ut.directory['extJSON'])
# here prefixes to write down the prefix we need, will be replaced later
dumData = ut.readJSON(ut.directory['prefixJSON'])
    
# we make the bot and put the prefix
bot = commands.Bot(command_prefix=ut.getPrefix)
bot.remove_command("help") # for removing the main help command



# main function for loading other extensions
def main():     
    # Assigning main extensions
    extensions = extData['extensions']
    # we go through each extension that we have of the cogs and load them
    for extension in extensions:
        ext = extension['extension']
        try:
            for folder in os.listdir("QuranicBot"):
                if os.path.exists(os.path.join("QuranicBot",folder, ext+".py")):
                    bot.load_extension(f"QuranicBot.{folder}.{ext}")
                else:
                    bot.load_extension(f"Cogs.{ext}")
        except Exception as errors:
            print(f'{ext} cannot be loaded. {errors}')
    
    bot.run(TOKEN)            



if __name__ == '__main__': 
    main()


