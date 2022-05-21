# References
# https://discordpy.readthedocs.io/en/stable/api.html#message
# https://discordpy.readthedocs.io/en/stable/api.html#embed

# Includes
import os
import discord
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Globals
client = discord.Client() # Client object

help_embed = discord.Embed(title = 'Commands', description = '', type = 'rich')                           # Help message
help_embed.add_field(name = '!help', value = 'Displays commands', inline = False)                         #
help_embed.add_field(name = '!item-desc <item>', value = 'Displays an item description', inline = False); #

error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000) # Error message

# Function definitions

# @brief Simplifies a string by converting it to lowercase, removing undiserable characters and replacing french accents with the english alphabet
# @param string The string to modify
# @return The simplified string
def simplify(string):
    # Converts all characters to lowercase
    string = string.lower()

    # Remove characters
    string = string.translate(str.maketrans('', '', '.,:()'))

    # Replace french accents with ASCII character
    string = string.replace("é", "e")
    string = string.replace("è", "e")

    return string

# @brief Checks if ALL keywords are present in a line
# @param line     A string containing the line (name of an item)
#        keywords A list of keywords to look for
# @return True if ALL the keywords were found in the line, false otherwise
def contains_keywords(line, keywords):
    # Store the words of the line in a list
    words = line.split()

    # If a keyword is missing from the line, return false
    for word in keywords:
        if((word in words) == False):
            return False
    
    # Else, return true
    return True

# @brief Finds the item using the keywords in the file of item names. If the item is found, 
#        extract the description at the corresponding 'id' in the descriptions file and store
#        the item's information in the embed
# @param keywords          A list of keywords to look for
#        names_file        A string containing the location of the file of names
#        descriptions_file A string containing the location of the file of descriptions
#        embed             An embed to store the item's information 
# @return The updated (or not) embed
def find_keywords(keywords, names_file, descriptions_file, embed):
    # If the item has not been found yet
    if(embed.title == "NULL"):
        # Parse the names file
        names_fd = open(names_file)
        names_soup = BeautifulSoup(names_fd, "xml")
        entries = names_soup.find("entries")

        # For each entry in the name file
        for tag in entries.contents:
                # If the entry contains the keywords
                if(contains_keywords(simplify(tag.text), keywords)):
                    # Parse the descriptions file and find the corresponding id
                    desc_fd = open(descriptions_file)
                    desc_soup = BeautifulSoup(desc_fd, "xml")
                    desc = desc_soup.find(attrs = {"id" : tag["id"]})

                    # Set the name and description of the item
                    embed.title = tag.text
                    embed.description = desc.text

                    # Exit
                    break
        
    return embed


# @brief Callback when a message is sent in a channel the bot has access to
# @param message The message (discord.py message)
@client.event
async def on_message(message):
    # If the bot is the author of the message, ignore it
    if message.author == client.user:
        return

    # If the !help command is entered, show help message
    if((len(message.content) == 5 and message.content[:5] == '!help') or 
        len(message.content) >= 6 and message.content[:6] == '!help '):
        await message.channel.send(embed = help_embed)
    
    # If the !item-desc command is entered...
    elif(len(message.content) >= 11 and message.content[:11] == '!item-desc '):
        # Store all the arguments in a list (after simpliying them)
        keywords = simplify(message.content[11:]).split()

        # Create an embed for the item
        item_embed = discord.Embed(title = "NULL", type = "rich")

        # Find the item using the keywords
        item_embed = find_keywords(keywords, "data/AccessoryNameStripped.fmg.xml", "data/AccessoryCaptionStripped.fmg.xml", item_embed)
        item_embed = find_keywords(keywords, "data/ArtsNameStripped.fmg.xml",      "data/ArtsCaptionStripped.fmg.xml", item_embed)
        item_embed = find_keywords(keywords, "data/GoodsNameStripped.fmg.xml",     "data/GoodsCaptionStripped.fmg.xml", item_embed)
        item_embed = find_keywords(keywords, "data/WeaponNameStripped.fmg.xml",    "data/WeaponCaptionStripped.fmg.xml", item_embed)

        # If an item was found, show it
        if(item_embed.title != "NULL"):
            await message.channel.send(embed = item_embed)
        
        # If no item was found, return an error message
        else:
            error_embed.description = "No item matching '{arguments}' was found.".format(arguments = message.content[11:])
            await message.channel.send(embed = error_embed)

    # If the command is unknown
    elif(message.content[0] == "!"):
        error_embed.description = "'{arguments}' : command not found.\nUse !help for a list of all commands.".format(arguments = message.content.split()[0])
        await message.channel.send(embed = error_embed)



# @brief Callback when the bot is connected and ready
@client.event
async def on_ready():
    print("Ready.")

# Main
# Load token and start the bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)