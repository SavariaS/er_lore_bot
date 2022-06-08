# References
# https://discordpy.readthedocs.io/en/stable/api.html#message
# https://discordpy.readthedocs.io/en/stable/api.html#embed

# Standard library imports
import os
import signal

# Third party library imports
import discord
import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Local imports
from utils import path
from help import help
from tag import show_tags
from item_desc import find_item_by_name, find_item_by_description, find_item_by_name_jp
from dialogue import find_dialogue, find_dialogue_jp
from translate import translate

# Globals
client = discord.Client() # Client object

# Function definitions

# @brief Callback when the bot is connected and ready
@client.event
async def on_ready():
    # Connect signal handlers
    client.loop.add_signal_handler(getattr(signal, "SIGINT"), lambda: asyncio.create_task(on_signal()))
    client.loop.add_signal_handler(getattr(signal, "SIGTERM"), lambda: asyncio.create_task(on_signal()))
    print("Ready")

# @brief Callback when the SGINT (Unix) and SIGTERM signals are caught
async def on_signal():
    # Go offline and stop the client
    print("Shutting down")
    await client.change_presence(status = discord.Status.offline)
    await client.close()
    asyncio.get_event_loop().stop()

# @brief Callback when a message is sent in a channel the bot has access to
# @param message The message (discord.py message)
@client.event
async def on_message(message):
    # If the bot is the author of the message, ignore it
    if message.author == client.user:
        return

    # If the !help command is entered, show help message
    if(len(message.content) >= 5 and message.content[:5] == "!help"):
        embed = help(message.content[5:])
        await message.channel.send(embed = embed)
        return
    
    # If the !tags command is entered, show all tags
    if(len(message.content) >= 5 and message.content[:5] == "!tags"):
        embed = show_tags()
        await message.channel.send(embed = embed)
        return
    
    # If the !item-name command is entered...
    elif(len(message.content) >= 11 and message.content[:11] == "!item-name "):
        embed = find_item_by_name(message.content[11:])
        await message.channel.send(embed = embed)
        return
    
    # If the !item-desc command is entered...
    elif(len(message.content) >= 11 and message.content[:11] == "!item-desc "):
        embed = find_item_by_description(message.content[11:])
        await message.channel.send(embed = embed)
        return

    # If the !dialogue command is entered...
    elif(len(message.content) >= 10 and message.content[:10] == "!dialogue "):
        embed = find_dialogue(message.content[10:])
        await message.channel.send(embed = embed)
        return
    
    # If the !item-name-jp command is entered
    elif(len(message.content) >= 14 and message.content[:14] == "!item-name-jp "):
        embed = find_item_by_name_jp(message.content[14:])
        await message.channel.send(embed = embed)
        return
    
    # If the !dialogue-jp command is entered...
    elif(len(message.content) >= 13 and message.content[:13] == "!dialogue-jp "):
        embed = find_dialogue_jp(message.content[13:])
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
load_dotenv(path("../config/.env"))
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)