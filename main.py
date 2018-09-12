import discord
from discord.ext import commands
import random
import logging
import time
from datetime import datetime


logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='?', description="description")

token = open("token.txt", "r")
API_TOKEN = token.read()


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
async def add(left : int, right : int):
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


@bot.command()
async def roll(dice: int):
    result = random.randint(dice)
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member : discord.Member):
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

