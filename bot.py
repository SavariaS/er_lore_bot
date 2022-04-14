# References
# https://discordpy.readthedocs.io/en/stable/api.html#message
# https://discordpy.readthedocs.io/en/stable/api.html#embed

# Includes (imports?)
import os
import re
import discord
from dotenv import load_dotenv

# Globals
client = discord.Client() # Client object

tag_re = re.compile('<.*?>') # Regular expression for finding HTML tags

help_embed = discord.Embed(title = 'Commands', description = '', type = 'rich')                           # Help message
help_embed.add_field(name = '!help', value = 'Displays commands', inline = False)                         #
help_embed.add_field(name = '!item-desc <item>', value = 'Displays an item description', inline = False); #

error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000) # Error message

item_embed = discord.Embed(type = "rich") # Embed for item name and description

# Function definitions

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

# @brief Removes HTML tags and certain characters from a string
# @param string The string to modify
# @return The modified string, with all the HTML tags, numbers and square brackets removed
def remove_tags(string):
    # Convert HTML tags to ASCII characters
    string = string.replace("</p>", "\n")

    # Remove HTML tags
    string = re.sub(tag_re, "", string)

    # Remove brackets and digits
    string = string.translate(str.maketrans('', '', '[0123456789]'))

    return string

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
    if(len(message.content) >= 11 and message.content[:11] == '!item-desc '):
        # Store all the arguments in a list (after simpliying them)
        keywords = simplify(message.content[11:]).split()

        # Open the string dump
        file = open("string_dump.html")

        # For each line in the dump...
        for line in file:
            # If the line is a header
            if("<h3>" in line):
                # Format it
                line = remove_tags(line)

                # If the line contains all the arguments
                if(contains_keywords(simplify(line), keywords)):
                    description = ""

                    # For each line until the next header...
                    while(True):
                        l = file.readline()
                        if(l[:4] == "<h3>"):
                            break
                        
                        # Format it and add it to the description
                        description += remove_tags(l)
                    
                    # Set the name and description of the item
                    item_embed.title = line
                    item_embed.description = description

                    # Display the item
                    await message.channel.send(embed = item_embed)

                    # Exit
                    return
        
        # If no line matches the arguments, return an error message
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = message.content[11:])
        await message.channel.send(embed = error_embed)


# @brief Callback when the bot is connected and ready
# Do interprated languages have a preprocessor?
#@client.event
#async def on_ready():
#    print('Ready')

# Main

# Load token and start the bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)