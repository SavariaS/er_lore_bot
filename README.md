# Elden Ring Lore Helper
This is a [Discord](https://discord.com/) bot that brings up Elden Ring item descriptions on demand. Contributions of any kind (new features, code improvements, more resources or improvements to the repository) are welcome.

## Usage
`!help` for the list of commands.

`!item-name <item>` to lookup an item by name.

`!item-desc <item>` to lookup an item by description.

`!dialogue <lines>` to lookup a block of dialogue.

`!item-name-jp <item>` Same as !item-name but uses the Japanese files instead.

`!dialogue-jp <lines>` Same as !dialogue but uses the Japanese file instead.

`!translate <text>` to translate a string.

## Hosting
1 - Set the `DISCORD_TOKEN` environment variable (in `.env`) to your token.

2 - Set the `GOOGLE_API_KEY` environment variable (in `.env`) to your Google Cloud Translation API key (optional).

3 - Run the python script.
```shell
cd source
python bot.py
```

## Dependencies
The XML files come from AsteriskAmpersand's [Carian Archive](https://github.com/AsteriskAmpersand/Carian-Archive).

The Python API used is [discord.py](https://github.com/Rapptz/discord.py)

The XML parser used is [BeautifulSoup4](https://github.com/wention/BeautifulSoup4) with [lxml](https://github.com/lxml/lxml)

[python-dotenv](https://github.com/theskumar/python-dotenv) is also required.
