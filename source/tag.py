# Third party library imports
import discord

# Globals
type_list = "Key\n\
Sorcery\n\
Incantation\n\
Weapon\n\
Shield\n\
Staff\n\
Catalyst\n\
Armor\n\
Talisman\n\
Consumable\n\
Upgrade\n\
Ammunition\n"

# @brief Constructs and returns an embed containing the list of all tags
# @return The embed
def show_tags():
    embed = discord.Embed(title = "Tags", description = "", type = "rich")
    embed.add_field(name = "Type", value = type_list, inline = True)

    return embed