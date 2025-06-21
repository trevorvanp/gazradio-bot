import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup Discord bot
intents = nextcord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Bulldogs Radio Stream
BULLDOGS_URL = "https://bulldogsradio.radioca.st/stream?ver=161693"

@bot.event
async def on_ready():
    print(f"🎵 Logged in as {bot.user.name} — Auto-stream engaged!")

    # 🔧 Replace this with your exact server name
    GUILD_NAME = "Gaz's Gutter"
    CHANNEL_NAME = "Gaz Radio"

    # Try to find the guild and voice channel
    for guild in bot.guilds:
        if guild.name == GUILD_NAME:
            for channel in guild.voice_channels:
                if channel.name == CHANNEL_NAME:
                    try:
                        vc = await channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio(
                            BULLDOGS_URL,
                            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                            options='-vn -bufsize 64k'
                        ))
                        print(f"🟢 Auto-playing Bulldogs Radio in {CHANNEL_NAME}")
                        return
                    except nextcord.ClientException as e:
                        print(f"⚠️ Bot is already connected: {e}")
                        return
    print("❌ Could not find the GazRadio channel or connect to it.")

@bot.command()
async def play(ctx):
    """Manual play command in case auto fails"""
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to summon the beast!")
        return

    channel = ctx.author.voice.channel
    try:
        vc = ctx.voice_client or await channel.connect()
    except nextcord.ClientException as e:
        await ctx.send("❌ Failed to connect to voice.")
        print(f"Voice connection error: {e}")
        return

    if vc.is_playing():
        vc.stop()

    vc.play(nextcord.FFmpegPCMAudio(
        BULLDOGS_URL,
        before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        options='-vn -bufsize 64k'
    ))

    await ctx.send("🐾 Now playing: **Bulldogs Radio**")

@bot.command()
async def stop(ctx):
    """Stops the stream"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("🛑 Playback stopped.")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Peace out!")

# Run the bot
bot.run(TOKEN)
