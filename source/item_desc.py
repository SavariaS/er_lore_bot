# Third party library imports
import discord
from bs4 import BeautifulSoup

# Local imports
from utils import path, simplify, contains_keywords

# Function definitions

# @brief Finds the item in a file using the keywords. If the item is found, return the data found in both files
# @param keywords     A list of keywords to look for
#        src_file     A string containing the location of a XML file. One of the entries of that file must match the keywords
#        lookup_file  A string containing the location of another XML file. The corresponding entry in that file will be returned as data
#        data         An array containing two fields. One for the item name, the other for the item description
# @return The updated (or not) data
def find_keywords(keywords, src_file, lookup_file, data):
    # If the item has not been found yet
    if(data[0] == "NULL"):
        # Parse the first file
        src_fd = open(path(src_file))
        src_soup = BeautifulSoup(src_fd, "xml")
        entries = src_soup.find("entries")

        # For each entry in the file
        for tag in entries.find_all("text"):
                # If the entry contains the keywords
                if(contains_keywords(simplify(tag.text), keywords)):
                    # Parse the second file and find the corresponding id
                    lookup_fd = open(path(lookup_file))
                    lookup_soup = BeautifulSoup(lookup_fd, "xml")
                    match = lookup_soup.find(attrs = {"id" : tag["id"]})

                    # Set data to the two entries found
                    data[0] = tag.text
                    data[1] = match.text

                    # Exit
                    break
        
    return data

def find_item_by_description(item):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(item).split()

    # Create an array to hold the item data
    item_data = ["NULL", "NULL"]

    # Find the item using the keywords
    item_embed = find_keywords(keywords, "../data/AccessoryCaptionStripped.xml", "../data/AccessoryNameStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ArtsCaptionStripped.xml",      "../data/ArtsNameStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/GoodsCaptionStripped.xml",     "../data/GoodsNameStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ProtectorCaptionStripped.xml", "../data/ProtectorNameStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/WeaponCaptionStripped.xml",    "../data/WeaponNameStripped.xml", item_data)

    # If an item was found, return it
    if(item_data[0] != "NULL"):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_data[1], type = "rich")
        item_embed.description = item_data[0]
        return item_embed
    
    # If no item was found, return an error message
    else:
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = item)
        return error_embed

# @brief Finds the description of an item.
# @param item  The name of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_by_name(item):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(item).split()

    # Create an array to hold the item data
    item_data = ["NULL", "NULL"]

    # Find the item using the keywords
    item_embed = find_keywords(keywords, "../data/AccessoryNameStripped.xml", "../data/AccessoryCaptionStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ArtsNameStripped.xml",      "../data/ArtsCaptionStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/GoodsNameStripped.xml",     "../data/GoodsCaptionStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ProtectorNameStripped.xml", "../data/ProtectorCaptionStripped.xml", item_data)
    item_embed = find_keywords(keywords, "../data/WeaponNameStripped.xml",    "../data/WeaponCaptionStripped.xml", item_data)

    # If an item was found, return it
    if(item_data[0] != "NULL"):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_data[0], type = "rich")
        item_embed.description = item_data[1]
        return item_embed
    
    # If no item was found, return an error message
    else:
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = item)
        return error_embed


# @brief Finds the japanese description of an item.
# @param item  The name of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_by_name_jp(item):
    # Store all the arguments in a list (after simpliying them)
    keywords = simplify(item).split()

    # Create an array to hold the item data
    item_data = ["NULL", "NULL"]

    # Find the item using the keywords
    item_embed = find_keywords(keywords, "../data/AccessoryNameStripped.xml", "../data/AccessoryCaptionStrippedJP.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ArtsNameStripped.xml",      "../data/ArtsCaptionStrippedJP.xml", item_data)
    item_embed = find_keywords(keywords, "../data/GoodsNameStripped.xml",     "../data/GoodsCaptionStrippedJP.xml", item_data)
    item_embed = find_keywords(keywords, "../data/ProtectorNameStripped.xml", "../data/ProtectorCaptionStrippedJP.xml", item_data)
    item_embed = find_keywords(keywords, "../data/WeaponNameStripped.xml",    "../data/WeaponCaptionStrippedJP.xml", item_data)

    # If an item was found, return it
    if(item_data[0] != "NULL"):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_data[0], type = "rich")
        item_embed.description = item_data[1]
        return item_embed
    
    # If no item was found, return an error message
    else:
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = item)
        return error_embed