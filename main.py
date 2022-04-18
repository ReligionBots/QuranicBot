import os
import json
import discord
from Utils import utils as ut
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# here we are opeing the extensions file to get the extension details
ext_data = ut.readJSON(ut.directory['extJSON'])

    
# we make the bot and put the prefix
bot = commands.Bot(command_prefix=ut.get_prefix_1, activity = discord.Game(name=f"Use ~help to get commands info"))
bot.remove_command("help") # for removing the main help command


# main function for loading other extensions
def main():     
    # Assigning main extensions
    extensions = ext_data['extensions']
    # we go through each extension that we have of the cogs and load them
    for extension in extensions:
        ext = extension['extension']
        try:
            if os.path.exists("./QuranicBot"):
                for folder in os.listdir("QuranicBot"):
                    if os.path.exists(os.path.join("QuranicBot",folder, ext+".py")):
                        bot.load_extension(f"QuranicBot.{folder}.{ext}")
                    else:
                        bot.load_extension(f"Cogs.{ext}")
            else:
                bot.load_extension(f"Cogs.{ext}")
        except Exception as errors:
            print(f'{errors}')
    
    bot.run(TOKEN)            



if __name__ == '__main__':
    main()



