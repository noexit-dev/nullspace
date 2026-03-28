# NULLSPACE

A tool to integrate RSS feeds to discord.

> [!WARNING] 
> This bot is not hosted anywhere and is not on the public appstore due to this being my first bot project and not willing to spend the resources to keep it up. Although, you can install the bot yourself by referencing the [installation](#installation) steps below.

## Installation
- Clone this repository
- Install the dependencies listed in `requirements.txt` using pip (You may need to use a [virtual environment](https://docs.python.org/3/library/venv.html) to manage packages for this project)
- Make the bot in the [Discord Developer Portal](https://discord.com/developers/applications)
> [!NOTE]
> Ensure you have the right permissions to invite the bot to your server of choice.
>
> First, go to Applications->(Your bot)->Bot.
>
> Verify that it is a public bot and that Server Members Intent/Message Content Intent are enabled.
>
> Second go to Applications->(Your bot)->OAuth2.
> 
> Go to the OAuth2 URL generator and select Bot as the scope. Then select permissions Send Messages/Send Messages in Threads, Use Slash Commands, View Channels.
>
> It will then generate a link at the bottom (Please verify that this is a guild install). Use this link to invite your bot to the server of your choice.

- Make sure you grab the bot token (located in the bot tab in the portal) as well.
- In the cloned repository, create a .env file and store your token in the following format:
```.env
DISCORD_TOKEN = "<Your bot's discord token>"
```

- Then that should be everything to get it up and running <3

## Usage

- To run the bot use the following command:

```python
python nullspace.py
```

- It should connect to discord using the token you provided and should wake your bot up in the server

## Commands

### /set-url
Sets the RSS to parse from using a valid RSS URL

### /rss-headlines
Displays the top 5 headlines of chosen RSS with embedded links

### /test
Tests to make sure that bot and slash commands are working
