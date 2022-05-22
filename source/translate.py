# References
# https://cloud.google.com/translate/docs/reference/rest/v2/translate

# Includes
import os
import requests
import json

# @brief Translates a string into the target language
# @param target  The target language. Must be a language code compatible with the Google Clould Translation API
#        text    The string to translate
# @return The translated string
def translate(target, text):
    # Remove newlines
    text = text.replace("\n", " ")

    # Generate the URL from the API key, the target and source languages, and the text to translate
    url = "https://translation.googleapis.com/language/translate/v2?key={k}&target={t}&q={q}".format(k = os.getenv("GOOGLE_API_KEY"), t = target, q = text)

    # Call the API and convert the JSON received to a Python dictionnary
    response = json.loads(requests.post(url).text)

    # Return the translated text
    return response["data"]["translations"][0]["translatedText"]

