# Emergency Tones Discord Bot
# Created by Js0n#7106

# Before continuing, ensure you have the following things installed:
# - FFmpeg (it must be added to your default PATH environment variables)
# - discord python package

import discord
import time
from discord.ext import commands
from discord import FFmpegPCMAudio

# CREATE A BOT AT https://discord.com/developers/applications/
TOKEN = 'INSERT YOUR BOT TOKEN HERE'

# SET YOUR PREFIX
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot online!')

@client.command(pass_context = True)
async def tones(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice == None:
        tones_active = False
    else:
        tones_active = True

    # Copy the voice channel ID that you would like the bot to play the tones in
    channel_id = CHANGEME #(<-- Should be in integer form, meaning just a number with no quotes or anything around it)
    voice_channel = client.get_channel(channel_id)

    if not tones_active:
        voice = await voice_channel.connect()
        await ctx.message.delete()
        tones_active = True

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        # IF YOU'D LIKE TO CREATE YOUR OWN CUSTOM EMBED THAT IS DIFFERENT THAN MY FORMAT
        # GO TO https://cog-creators.github.io/discord-embed-sandbox/

        # Configure the message sent when the codes are toggled ON
        embed=discord.Embed(title=":bangbang: CODE 33 IS NOW IN EFFECT :bangbang:", description="Emergency Radio Traffic Only", color=0xff0000)
        embed.set_thumbnail(url="INSERT LINK TO THUMBNAIL")
        embed.set_footer(text=current_time)
        await ctx.send(embed=embed)

        voice_client = ctx.guild.voice_client

        # Ensure your audio file for the emergency tones is named tones.mp3
        source = FFmpegPCMAudio('tones.mp3')
        voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else client.loop.create_task(play_source(voice_client)))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.5
    else:
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()
        await ctx.message.delete()
        tones_active = False

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        # Configure the message sent when the codes are toggled ON
        embed=discord.Embed(title=":exclamation: CODE 33 IS NO LONGER IN EFFECT :exclamation:", description="All Radio Traffic May Resume", color=0x11ff00)
        embed.set_thumbnail(url="INSERT LINK TO THUMBNAIL")
        embed.set_footer(text=current_time)
        await ctx.send(embed=embed)

@client.command(pass_context = True)
async def play_source(voice_client):
    source = FFmpegPCMAudio('tones.mp3')
    voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else client.loop.create_task(play_source(voice_client)))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = 0.5

client.run(TOKEN)
