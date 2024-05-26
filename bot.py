# bot.py
import os
import discord
import random
import json

import requests
from bs4 import BeautifulSoup

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


# numerology (birthday) command #
@tree.command(name="numerology", description="Input your birthday to find your life path number.", guild=discord.Object(id=GUILD_ID))
async def life_path(interaction, date: app_commands.Range[int, 1, 31], month: app_commands.Range[int, 1, 12], year: app_commands.Range[int, 1000, 9999]):
    if (month == (4 or 6 or 9 or 11) and date > 30) or (month == 2 and date > 28 and (year % 4 != 0)) or (month == 2 and date > 29 and (year % 4 == 0)):
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
        life_path_number = 0

        for i in range(0, len(life_path_total)):
            life_path_number += int(life_path_total[i])


        await interaction.response.send_message(f'Your life path number is {life_path_number}.')


# numerology (name) command #
@tree.command(name="destiny", description="Input your full name to find your destiny number.", guild=discord.Object(id=GUILD_ID))
async def destiny_number(interaction, full_name: str):
    numbers_dict = { "a" : 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 1, "k": 2, "l": 3, "m": 4, "n": 5, "o": 6, "p": 7, "q": 8, "r": 9, "s": 1, "t": 2, "u": 3, "v": 4, "w": 5, "x": 6, "y": 7, "z": 8 }

    name_array = full_name.lower().split()
    name_total = 0
    name_total_array = []

    # for each name (separated by spaces), find the sum of their values and put individual name values in an array
    # e.g. john doe -> ['john', 'doe'] -> [(1 + 6 + 8 + 5), (4 + 6 + 5)] -> [20, 15]
    for x in range(0, len(name_array)):
        for y in range(0, len(name_array[x])):
            if name_array[x][y] in numbers_dict:
                name_total += numbers_dict[name_array[x][y]]

        name_total_array.append(str(name_total))
        name_total = 0

    # converts values in the array to single digit values
    # e.g. [20, 15] -> [(2 + 0), (1 + 5)] -> [2, 6]
    destiny_total = 0
    destiny_total_array = []
    for x in range(0, len(name_total_array)):
        if not (name_total_array[x] == 11 or name_total_array[x] == 22):
            for y in range(0, len(name_total_array[x])):
                destiny_total += int(name_total_array[x][y])

            destiny_total_array.append(destiny_total)
            destiny_total = 0

        else:
            destiny_total_array.append(name_total_array[x])


    # finds the sum of the array values and then converts it to a single digit
    # e.g. [2, 6] -> 8 (already single digit)
    destiny_number = 0
    for x in range(0, len(destiny_total_array)):
        destiny_number += destiny_total_array[x]

    if destiny_number >= 10 and destiny_number != 11 and destiny_number != 22:
        destiny_number = str(destiny_number)
        temp = 0
        for x in range(0, len(destiny_number)):
            temp += int(destiny_number[x])

        destiny_number = temp

    await interaction.response.send_message(f'Your destiny number is {destiny_number}.')


# daily horoscope command #
@tree.command(name="horoscope", description="Your daily horoscope, pulled from horoscope.com", guild=discord.Object(id=GUILD_ID))
async def horoscope(interaction, sign: str):
    star_signs = { "aries": 1, "taurus": 2, "gemini": 3, "cancer": 4, "leo": 5, "virgo": 6, "libra": 7, "scorpio": 8, "sagittarius": 9, "capricorn": 10, "aquarius": 11, "pisces": 12  }
    sign_value = 0

    if not (sign.lower() in star_signs):
        horoscope_p = "Oops! That's not a valid star sign...did you spell it correctly?"

    else:
        sign_value = star_signs[sign]

        url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={sign_value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        horoscope_div = soup.find('div', class_="main-horoscope").text

        for element in horoscope_div:
            horoscope_p = str(soup.find('p', class_=""))

        elements = ["<p>", "</p>", "<strong>", "</strong>"]

        for x in range(0, len(elements)):
            horoscope_p = horoscope_p.replace(elements[x], "")

    await interaction.response.send_message(f'{horoscope_p}')


# tarot card (single) command #
@tree.command(name="tarot-card", description="Draw a single Tarot card.", guild=discord.Object(id=GUILD_ID))
async def single_tarot(interaction):
    card_id = random.randint(0, 77)
    orientation = random.randint(0, 1)

    with open('tarot.json') as tarot_json:
        data = json.load(tarot_json)
        card = data[card_id]
        card_meaning_array = []

        if orientation == 0:
            card_meaning_array = (card.get("reverse_meaning")).split(", ")
        else:
            card_meaning_array = (card.get("meaning")).split(", ")

        card_meaning_array[-1] = f'and {card_meaning_array[-1]}'

        card_meaning = ', '.join(card_meaning_array).lower()


        await interaction.response.send_message(f'Your card is: {card.get("name")}{f" (reversed)" if (orientation == 0) else ""}. This typically represents {card_meaning}.')


client.run(TOKEN)