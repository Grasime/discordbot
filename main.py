import os
import random
import asyncio
import aiohttp
from dotenv import load_dotenv
from discord import Intents, Member
from discord.ext import commands
import discord

# Load token from a safe location
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup, this is for permissions
intents = Intents.default()
intents.messages = True  # Enable message intent
intents.message_content = True  # Enable message content intent

# Define the bot prefix and include intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command handler for the 'ping' command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Mute command
@bot.command()
@commands.has_permissions(manage_roles=True)  # Ensure the user running the command has the required permission
async def mute(ctx, member: Member, time: int, *, reason: str = "No reason provided"):
    """Mutes a member for a specific time with a reason."""
    # Create or find a 'Muted' role
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")

    # If no Muted role exists, create one
    if not muted_role:
        muted_role = await guild.create_role(name="Muted", reason="For muting users")
        for channel in guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    # Apply the role to the member
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {time} seconds. Reason: {reason}")

    # Wait for the specified time, then unmute
    await asyncio.sleep(time)
    await member.remove_roles(muted_role, reason="Mute duration expired")
    await ctx.send(f"{member.mention} has been unmuted.")

# Define the momma command
@bot.command()
async def momma(ctx, target: str):
    """Sends a 'yo mama' joke directed at the target."""
    # List of 'yo mama' jokes
    jokes = [
        "Yo mama so fat, when she skips a meal, the stock market drops.",
        "Yo mama so old, her birth certificate says 'Expired.'",
        "Yo mama so stupid, she stared at a cup of orange juice for 12 hours because it said 'Concentrate.'",
        "Yo mama so clumsy, she tripped over a wireless router.",
        "Yo mama so short, she went to see Santa and he told her to get back to work."
    ]

    # Pick a random joke
    joke = random.choice(jokes)

    # Send the joke, mentioning the target
    await ctx.send(f"{target}, {joke}")

# Mimic command
@bot.command()
async def mimic(ctx, target: discord.Member):
    """Mimics the target user's name and avatar."""
    # Change the bot's nickname to the target's name
    await ctx.guild.me.edit(nick=target.display_name)

    # Fetch the target's avatar and update the bot's avatar
    avatar_url = target.avatar.url
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            if response.status == 200:
                avatar_data = await response.read()
                await bot.user.edit(avatar=avatar_data)
                await ctx.send(f"Now mimicking {target.display_name}!")
            else:
                await ctx.send("Failed to fetch avatar.")

# Reset command
@bot.command()
async def reset(ctx):
    """Resets the bot's name and avatar."""
    await ctx.guild.me.edit(nick=None)  # Reset nickname
    await bot.user.edit(avatar=None)  # Reset avatar
    await ctx.send("Stopped mimicking!")

# Say command
@bot.command()
async def say(ctx, message: str, channel_name: str):
    """Sends a message as the bot to a specified channel."""
    # Find the channel by name
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)

    if channel is None:
        await ctx.send(f"Channel `{channel_name}` not found.")
        return

    # Send the message in the specified channel
    await channel.send(message)
    await ctx.send(f"Message sent to #{channel_name}!")

# Run the bot
def main():
    bot.run(TOKEN)  # Use bot.run instead of client.run

if __name__ == "__main__":
    main()
