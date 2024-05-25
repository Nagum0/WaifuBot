import os
import random
from dotenv import load_dotenv
from discord import Intents, Message, File, Member
from discord.ext.commands import Bot, Context
from discord.ext import commands as cmds
from typing import List

# Loading token:
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setting up bot and intents:
intents = Intents().default()
intents.message_content = True
bot: Bot = Bot(intents=intents, command_prefix="!") 

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(msg: Message):
    if msg.author == bot.user:
        return
    
    msg_content: str = f"[{msg.channel}] {msg.author}: {msg.content}"
    print(msg_content)

    with open("messages.log", "a") as file:
        file.write(msg_content + "\n")
    	
    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx: Context, error: cmds.CommandError):
    if isinstance(error, cmds.CommandNotFound):
        await ctx.channel.send("Command doesn't exist!")

@bot.event
async def on_member_join(member: Member):
    await member.dm_channel

@bot.command(name="rei", help="Sends an image of Rei...")
async def rei(ctx: Context):
    try:
        await ctx.channel.send(file=File("imgs/rei/rei9.jpg"))
    except Exception as e:
        await ctx.channel.send("Something went wrong...")

@bot.command(name="sex", help="SEGGSO")
async def sex(ctx: Context, sex: str = "IDK"):
    if sex == "male":
        await ctx.channel.send("SAY GEX")
    elif sex == "female":
        await ctx.channel.send("SESBIAN LEX")
    else:
        await ctx.channel.send("HUH...")

@bot.command(name="astolfo", help="Sends a random astolfo image!")
async def astolfo(ctx: Context):
    imgs: List[str] = os.listdir("imgs/astolfo")
    try:
        await ctx.channel.send(file=File("imgs/astolfo/" + random.choice(imgs)))
    except FileNotFoundError as fe:
        await ctx.channel.send("File not found...")

bot.run(token=TOKEN)