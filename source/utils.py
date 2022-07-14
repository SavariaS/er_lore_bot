# Standard library imports
import os

# Globals
directory = os.path.dirname(__file__)

# @brief Converts a path relative to the current working directory into a path relative to the source file
# @param string The path relative to the current working directory
# @return The path relative to this file
def path(relative_path):
    return os.path.join(directory, relative_path)

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
        alternative = ""
        # If the keyword is plural, get the singular variant
        if(word[-1] == "s"):
            alternative = word[:-1]
        # If the keyword is singular, get the plural variant
        else:
            alternative = word + "s"

        # If either form is missing...
        if((word in words) == False and (alternative in words) == False):
            return False
    
    # Else, return true
    return True