import feedparser
import requests
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

#rss-parsing

entrylinkArr = []
url = ""
feed = ""

def rss_parse(arg):

    # url = "https://www.fastcompany.com/latest/rss"
    global url
    global feed

    url = arg

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch the raw content with a custom header
    response = requests.get(url, headers=headers)

    # Parse the content directly
    feed = feedparser.parse(response.content)


    if feed.bozo:
        print(f"Still getting a Bozo error: {feed.bozo_exception}")
    else:
        # entryout += '```'
        for entry in feed.entries:
            entrylinkArr.append('- [' + entry.title + '](' + entry.link + ')' + '\n')
        # entryout += '```'

        # for entry in feed.entries:
        #     print(entry.title)
    

#bot-commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@app_commands.command(description="tests if commands work")
@bot.command()
async def test(ctx):
    pass

@app_commands.command(description="sets the RSS url you would like to recieve headlines from")
@bot.command()
async def set_url(ctx, arg):
    global url
    url = arg

# displays top 5 headlines from an rss page
@app_commands.command(description="displays top 5 headlines from RSS")
@bot.command()
async def rss_hl(ctx):
    global url
    rss_parse(url)

    entryout = ""
    
    entryout += "# Latest Headlines from " + feed.feed.title + '\n'
    for i in range(5):
        entryout += entrylinkArr[i]

    await ctx.send(entryout)
    # print(entryout)


bot.run(TOKEN)

# headless browser example

# source .venv/bin/activate.fish - to activate venv
# deactivate - deactivate venv
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import feedparser

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# driver.get("http://www.fastcompany.com/latest/rss")
# feed_content = driver.page_source
# feed = feedparser.parse(feed_content)

# print(feed)

# driver.quit()

