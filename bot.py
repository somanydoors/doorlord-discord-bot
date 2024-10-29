#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import os

# Get token file path from environment variable
token_path = os.getenv("DISCORD_BOT_TOKEN_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_token.txt"))

# Read the bot token from the specified file path
try:
    with open(token_path, "r") as f:
        token = f.read().strip()
except FileNotFoundError:
    raise ValueError(f"Token file not found at path: {token_path}")

# Import the database models and session function
from database import Event, Participant, get_session

# Create a database session
session = get_session()

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is ready and slash commands synced")

# Close the database session on bot shutdown
@bot.event
async def on_close():
    session.close()

# Run the bot with your token
bot.run(token)
