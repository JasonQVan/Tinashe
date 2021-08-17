# bot.py
import os
import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import asyncio
import youtube_dl

load_dotenv()

intents = discord.Intents.default()
client = commands.Bot(command_prefix=".", intents=intents)

TOKEN = os.getenv("TOKEN")


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def goodbye(ctx):
    await ctx.send("Bye")


@client.command(pass_context=True)
async def p(ctx):
    song_there = os.path.isfile("song.mp3")
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    if song_there:
        source = FFmpegPCMAudio("song.mp3")
        player = voice.play(source)
        while True:
            await asyncio.sleep(2)
            if voice.is_playing() == False:
                await voice.disconnect()
                break
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192', 
            }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/PPGqUDC0TMs'])
        
        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                os.rename(file, "song.mp3")


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


client.run(TOKEN)
