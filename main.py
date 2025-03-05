import os
import random
import asyncio
import aiohttp
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Set up intents to allow reading message content
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Load environment variables (including the bot token)
load_dotenv()

# Fetch the bot token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Ensure that TOKEN is loaded correctly
if TOKEN is None:
    print("Error: DISCORD_TOKEN not found in .env file!")
else:
    # Run the bot with the token
    client.run(TOKEN)
