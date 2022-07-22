# Includes
import discord
# Third party library imports
import discord
from bs4 import BeautifulSoup

# Local imports
from utils import path, simplify, contains_keywords

# @brief Finds a block of dialogue from keywords.
# @param dialogue Keywords to look for.
# @return An embed with the dialogue and its source, or an error message if the dialogue was not found
def find_dialogue(args):
    # Local variables
    tags = []
    keywords = []

    # If there is a delimiter...
    if(args.find(":") != -1):
        # Separate the string and store the tags and keywords in lists
        tags = simplify(args.split(':')[0]).split()
        keywords = simplify(args.split(':')[1]).split()
    else:
        # Ignore tags
        tags = []
        keywords = simplify(args).split()

    # Open the dialogues file and prase it
    dialogues_fd = open(path("../data/TalkMsgStripped.xml"))
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
                character_id = (section - (section % 100000)) if section < 100000000 else (section - (section % 1000000))

                author_fd = open(path("../data/TalkAuthor.xml"))
                author_soup = BeautifulSoup(author_fd, "xml")
                author = author_soup.find(attrs = {"id" : str(character_id)})

                # If the tags correspond to the author
                if((not tags) or (tags and author and contains_keywords(simplify(author.text), tags))):
                    # Construct the embed
                    if author and author.text:
                        item_embed = discord.Embed(title = author.text, type = "rich")
                        item_embed.description = text
                    else:
                        item_embed = discord.Embed(title = "Unknown", type = "rich")
                        item_embed.description = text

                    return item_embed
            
            # If it was not found, move on to the next section
            section = id - (id % 100) if id < 10000 else id - (id % 1000)
            text = tag.text + "\n"
    
    # If the dialogue wasn't found, return an error
    error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
    error_embed.description = "No dialogue matching '{arguments}' was found.".format(arguments = args)
    return error_embed

# @brief Finds a block of dialogue in japanese from keywords.
# @param dialogue Keywords to look for.
# @return An embed with the dialogue and its source, or an error message if the dialogue was not found
def find_dialogue_jp(args):
    # Local variables
    tags = []
    keywords = []

    # If there is a delimiter...
    if(args.find(":") != -1):
        # Separate the string and store the tags and keywords in lists
        tags = simplify(args.split(':')[0]).split()
        keywords = simplify(args.split(':')[1]).split()
    else:
        # Ignore tags
        tags = []
        keywords = simplify(args).split()

    # Open the dialogues file and prase it
    dialogues_fd = open(path("../data/TalkMsgStripped.xml"))
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
                author_fd = open(path("../data/TalkAuthor.xml"))
                author_soup = BeautifulSoup(author_fd, "xml")
                author = author_soup.find(attrs = {"id" : str(section)})

                # If the tags correspond to the author
                if((not tags) or (tags and author and contains_keywords(simplify(author.text), tags))):
                    # Get the japanese version
                    japanese_fd = open(path("../data/TalkMsgStrippedJP.xml"))
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
                    if author and author.text:
                        item_embed = discord.Embed(title = author.text, type = "rich")
                        item_embed.description = jp_text
                    else:
                        item_embed = discord.Embed(title = "Unknown", type = "rich")
                        item_embed.description = jp_text

                    return item_embed
            
            # If it was not found, move on to the next section
            section = id
            text = tag.text + "\n"
    
    # If the dialogue wasn't found, return an error
    error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
    error_embed.description = "No dialogue matching '{arguments}' was found.".format(arguments = args)
    return error_embed


