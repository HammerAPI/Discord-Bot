import discord
from discord.ext import commands
import info
import random
import time
import scripts.word_ladder as wl


PREFIX = "$"
# Startup
client = discord.Client()
bot = commands.Bot(command_prefix="{}".format(PREFIX))

# Globals
dictionary = wl.build_dictionary()


@bot.event
async def on_ready():
    print("{} has logged in".format(bot.user))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower().replace(" ", "")

    if "test" in msg:
        await message.channel.send("test")


@bot.command()
async def ping(ctx):
    '''
    Issues a ping and returns the latency
    '''
    latency = bot.latency
    await ctx.send("Pong! " + str(latency))


@bot.command()
async def roll(ctx, num_dice=0, num_sides=0):
    """
    Rolls `x` `n`-sided dice

    Usage: `roll x n`
    """

    if num_sides == 0 or num_dice == 0:
        await ctx.send("Usage: `{}roll [num dice] [num sides]`".format(PREFIX))
        return

    if num_sides > 1_000_000:
        num_sides = 1_000_000
    if num_dice > 1_000_000:
        num_dice = 1_000_000

    dice = [random.randint(1, num_sides) for _ in range(num_dice)]
    total = 0
    for die in dice:
        total += die

    message = "**Total:** " + str(total) + "\n**Rolls:** " + str(dice)
    if len(message) >= 2000:
        message = "**Total:** " + str(total) + "\nRolls emitted due to length"
    await ctx.send(message)


@bot.command()
async def ladder(ctx, start_word="", end_word=""):
    """
    Finds a word ladder between two words

    Usage: `ladder [start word] [end word]`
    """
    if not start_word or not end_word:
        await ctx.send("Usage: `{}ladder [start word] [end word]`".format(PREFIX))
        return

    msg, check = wl.check_words(dictionary, start_word, end_word)
    await ctx.send(msg)
    if check is None:
        return

    word_list = wl.build_word_list(dictionary, len(start_word))
    start_time = time.time()
    ladder = wl.build_ladder(word_list, start_word, end_word)
    end_time = round(time.time() - start_time, 3)
    if ladder == None:
        await ctx.send("2 minute timeout reached")

    if ladder:
        msg = "\nA ladder was found!"
        for word in ladder:
            msg = msg + "\n" + word
    else:
        msg = "No ladder was found"

    msg += "\nTime taken: " + str(end_time) + " seconds"
    await ctx.send(msg)


bot.run(info.TOK)
