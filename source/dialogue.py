# Includes
import os
import discord
from bs4 import BeautifulSoup

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

    string = string.replace("'s", "")

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

# @brief Finds a block of dialogue from keywords.
# @param dialogue Keywords to look for.
# @return An embed with the dialogue and its source, or an error message if the dialogue was not found
def find_dialogue(dialogue):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(dialogue).split()

    # Open the dialogues file and prase it
    dialogues_fd = open("../data/TalkMsgStripped.xml")
    dialogues_soup = BeautifulSoup(dialogues_fd, "xml")
    entries = dialogues_soup.find("entries")

    # Variables
    section = 1000
    text = "" 

    # For each entry
    for tag in entries.find_all("text"):
        # Get the tag's id
        id = int(tag["id"])

        # If the tag belongs to the same section, add it to the text and continue
        if((section < 10000 and ((id - (id % 100)) == section)) or
           (section >= 10000 and ((id - (id % 1000)) == section))):
            text += tag.text + "\n"
            continue

        # If the tag does not belong to the same section, check if the dialogue was found
        else:
            # If the dialogue was found, return it
            if(contains_keywords(simplify(text), keywords)):
                # Get the author
                author_fd = open("../data/TalkAuthor.xml")
                author_soup = BeautifulSoup(author_fd, "xml")
                author = author_soup.find(attrs = {"id" : str(section)})

                # Construct the embed
                if author is None:
                    item_embed = discord.Embed(title = "Unknown", type = "rich")
                    item_embed.description = text
                else:
                    item_embed = discord.Embed(title = author.text, type = "rich")
                    item_embed.description = text

                return item_embed
            
            # If it was not found, move on to the next section
            else:
                section = id
                text = tag.text + "\n"
    
    # If the dialogue wasn't found, return an error
    error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
    error_embed.description = "No dialogue matching '{arguments}' was found.".format(arguments = dialogue)
    return error_embed

# @brief Finds a block of dialogue in japanese from keywords.
# @param dialogue Keywords to look for.
# @return An embed with the dialogue and its source, or an error message if the dialogue was not found
def find_dialogue_jp(dialogue):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(dialogue).split()

    # Open the dialogues file and prase it
    dialogues_fd = open("../data/TalkMsgStripped.xml")
    dialogues_soup = BeautifulSoup(dialogues_fd, "xml")
    entries = dialogues_soup.find("entries")

    # Variables
    section = 1000
    text = "" 

    # For each entry
    for tag in entries.find_all("text"):
        # Get the tag's id
        id = int(tag["id"])

        # If the tag belongs to the same section, add it to the text and continue
        if((section < 10000 and ((id - (id % 100)) == section)) or
           (section >= 10000 and ((id - (id % 1000)) == section))):
            text += tag.text + "\n"
            continue

        # If the tag does not belong to the same section, check if the dialogue was found
        else:
            # If the dialogue was found, return it
            if(contains_keywords(simplify(text), keywords)):
                # Get the author
                author_fd = open("../data/TalkAuthor.xml")
                author_soup = BeautifulSoup(author_fd, "xml")
                author = author_soup.find(attrs = {"id" : str(section)})

                # Get the japanese version
                japanese_fd = open("../data/TalkMsgStrippedJP.xml")
                japanese_soup = BeautifulSoup(japanese_fd, "xml")
                start = japanese_soup.find(attrs = {"id" : str(section)})

                jp_text = ""
                jp_id = int(start["id"])

                # For each tag in the same section
                while ((section < 10000 and ((jp_id - (jp_id % 100)) == section)) or
                       (section >= 10000 and ((jp_id - (jp_id % 1000)) == section))):
                    jp_text += start.text + "\n"
                    start = start.find_next_sibling("text")
                    jp_id = int(start["id"])
                
                # Construct the embed
                if author is None:
                    item_embed = discord.Embed(title = "Unknown", type = "rich")
                    item_embed.description = jp_text
                else:
                    item_embed = discord.Embed(title = author.text, type = "rich")
                    item_embed.description = jp_text

                return item_embed
            
            # If it was not found, move on to the next section
            else:
                section = id
                text = tag.text + "\n"
    
    # If the dialogue wasn't found, return an error
    error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
    error_embed.description = "No dialogue matching '{arguments}' was found.".format(arguments = dialogue)
    return error_embed


