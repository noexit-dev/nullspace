import feedparser
import requests
import discord
import os
import time
from discord.ext import commands
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# port binding

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

#to keep hosting alive 24/7
def keep_alive():
    while True:
        #maybe use headless browser if this doesn't work

        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        url = '' #put url for site you want to keep active
        response = requests.get(url, headers=headers, timeout=15)

        time.sleep(840) #sleeps for 14 min and then visits site again to keep active


# Start the server in a separate thread so it doesn't block the bot
Thread(target=run).start()

#start website requester to keep website alive hopefully
# Thread(target=keep_alive).start()

# rss-parsing

entrylinkArr = []
url = ""
feed = ""

def rss_parse(arg):

    global url
    global feed

    url = arg

    # Reset cached links so repeated calls do not duplicate headlines.
    entrylinkArr.clear()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch the raw content with a custom header
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    # Parse the content directly
    feed = feedparser.parse(response.content)

    if feed.bozo:
        print(f"Still getting a Bozo error: {feed.bozo_exception}")
    else:
        for entry in feed.entries:
            entrylinkArr.append('- [' + entry.title + '](<' + entry.link + '>)' + '\n')

# bot-commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def setup_hook():
    # This syncs your commands globally
    await bot.tree.sync()
    print("Slash commands synced!")

@bot.tree.command(name="test", description="tests out tooltip")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Slash commands are working.")

@bot.tree.command(name="set-url", description="description=sets the RSS url you would like to recieve headlines from")
async def set_url(interaction: discord.Interaction, arg:str):
    global url
    url = arg
    await interaction.response.send_message(f"RSS URL set to: {url}", ephemeral=True)

# displays top 5 headlines from an rss page
@bot.tree.command(name="rss-headlines", description="Displays top 5 headlines from chosen RSS")
async def rss_hl(interaction: discord.Interaction):
    global url
    
    if not url:
        await interaction.response.send_message(
            "Set a URL first with /set-url <rss_url>.",
            ephemeral=True,
        )
        return

    try:
        rss_parse(url)
    except requests.RequestException as exc:
        await interaction.response.send_message(
            f"Failed to fetch RSS feed: {exc}",
            ephemeral=True,
        )
        return

    entryout = ""
    
    entryout += "# Latest Headlines from " + feed.feed.title + '\n'

    if not entrylinkArr:
        await interaction.response.send_message(
            "No headlines found in that feed.",
            ephemeral=True,
        )
        return

    for i in range(5):
        entryout += entrylinkArr[i]

    await interaction.response.send_message(entryout)

bot.run(TOKEN)
