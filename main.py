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


def embed_timestamp():
    update_timestamp = time.time()
    update_timestamp = datetime.utcfromtimestamp(update_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    update_timestamp += " (UTC)"
    return update_timestamp


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


@bot.group(pass_context=True, description="Default region for commands is EUW")
async def league(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("No subcommand invoked")


@league.command(description="Looks up a summoner")
async def summoner(player_name, region="euw"):
    global RIOT_TOKEN
    player = maw.Summoner(RIOT_TOKEN, name=player_name)
    region_url = player.region_check(region)
    await player.get_summoner_info(region_url)
    if player.loaded is None:
        await bot.say("Summoner not found")
    player.json()
    timestamp = embed_timestamp()

    embed = discord.Embed(title="Summoner Info", description="Information about a summoner", color=0x800080)
    embed.set_author(name="emas-bot", icon_url="https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png")
    embed.set_thumbnail(url=player.get_icon(player.profileIcon))
    embed.add_field(name="Name", value=player.loaded_name)
    embed.add_field(name="Level", value=player.level)
    embed.add_field(name="ID", value=player.id)
    embed.set_footer(text=timestamp)
    await bot.say(embed=embed)


@league.command(description="Looks up an ongoing match by summoner")
async def match(player_name, region="euw"):
    global RIOT_TOKEN
    player = maw.Summoner(RIOT_TOKEN, name=player_name)
    region_url = player.region_check(region)
    await player.get_summoner_info(region_url)
    player.json()
    player_match = maw.Match(RIOT_TOKEN, player.id)
    await player_match.get_match(region_url)
    player_match.json()

    embed = discord.Embed(title="Match status", description="Information about a match", color=0x800080)
    embed.set_author(name="emas-bot", icon_url="https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png")
    embed.set_thumbnail(url="https://www.riotgames.com/darkroom/original/06fc475276478d31c559355fa475888c:af22b5d4c9014d23b550ea646eb9dcaf/riot-logo-fist-only.png")
    embed.add_field(name="Game started", value=player_match.game_start_time)
    embed.add_field(name="Current game time", value=player_match.game_length)
    embed.add_field(name="Champion", value=player_match.champion_id)
    embed.set_footer(text=embed_timestamp())
    await bot.say(embed=embed)


@league.command(description="Checks the status for a given region")
async def status(**region):
    global RIOT_TOKEN
    status_check = maw.Status(RIOT_TOKEN)
    region_url = maw.Summoner.region_check(region)
    await status_check.get_status(region_url)
    status_check.json()

    embed = discord.Embed(title="League status", description="Status of League of Legends' services", color=0x800080)
    embed.set_author(name="emas-bot", icon_url="https://cdn.discordapp.com/avatars/455442815800049685/0db7f7e2361b5f4ecf109601be986617.png")
    embed.set_thumbnail(url="https://www.riotgames.com/darkroom/original/06fc475276478d31c559355fa475888c:af22b5d4c9014d23b550ea646eb9dcaf/riot-logo-fist-only.png")
    embed.add_field(name="Game", value=status_check.game_status)
    embed.add_field(name="Store", value=status_check.store_status)
    embed.add_field(name="Website", value=status_check.website_status)
    embed.add_field(name="Client", value=status_check.client_status)
    embed.set_footer(text=embed_timestamp())
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
    timestamp = embed_timestamp()
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
    embed.set_footer(text=timestamp)
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