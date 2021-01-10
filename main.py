# bot.py
import os
import random
import pickle

import discord
from discord import Embed, Colour
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=".")

print('lol')


@bot.command()
async def mock(ctx, *arguments):
    result = ""
    for argument in arguments:
        result += argument + " "
    response = ''.join(x.upper() if random.randint(0, 1) else x for x in result)

    await ctx.message.delete()
    # await ctx.channel.send(response)
    # await ctx.channel.send("<:mock:766712939704614934>")
    embed = Embed(
        title=ctx.message.author.name,
        colour=Colour(0xE5E242),
        description=response + "<:mock:766712939704614934>",
    )
    await ctx.send(embed=embed)


@bot.command()
async def helpMe(ctx):
    embed = Embed(
        title="Help",
        colour=Colour(0xE5E242),
        description="Commands are <.mock> and <.lmgtfy>. Who needs docs anyway ¯\\_(ツ)_/¯",
    )
    await ctx.send(embed=embed)


@bot.command()
async def lmgtfy(ctx, *arguments):
    query = "https://www.google.com/search?q="
    for argument in arguments:
        query += argument + "+"

    embed = Embed(
        title="Let me help you with that...",
        colour=Colour(0xE5E242),
        description="Have you tried using google already? " + "\n" + query,
    )
    await ctx.send(embed=embed)


@bot.command()
async def vote(ctx, *args):
    embed = Embed(
        title="Umfrage von {0}".format(ctx.message.author.name),
        colour=Colour(0x8f1312),
        description=' '.join(args) + '?',
        thumbnail=ctx.message.author.avatar_url,
    )

    await ctx.message.delete()
    reactto = await ctx.send(embed=embed)
    await reactto.add_reaction('👍')
    await reactto.add_reaction('👎')


@bot.event
async def on_message(message):
    channel = message.channel
    text = message.content.lower()
    messageOidaCount = 0
    with open('oidaFile.pickled', 'rb') as in_file:
        oidas = pickle.load(in_file)
        print('loaded value ' + str(oidas))
    wordlist = text.split()
    if not message.author.bot:
        for word in wordlist:
            if "oida" in word:
                messageOidaCount += 1
    print('oida count ' + str(messageOidaCount))
    oidas += messageOidaCount
    with open('oidaFile.pickled', 'wb') as out_file:
        pickle.dump(oidas, out_file)
    if "oida" in text:
        if message.author.bot:
            return
        embed = Embed(
            title="OIDA COUNT",
            colour=Colour(0x8f1312),
            description="{0} <:spam:797552389083234315>".format(oidas),
        )
        await channel.send(embed=embed)
    await bot.process_commands(message)


bot.run(TOKEN)
