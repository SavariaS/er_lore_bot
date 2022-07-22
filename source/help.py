# Third party library imports
import discord

# @brief Constructs and returns an embed containing the list of all commands
# @return The embed
def show_help():
    help_embed = discord.Embed(title = "Commands", description = "", type = "rich")                                  
    help_embed.add_field(name = "!help", value = "Displays the list of all commands.", inline = False)                                        
    help_embed.add_field(name = "!help <command>", value = "Displays information about a command.", inline = False)
    help_embed.add_field(name = "!tags", value = "Displays the list of all tags.", inline = False)  
    help_embed.add_field(name = "!item-name <tags> : <name>", value = "Finds an item by its name.", inline = False)                       
    help_embed.add_field(name = "!item-desc <tags> : <description>", value = "Finds an item by its description.", inline = False)              
    help_embed.add_field(name = "!dialogue <author> : <lines>", value = "Finds a block of dialogue.", inline = False)                 
    help_embed.add_field(name = "!item-name-jp <tags> : <name>", value = "Finds an item in Japanese by name.", inline = False);        
    help_embed.add_field(name = "!dialogue-jp <author> : <lines>", value = "Finds a block of dialogue in Japanese.", inline = False)  
    help_embed.add_field(name = "!translate <text>", value = "Translates text to English.", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !help command
# @return The embed
def show_help_command():
    help_embed = discord.Embed(title = "!help / !help <command>", description = "Displays the list of all commands or displays information about a command.", type = "rich")
    help_embed.add_field(name = "<command>", value = "The name of the command.", inline = False)
    help_embed.add_field(name = "Example:", value = "!help item-desc", inline = False)

    return help_embed
# @brief Constructs and returns an embed containing information about the !tags command
# @return The embed

def show_tags():
    help_embed = discord.Embed(title = "!tags", description = "Displays the list of all tags.", type = "rich")

    return help_embed

# @brief Constructs and returns an embed containing information about the !item-name command
# @return The embed
def show_item_name():
    help_embed = discord.Embed(title = "!item-name <tags> : <name>", description = "Finds an item by its name.", type = "rich")
    help_embed.add_field(name = "<tags> (Optional)", value = "Tags associated with the item.", inline = False)
    help_embed.add_field(name = "<name>", value = "Keywords to be found in the item's name.", inline = False)
    help_embed.add_field(name = "Example:", value = "!item-name key : map snowfield", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !item-desc command
# @return The embed
def show_item_desc():
    help_embed = discord.Embed(title = "!item-desc <tags> : <description>", description = "Finds an item by its description.", type = "rich")
    help_embed.add_field(name = "<tags> (Optional)", value = "Tags associated with the item.", inline = False)
    help_embed.add_field(name = "<description>", value = "Keywords to be found in the item's description.", inline = False)
    help_embed.add_field(name = "Example:", value = "!item-desc incantation : malenia true goddess", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !dialogue command
# @return The embed
def show_dialogue():
    help_embed = discord.Embed(title = "!dialogue <author> : <lines>", description = "Finds a block of dialogue.", type = "rich")
    help_embed.add_field(name = "<author> (Optional)", value = "The source of the dialogue.", inline = False)
    help_embed.add_field(name = "<lines>", value = "Keywords to be found within the block of dialogue.", inline = False)
    help_embed.add_field(name = "Example:", value = "!dialogue melina : destined death", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !item-name-jp command
# @return The embed
def show_item_name_jp():
    help_embed = discord.Embed(title = "!item-name-jp <tags> : <name>", description = "Finds an item in Japanese by its name.", type = "rich")
    help_embed.add_field(name = "<tags> (Optional)", value = "Tags associated with the item.", inline = False)
    help_embed.add_field(name = "<name>", value = "English keywords to be found in the item's name.", inline = False)
    help_embed.add_field(name = "Example:", value = "!item-name-jp scarlet aeonia", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !dialogue-jp command
# @return The embed
def show_dialogue_jp():
    help_embed = discord.Embed(title = "!dialogue-jp <author> : <lines>", description = "Finds a block of dialogue in Japanese.", type = "rich")
    help_embed.add_field(name = "<author> (Optional)", value = "The source of the dialogue.", inline = False)
    help_embed.add_field(name = "<lines>", value = "English keywords to be found within the block of dialogue.", inline = False)
    help_embed.add_field(name = "Example:", value = "!dialogue-jp melina : destined death", inline = False)

    return help_embed

# @brief Constructs and returns an embed containing information about the !translate command
# @return The embed
def show_translate():
    help_embed = discord.Embed(title = "!translate <text>", description = "Translates text to English.", type = "rich")
    help_embed.add_field(name = "<text>", value = "The text to translate to English. Can be in any language.", inline = False)
    help_embed.add_field(name = "Example:", value = "!translate 三度目に、きっと彼女は女神となる", inline = False)

    return help_embed

# @brief Return information about the specificed command
# @param args The name of the command
# @return An embed containing the list of all commands if no command was specified or help about the specificed command or an error message.
def help(args):
    # Format the argument
    command = args.strip()

    # If no command was specificed, return the list of all commands
    if(command == ""):
        return show_help()

    # If a command was given, return information about it or an error message if it could not be found
    else:
        if(command == "help" or command == "!help"):
            return show_help_command()
        elif(command == "item-name" or command == "!item-name"):
            return show_item_name()
        elif(command == "tags" or command == "!tags"):
            return show_tags()
        elif(command == "item-desc" or command == "!item-desc"):
            return show_item_desc()
        elif(command == "dialogue" or command == "!dialogue"):
            return show_dialogue()
        elif(command == "item-name-jp" or command == "!item-name-jp"):
            return show_item_name_jp()
        elif(command == "dialogue-jp" or command == "!dialogue-jp"):
            return show_dialogue_jp()
        elif(command == "translate" or command == "!translate"):
            return show_translate()
        else:
            error_embed = discord.Embed(title = "Error", type = "rich", colour = 0xFF0000)
            error_embed.description = "No command known as '{argument}'.".format(argument = command)
            return error_embed