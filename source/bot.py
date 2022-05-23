# References
# https://discordpy.readthedocs.io/en/stable/api.html#message
# https://discordpy.readthedocs.io/en/stable/api.html#embed

# Library imports
import os
import discord
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Local imports
from item_desc import find_item_description
from dialogue import find_dialogue
from translate import translate

# Globals
client = discord.Client() # Client object

help_embed = discord.Embed(title = "Commands", description = "", type = "rich")                           # Help message
help_embed.add_field(name = "!help", value = "Displays commands", inline = False)                         #
help_embed.add_field(name = "!item-desc <item>", value = "Displays an item description", inline = False); #
help_embed.add_field(name = "!dialogue <lines>", value = "Displays a block of dialogue", inline = False)
help_embed.add_field(name = "!translate <text>", value = "Translates text to english", inline = False);   #

# Function definitions

# @brief Callback when the bot is connected and ready
@client.event
async def on_ready():
    print("Ready.")

# @brief Callback when a message is sent in a channel the bot has access to
# @param message The message (discord.py message)
@client.event
async def on_message(message):
    # If the bot is the author of the message, ignore it
    if message.author == client.user:
        return

    # If the !help command is entered, show help message
    if((len(message.content) == 5 and message.content[:5] == "!help") or 
        len(message.content) >= 6 and message.content[:6] == "!help "):
        await message.channel.send(embed = help_embed)
        return
    
    # If the !item-desc command is entered...
    elif(len(message.content) >= 11 and message.content[:11] == "!item-desc "):
        embed = find_item_description(message.content[11:])
        await message.channel.send(embed = embed)
        return

    # If the !dialogue command is entered...
    elif(len(message.content) >= 10 and message.content[:10] == "!dialogue "):
        embed = find_dialogue(message.content[10:])
        await message.channel.send(embed = embed)
        return
    
    # If the !translate command is entered
    elif(len(message.content) >= 11 and message.content[:11] == "!translate "):
        embed = translate("en", message.content[11:])
        await message.channel.send(embed = embed)
        return

    # If the command is unknown
    elif(message.content[0] == "!"):
        # Return an error message
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "'{arguments}' : command not found.\nUse !help for a list of all commands.".format(arguments = message.content.split()[0])
        await message.channel.send(embed = error_embed)
        return

# Main
# Load token and start the bot
load_dotenv("../config/.env")
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)