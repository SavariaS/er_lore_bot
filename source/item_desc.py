# Third party library imports
import discord
from bs4 import BeautifulSoup

# Local imports
from utils import path, simplify, contains_keywords

# Function definitions

# @brief Generates the path to a data file
# @param name            The beginning of the name of the file
#        is_description  True if it's a file containing descriptions, False if it's a file containing names
#        is_japanese     True if it's a japanese file, False if not
# @return The path to the file
def file_path(name, is_description, is_tags, is_japanese):
    path = "../data/"
    path += name
    path += "Caption" if is_description else "Tags" if is_tags else "Name"
    path += "Stripped"
    path += "JP" if is_japanese else ""
    path += ".xml"

    return path

# @brief Generates a list of files from the tags
# @param tags                  A list of tags
#        is_description_first  True if the descriptions file should be first, False if not
#        is_japanese           True if description should be in japanese
# @return A list of files to search through
def get_files_list(tags, is_description_first, is_japanese):
    files_list = []

    if(not tags or "talisman" in tags):
        files_list.append([file_path("Accessory", is_description_first, False, False), file_path("Accessory", not is_description_first, False, is_japanese), file_path("Accessory", False, True, False)])
    if(not tags or "armor" in tags):
        files_list.append([file_path("Protector", is_description_first, False, False), file_path("Protector", not is_description_first, False, is_japanese), file_path("Protector", False, True, False)])
    if(not tags or "weapon" in tags or "catalyst" in tags or "shield" in tags or "ammunition" in tags):
        files_list.append([file_path("Weapon", is_description_first, False, False), file_path("Weapon", not is_description_first, False, is_japanese), file_path("Weapon", False, True, False)])
    if(not tags or "sorcery" in tags or "incantation" in tags or "key" in tags or "ashes" in tags or "material" in tags or "consumable" in tags):
        files_list.append([file_path("Goods", is_description_first, False, False), file_path("Goods", not is_description_first, False, is_japanese), file_path("Goods", False, True, False)])

    return files_list

# @brief Finds the item in a file using the keywords. If the item is found, return the data found in both files
# @param keywords     A list of keywords to look for
#        src_file     A string containing the location of a XML file. One of the entries of that file must match the keywords
#        lookup_file  A string containing the location of another XML file. The corresponding entry in that file will be returned as data
#        data         An array containing two fields. One for the item name, the other for the item description
# @return The updated (or not) data
def find_keywords(keywords, tags, src_file, lookup_file, tag_file, item_list):
    # Parse the source file
    src_fd = open(path(src_file))
    src_soup = BeautifulSoup(src_fd, "xml")
    entries = src_soup.find("entries")

    # Parse the tags file
    tag_fd = open(path(tag_file))
    tag_soup = BeautifulSoup(tag_fd, "xml")

    # For each entry in the file
    for tag in entries.find_all("text"):
            # If the entry contains the keywords
            if(contains_keywords(simplify(tag.text), keywords)):
                # If the entry does not contain the tags, ignore it
                if(tags):
                    tag_list = tag_soup.find(attrs = {"id" : tag["id"]})
                    if(not contains_keywords(tag_list.text, tags)):
                        continue

                # Parse the second file and find the corresponding id
                lookup_fd = open(path(lookup_file))
                lookup_soup = BeautifulSoup(lookup_fd, "xml")
                match = lookup_soup.find(attrs = {"id" : tag["id"]})

                # Set data to the two entries found
                if(match):
                    item_list.append([tag.text, match.text])
        
    return item_list


# @brief Finds the description of an item.
# @param args  The description of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_by_description(args):
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
    
    # Get the list of files from the tags
    file_list = get_files_list(tags, is_description_first = True, is_japanese = False)

    # Search for the item in the files
    item_list = []
    for files in file_list:
        item_list = find_keywords(keywords, tags, files[0], files[1], files[2], item_list)
    
    # If no item was found, return an error message
    if(len(item_list) == 0):
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = args)
        return error_embed

    # If only one item was found, return it   
    if(len(item_list) == 1):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_list[0][1], type = "rich")
        item_embed.description = item_list[0][0]
        return item_embed

    # If more than one item was found, return a list
    if(len(item_list) > 1):
        if(len(item_list) <= 6):
            desc = ""
            for item in item_list:
                desc += item[1] + "\n"

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed
        else:
            desc = ""
            for i in range(5):
                desc += item_list[i][1] + "\n"
            desc += "... {} more items found.".format(len(item_list) - 5)

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed

# @brief Finds the description of an item by its name.
# @param args  The name of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_by_name(args):
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
    
    # Get the list of files from the tags
    file_list = get_files_list(tags, is_description_first = False, is_japanese = False)

    # Search for the item in the files
    item_list = []
    for files in file_list:
        item_list = find_keywords(keywords, tags, files[0], files[1], files[2], item_list)
    
    # If no item was found, return an error message
    if(len(item_list) == 0):
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = args)
        return error_embed

    # If only one item was found, return it   
    if(len(item_list) == 1):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_list[0][0], type = "rich")
        item_embed.description = item_list[0][1]
        return item_embed

    # If more than one item was found, return a list
    if(len(item_list) > 1):
        if(len(item_list) <= 6):
            desc = ""
            for item in item_list:
                desc += item[0] + "\n"

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed
        else:
            desc = ""
            for i in range(5):
                desc += item_list[i][0] + "\n"
            desc += "... {} more items found.".format(len(item_list) - 5)

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed


# @brief Finds the japanese description of an item by its name.
# @param args  The name of the item to search for. Used as keywords to facilitate the search
# @return An embed to be displayed. The item's name and description if it was found, else an error message
def find_item_by_name_jp(args):
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
    
    # Get the list of files from the tags
    file_list = get_files_list(tags, is_description_first = False, is_japanese = True)

    # Search for the item in the files
    item_list = []
    for files in file_list:
        item_list = find_keywords(keywords, tags, files[0], files[1], files[2], item_list)

    # If no item was found, return an error message
    if(len(item_list) == 0):
        error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
        error_embed.description = "No item matching '{arguments}' was found.".format(arguments = args)
        return error_embed

    # If only one item was found, return it   
    if(len(item_list) == 1):
        # Create an embed for the item
        item_embed = discord.Embed(title = item_list[0][0], type = "rich")
        item_embed.description = item_list[0][1]
        return item_embed

    # If more than one item was found, return a list
    if(len(item_list) > 1):
        if(len(item_list) <= 6):
            desc = ""
            for item in item_list:
                desc += item[0] + "\n"

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed
        else:
            desc = ""
            for i in range(5):
                desc += item_list[i][0] + "\n"
            desc += "... {} more items found.".format(len(item_list) - 5)

            item_embed = discord.Embed(title = "Disambiguation", type = "rich", colour = 0xFFFF00)
            item_embed.description = desc
            return item_embed