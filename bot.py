# MISC
import os

# DOTENV
from dotenv import load_dotenv

# DISCORD
from discord import Intents, Message, File, Member, DMChannel
from discord.ext.commands import Bot, Context

# TYPES
from typing import List

# WEBSCRAPER
from webscraper.scraper import get_random_image_for_discord

# Loading token:
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setting up bot and intents:
intents = Intents().default()
intents.message_content = True
intents.members = True
bot: Bot = Bot(intents=intents, command_prefix="w!")

""" ------------------------- BOT EVENTS ------------------------- """
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is ready!")

@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    
    if "sus" in message.content:
        await message.channel.send("BAKA!")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member: Member) -> None:
    dm_channel: DMChannel = await member.create_dm()
    await dm_channel.send(f"Welcome to {member.guild.name}, {member.name} :)")

@bot.event
async def on_member_remove(member: Member) -> None:
    dm_channel: DMChannel = await member.create_dm()
    await dm_channel.send(f"Goodbye from {member.guild.name}, {member.name} :(")

""" ------------------------- BOT COMMANDS ------------------------- """
@bot.command(name="waifu", help="Sends a random image of whatever you tell it to.")
async def waifu(context: Context, search_term: str) -> None:
    sender: Member = context.author
    await context.send(f"Unfortunately {sender.name}, this feature is still being developed...")

if __name__ == "__main__":
    bot.run(token=TOKEN)