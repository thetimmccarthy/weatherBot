import requests
import discord
import os
import discord.ext
import pytz
from datetime import datetime
from discord.ext import commands

my_secret = os.environ['TOKEN']
weather_key = os.environ['weather']

client = discord.Client()

client = commands.Bot(command_prefix='$')


def toEasternTime(timestamp):
    est = pytz.timezone('US/Eastern')
    fmt = '%Y-%m-%d %H:%M:%S'
    return timestamp.astimezone(est).strftime(fmt)


@client.event
async def on_ready():
    print('Welcome to the server, {0.user}!'.format(client))


@client.command()
async def weather(ctx, lookup):
    if lookup == "":
        await ctx.send('Please specify a city to lookup!')

    try:
        try:
            lookup = int(lookup)
            lookup = str(lookup)
            url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + lookup + '&units=imperial&appid=' + weather_key

        except:
            lookup = lookup.strip().capitalize()
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + lookup + '&units=imperial&appid=' + weather_key

    except:
        await ctx.send(
            'I do not recognize that city, please make sure you have spelled it correctly.'
        )
    response = requests.get(url).json()
    temp = response['main']['temp']
    await ctx.send('It is currently {0} degrees in {1}!'.format(
        int(temp), lookup))


@client.command()
async def forecast(ctx, lookup):
    if lookup == "":
        await ctx.send('Please specify a city or zipcode to lookup!')

    results = {}
    try:
        try:
            lookup = int(lookup)
            lookup = str(lookup)
            url = 'http://api.openweathermap.org/data/2.5/forecast?zip=' + lookup + '&units=imperial&appid=' + weather_key

        except:
            lookup = lookup.strip().capitalize()
            url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + lookup + '&units=imperial&appid=' + weather_key

    except:
        await ctx.send(
            'I do not recognize that city, please make sure you have spelled it correctly.'
        )

    response = requests.get(url).json()

    for x in response['list']:
        utcTime = datetime.fromtimestamp(x['dt'])
        est = toEasternTime(utcTime)

        if est[0:10] not in results:
            results[est[0:10]] = [x['main']['temp'], x['weather'][0]['main']]

    to_send = '    Date   | Temp (F) |  Weather\n'
    to_send += '--------------------------------\n'

    for key, value in results.items():
        to_send += '{0} |   {1}   | {2}\n'.format(key, int(value[0]), value[1])

    await ctx.send(to_send)


client.run(my_secret)
