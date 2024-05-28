# MISC
import os
import random

# DOTENV
from dotenv import load_dotenv

# DISCORD
from discord import Intents, Message, File, Member, DMChannel
from discord.ext.commands import Bot, Context
from discord.ext import commands as cmds

# TYPES
from typing import List

# Loading token:
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setting up bot and intents:
intents = Intents().default()
intents.message_content = True
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

""" ------------------------- BOT COMMANDS ------------------------- """

if __name__ == "__main__":
    bot.run(token=TOKEN)