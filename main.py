import discord
from discord.ext import commands
import random
import logging
import time
from datetime import datetime
from urllib import request
from api_geo import Tracker
import CogMaw as maw

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='?', description="description")

token = open("token.txt", "r")
API_TOKEN = token.read()
riot_token = open("riot_token.txt", "r")
RIOT_TOKEN = riot_token.read()


@bot.event
async def on_ready():
    timestamp = time.time()
    print('Logged in as')
    print(bot.user.name)
    print(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), "(UTC)")
    print(bot.user.id)
    print('------')


@bot.command()
async def marth():
    await bot.say("suger kuk")


@bot.command()
async def league(player_name, region):
    global RIOT_TOKEN
    summoner = maw.Summoner(RIOT_TOKEN, region=region, name=player_name)

    info = summoner.get_summoner_info()
    if info == 1:
        await bot.say("Could not find user; either the API is down or the user doesn't exist")
    info_list = maw.Json(summoner)

    embed = discord.Embed(title="Summoner Info", description="Information about a summoner", color=0x800080)
    embed.set_author(name="emas-bot", icon_url="https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png")
    embed.set_thumbnail(url=summoner.get_icon(info_list.profileIcon))
    embed.add_field(name="Name", value=info_list.name)
    embed.add_field(name="Level", value=info_list.level)
    embed.add_field(name="ID", value=info_list.id)
    await bot.say(embed=embed)


@bot.command(description="Gives the current position and address of the ISS")
async def iss():
    version = "MOBILE 1.0"
    tracker = Tracker(version)
    contents = tracker.pos_update()
    if contents == 1:
        raise request.HTTPError
    position = contents.get("iss_position")
    latitude = position.get("latitude")
    longitude = position.get("longitude")
    update_timestamp = time.time()
    update_timestamp = datetime.utcfromtimestamp(update_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    update_timestamp += " (UTC)"
    geo_name = tracker.location_query(position)
    hemisphere = tracker.hemisphere_check(position)
    embed = discord.Embed(title="ISS tracker", url="https://github.com/emasru/iss_tracker", description="Tracks the ISS", color=0x800080)
    embed.set_author(name="emas-bot", icon_url="https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png")
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/8/80/ISS_March_2009.jpg")
    embed.add_field(name="Latitude", value=latitude, inline=True)
    embed.add_field(name="Longitude", value=longitude, inline=True)
    embed.add_field(name="Hemisphere", value=hemisphere, inline=True)
    if geo_name is None:
        geo_name = "None (Sea)"
    embed.add_field(name="Address", value=geo_name, inline=True)
    embed.set_footer(text=update_timestamp)
    await bot.say(embed=embed)


@bot.command()
async def roy():
    await bot.say("is not our boy")


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def ban(member):
    try:
        await bot.ban(member, 0)
        await bot.say("Successfully banned", member)
    except Exception:
        await bot.say("Could not ban", member)


@bot.command()
async def ping():
    await bot.say("pong")


@bot.command(description="rolls a random integer in between the specified number and 1")
async def roll(dice: int):
    result = random.randint(1, dice)
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


bot.run(API_TOKEN)

'''
embed=discord.Embed(title=ISS tracker, url=https://github.com/emasru/iss_tracker, description=Tracks the ISS, color=0x800080)
embed.set_author(name=emas-bot,icon_url=https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png)
embed.set_thumbnail(url=https://upload.wikimedia.org/wikipedia/commons/8/80/ISS_March_2009.jpg)
embed.add_field(name=Latitude, value=latitude, inline=True)
embed.add_field(name=Longitude, value=longitude, inline=True)
embed.add_field(name=Hemisphere, value=hemisphere, inline=True)
embed.add_field(name=Address, value=address, inline=True)
await self.bot.say(embed=embed)
'''