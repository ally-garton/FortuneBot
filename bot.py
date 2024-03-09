# bot.py
import os
import discord
import random
import json

from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")



# intial test command #
@tree.command(name = "hello", description = "just saying hi", guild=discord.Object(id=GUILD_ID))
async def first_command(interaction):
    await interaction.response.send_message("oh, hello there!")




client.run(TOKEN)