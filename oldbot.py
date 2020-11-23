import os
import random
import discord
import asyncio
import datetime
import sys
import time
import info
import word_ladder as wl
import word_count as ws
import make_poem as mp

from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get


load_dotenv()
TOKEN = info.TOK
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='&')
client = discord.Client()

dictionary = wl.build_dictionary()


# Log on message for the bot
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])


# Writes errors to file
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


# info command
@bot.command(name='info')
async def info(ctx):
    info_message = 'Hi kid. My name\'s Bill. Bill Cipher. I help out around here\nMy prefix is `&` and I can do things like spam quotes and make fun of you.\nMaybe one day I\'ll be useful. But not today!'
    await ctx.send(info_message)


# Quote command
@bot.command(name='quote', help='Responds with a random Gravity Falls quote')
async def quote(ctx):

    gravity_falls_quotes = [
        'Reality is an illusion, the universe is a hologram, buy gold, bye!',
        'Hey kid, wanna make a *deal?*',
        'Time is dead and meaning has no meaning.',
        'Existence is upside down and i reign supreme.',
        'It\'s funny how dumb you are',
        'Here, have a head that\'s always screaming',
        'Did you miss me? Admit it, you missed me',
        'I\'m watching you nerds'
    ]

    response = random.choice(gravity_falls_quotes)
    await ctx.send(response)


# Rolls dice
@bot.command()
async def roll(ctx, num_dice: int, num_sides: int):
    dice = [
        str(random.choice(range(1, num_sides + 1)))
        for _ in range(num_dice)
    ]
    total = 0
    for die in dice:
        sum += int(die)
    await ctx.send(str(dice) + " with a total of " + str(total))


# ping command
@bot.command()
async def ping(ctx):
    '''
    Issues a ping and returns the latency
    '''

    latency = bot.latency
    await ctx.send("Pong! " + str(latency))


# Respond to messages
@bot.event
async def on_message(message):
    if (message.author.bot):
        return
    await bot.process_commands(message)
    msg = message.content.lower().replace(" ", "")
    username = message.author.name.lower().replace(" ", "")
    if '!stop!' in msg:
        await bot.logout()
    if 'brown' in msg:
        await message.channel.send('Brown is closed on weekends')
    if 'bill' in msg or 'cipher' in msg:
        emoji = '<:bill_cipher_pointing:621113711473590274>'
        await message.add_reaction(emoji)
    if 'dannys theme' in msg or "danny's theme" in msg:
        await message.channel.send('https://soundcloud.com/mynameisdonut/dannys-theme-but-im-leaving-it-unmixed-and-unfinished-because-danny-is-trash')
    if 'summon' in msg:
        emoji = '<:bill_cipher_pointing:621113711473590274>'
        await message.channel.send(emoji)
    if 'conceptually' in msg:
        emoji = '<:conceptually:688540260417667078>'
        await message.channel.send(emoji)
    if 'mel' in username:
        rand = random.randint(0, 1001)
        if rand is 42:
            await message.channel.send("Time's up, Mel.")
            await message.channel.send(file=discord.File('vibecheck.jpg'))

# join the voice channel


@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

# leave the voice channel


@bot.command()
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

# Word ladder


@bot.command()
async def word_ladder(ctx):
    context = ctx.message.content.lower().split()
    end_word = context[2]
    start_word = context[1]

    wl.check_words(dictionary, start_word, end_word)
    word_list = wl.build_word_list(dictionary, start_word)

    await ctx.send("Attempting to find a ladder between %s and %s"
                   % (start_word, end_word))
    start_time = time.time()
    ladder = wl.build_ladder(word_list, start_word, end_word)
    end_time = round(time.time() - start_time, 3)
    if end_time >= 120:
        await ctx.send("2 minute timeout reached: No ladder found in time")

    msg = "After " + str(end_time) + " seconds,"

    if ladder:
        await ctx.send("a ladder was found.")
        msg = msg + "\nA ladder was found!"
        for word in reversed(ladder):
            msg = msg + "\n" + word
        await ctx.send(msg)
    else:
        await ctx.send("no ladder found.")


@bot.command()
async def poem(ctx):
    context = ctx.message.content.lower().split()
    msg = ""
    available_files = os.listdir("./input_files")

    if len(context) > 1:
        if ".txt" in context[1]:
            path = os.path.join("./input_files/", context[1])
        else:
            path = os.path.join("./input_files/", context[1] + ".txt")

    if len(context) is 2:
        if "list" in context[1]:
            msg = "Hi there! I can make a poem using any of the following files:\n"
            for input_file in available_files:
                msg += str(input_file) + "\n"
        elif context[1] not in available_files and (context[1] + ".txt") not in available_files:
            msg = "There is no file named " + str(context[1]) + " available!"
        else:
            msg = mp.main(path, 3, 5, 7)

    elif len(context) is 5:
        if context[1] not in available_files and (context[1] + ".txt") not in available_files:
            msg = "There is no file named " + str(context[1]) + " available!"

        num_stanzas = eval(context[2])
        lines_per_stanza = eval(context[3])
        words_per_line = eval(context[4])
        msg = mp.main(path, num_stanzas, lines_per_stanza, words_per_line)
    else:
        msg = "Usage: `&poem <name of input file> <number of stanzas> <number of lines per stanza> <number of words per line>`"

    if len(msg) > 2000:
        await ctx.send("Reached the 2,000 character limit. Omitting excess.")
        msg = msg[:1999]
    await ctx.send(msg)


# Send random word
@bot.command()
async def rand(ctx):
    word = random.choice(dictionary)
    await ctx.send(word + "!")


# Send a message at a specific time
async def time_check():
    await bot.wait_until_ready()

    while True:
        await asyncio.sleep(30)
        channel = bot.get_channel(688536939132878848)
        now = datetime.datetime.now()

        rand = random.randint(0, 1001)
        if rand is 420:
            await channel.send("I'm watching you...")


bot.loop.create_task(time_check())

bot.run(TOKEN)
