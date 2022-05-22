# Elden Ring Lore Helper
This is a [Discord](https://discord.com/) bot that brings up Elden Ring item descriptions on demand. Contributions of any kind (new features, code improvements, more resources or improvements to the repository) are welcome.

## Usage
`!help` for the list of commands.

`!item-desc <item>` to lookup the description of an item.

`!translate <text>` to translate a string.

## Hosting
1 - Set the `DISCORD_TOKEN` environment variable (in `.env`) to your token.

2 - Run the python script.
```shell
cd source
python bot.py
```
## Dependencies
The XML files come from AsteriskAmpersand's [Carian Archive](https://github.com/AsteriskAmpersand/Carian-Archive).

The Python API used is [discord.py](https://github.com/Rapptz/discord.py)

The XML parsed used is [BeautifulSoup4](https://github.com/wention/BeautifulSoup4)
