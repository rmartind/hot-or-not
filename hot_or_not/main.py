import discord
import random
import asyncio
import pymongo
import configparser
from imgur import Imgur


config = configparser.ConfigParser()
config.read('config.ini')

imgur_client_id = config['IMGUR_CLIENT']['CLIENT_ID']
girl_album_hash = config['IMGUR_CLIENT']['GIRL_HASH']

imgur = Imgur(imgur_client_id)
client = discord.Client()


@client.event
async def on_ready():
    print(client.user.name)


@client.event
async def on_message(msg):
    if msg.channel.id == '502656152702681089':
        if msg.content.startswith('.girl'):

            girl_images = imgur.album_images(girl_album_hash)['data']
            girl_count = len(girl_images)
            random_girl = girl_images[random.randrange(girl_count)]


            embed = discord.Embed(
                title='*How to rate*', description='`.rate 1-10 to rate this image`', color=0x00BFFF, timestamp=msg.timestamp)
            embed.set_author(name='Hot or Not')
            embed.add_field(name='Average rating:', value=2.5, inline=True)
            embed.set_image(url=random_girl['link'])
            embed.set_footer(text='sent')
            await client.send_message(msg.channel, embed=embed)

        elif msg.content.startswith('.boy'):
            embed = discord.Embed(
                title='*How to rate*', description='`.rate 1-10 to rate this image`', color=0x00BFFF, timestamp=msg.timestamp)
            embed.set_author(name='Hot or Not')
            embed.add_field(name='Average rating:', value=2.5, inline=True)
            embed.set_image(url='https://i.imgur.com/3vW8pdd.jpg')
            embed.set_footer(text='sent')
            await client.send_message(msg.channel, embed=embed)

        elif msg.content.startswith('.rate'):
            print('.rate')

client.run('NTQ3MjM4MTIyMjI0NzQ2NDk2.D05Ubg.UP4NZKpH71VBWaLdAGvzbGYGMU0')
