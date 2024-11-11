
import discord
from discord.ext import commands, tasks 
import os
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timezone  # Import timezone

# Load the token from the environment
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
key = os.getenv("my_token")

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Global flag to track whether the initial check has been performed
# initial_check_done = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    # global initial_check_done
    # if not initial_check_done:
    await initial_message_check()
        # initial_check_done = True
    regular_check.start()  # Start the regular checks after the initial check

async def initial_message_check():
    print("Performing initial message check...")
    target_bot_id = 945683386100514827  # The bot ID to check for
    for guild in bot.guilds:
        for channel in guild.text_channels + guild.voice_channels:
            try:
                # Adjust the limit as needed to perform a thorough initial check
                async for m in channel.history(limit=None):
                    if m.author.id == target_bot_id:
                        await m.delete()
            except discord.errors.Forbidden:
                print(f"Missing permissions in {channel.name} of {guild.name}")
            except Exception as e:
                print(f"An error occurred during the initial check: {e}")
    print("Initial message check completed.")

@tasks.loop(seconds = 30)
async def regular_check():
    print("Performing regular message check...")
    target_bot_id = 945683386100514827  # The bot ID to check for
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                # Now limiting to the last 100 messages for regular checks
                async for m in channel.history(limit=100):
                    current_time_utc = datetime.now(timezone.utc)
                    time_diff = current_time_utc - m.created_at
                    if m.author.id == target_bot_id and time_diff.total_seconds() > 60:
                        await m.delete()
            except discord.errors.Forbidden:
                print(f"Missing permissions in {channel.name} of {guild.name}")
            except Exception as e:
                print(f"An error occurred during the regular check: {e}")
    print("Regular message check completed.")

bot.run(key)

