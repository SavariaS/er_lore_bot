# Includes
import discord
from bs4 import BeautifulSoup

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

# @brief Finds the description of an item.
# @param item  The name of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_description(item):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(item).split()

    # Create an embed for the item
    item_embed = discord.Embed(title = "NULL", type = "rich")

    # Find the item using the keywords
    item_embed = find_keywords(keywords, "../data/AccessoryNameStripped.xml", "../data/AccessoryCaptionStripped.xml", item_embed)
    item_embed = find_keywords(keywords, "../data/ArtsNameStripped.xml",      "../data/ArtsCaptionStripped.xml", item_embed)
    item_embed = find_keywords(keywords, "../data/GoodsNameStripped.xml",     "../data/GoodsCaptionStripped.xml", item_embed)
    item_embed = find_keywords(keywords, "../data/ProtectorNameStripped.xml", "../data/ProtectorCaptionStripped.xml", item_embed)
    item_embed = find_keywords(keywords, "../data/WeaponNameStripped.xml",    "../data/WeaponCaptionStripped.xml", item_embed)

    # If an item was found, return it
    if(item_embed.title != "NULL"):
        return item_embed
    
    # If no item was found, return an error message
    else:
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = item)
        return error_embed
