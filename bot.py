# bot.py
import os
import discord
import random
import json

from discord import app_commands
from dotenv import load_dotenv

from _8ball import responses


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


# magic 8-ball command #
@tree.command(name="magic8ball", description="Ask anything!", guild=discord.Object(id=GUILD_ID))
async def magic_8ball(interaction, question: str):
    number = random.randint(0, len(responses))
    await interaction.response.send_message(f'You asked: {question} \n\nMagic 8 Ball says: {responses[number].lower()}')


# magic 8-ball command #
@tree.command(name="numerology", description="Find your life path number.", guild=discord.Object(id=GUILD_ID))
async def numbers(interaction, date: int, month: int, year: int):
    if (date > 31 or date < 1) or (month < 1 or month > 12) or (year < 1000 or year > 9999) or (month == (4 or 6 or 9 or 11) and date > 30) or (month == 2 and date > 28 and (year % 4 != 0)) or (month == 2 and date > 29 and (year % 4 == 0)):
        print('invalid date')
        await interaction.response.send_message('Invalid date!')
    
    else:
        date = list(str(date))
        month = list(str(month))
        year = list(str(year))

        date_array = date + month + year
        date_total = 0

        for i in range(0, len(date_array)):
            date_total += int(date_array[i])
        
        life_path_total = list(str(date_total))
        life_path_number = 0;

        for i in range(0, len(life_path_total)):
            life_path_number += int(life_path_total[i])


        await interaction.response.send_message(f'Your life path number is {life_path_number}.')





client.run(TOKEN)