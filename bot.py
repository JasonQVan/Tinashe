# bot.py
import os
from time import sleep
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import asyncio
load_dotenv()

intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents=intents)

TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def goodbye(ctx):
    await ctx.send("Bye")


@client.event
async def on_member_join(member):
    channel = client.get_channel(client.guilds.channels[0].id)
    await channel.send(f'Welcome to {client.guilds.name}, {member.name}.')

@client.command(pass_context=True)
async def periodt(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('periodt.mp3')
        player = voice.play(source)
        while True:
            await asyncio.sleep(5)
            if voice.is_playing() == False:
                await voice.disconnect()
                break
    else:
        await ctx.send("You are not in a voice channel.")
        
        
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
        
client.run(TOKEN)
