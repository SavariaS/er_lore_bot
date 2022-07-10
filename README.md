# Elden Ring Lore Helper
This is a [Discord](https://discord.com/) bot that brings up Elden Ring item descriptions on demand. Contributions of any kind (new features, code improvements, more resources or improvements to the repository) are welcome.

## Usage
`!help` Displays the list of all commands.

`!help <command>` Displays information about a command.

`!tags` Displays the list of all tags.

`!item-name <name>` Finds an item by its name.

`!item-desc <description>` Finds an item by its description.

`!dialogue <lines>` Finds a block of dialogue.

`!item-name-jp <name>` Finds an item in Japanese by name.

`!dialogue-jp <lines>` Finds a block of dialogue in Japanese.

`!translate <text>` Translates text to English.

## Hosting
1 - Set the `DISCORD_TOKEN` environment variable (in `.env`) to your token.

2 - Set the `GOOGLE_API_KEY` environment variable (in `.env`) to your Google Cloud Translation API key (optional).

3 - Run the python script.
```shell
cd source
python bot.py
```

## Dependencies
Tested with Python 3.8 and above.

The XML files come from AsteriskAmpersand's [Carian Archive](https://github.com/AsteriskAmpersand/Carian-Archive).

The Python API used is [discord.py](https://github.com/Rapptz/discord.py)

The XML parser used is [BeautifulSoup4](https://github.com/wention/BeautifulSoup4) with [lxml](https://github.com/lxml/lxml)

[python-dotenv](https://github.com/theskumar/python-dotenv) is also required.
