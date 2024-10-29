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

@bot.tree.command(name="newevent", description="Create a new event")
@app_commands.describe(
    name="Name of the event",
    is_private="Set to True for a private event; False for a public event",
    event_date="Date and time of the event in YYYY-MM-DD HH:MM format",
    expiry_date="Date and time the channel should expire in YYYY-MM-DD HH:MM format"
)
async def create_event(interaction: discord.Interaction, name: str, is_private: bool, event_date: str, expiry_date: str):
    event_date = datetime.strptime(event_date, "%Y-%m-%d %H:%M")
    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M")

    new_event = Event(
        name=name,
        creator_id=interaction.user.id,
        is_private=is_private,
        event_date=event_date,
        expiry_date=expiry_date,
        archive_after_expiry=True  # Set default value; you could make this configurable
    )

    # Add the event to the session and commit
    try:
        session.add(new_event)
        session.commit()
        await interaction.response.send_message(f"Event '{name}' created successfully!")
    except Exception as e:
        session.rollback()
        await interaction.response.send_message("Failed to create event. Please try again.")
        print(f"Error: {e}")
# Close the database session on bot shutdown
@bot.event
async def on_close():
    session.close()

# Run the bot with your token
bot.run(token)
