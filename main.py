import discord
from discord.ext import commands 
import os
import requests
import json
import aiohttp
my_secret = os.environ['TOKEN']
client = commands.Bot(command_prefix="!")

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
@client.command()
async def meme(ctx):
  async with aiohttp.ClientSession() as cs:
    async with cs.get("https://www.reddit.com/r/memes/hot.json") as r:
      memes = await r.json()
      embed = discord.Embed (
        color = discord.Color.purple()
      )
      embed.set_image(url=memes["data"]["children"][random.randint(0,25)]["data"]["url"])
      embed.set_footer(text=f"Powered by r/memes and requested by {ctx.author}") 
@client.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

client.run(my_secret)

