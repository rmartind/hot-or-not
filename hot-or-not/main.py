"""
boy collection
girl collection

"""

import discord
import asyncio
import pymongo
from imgur import Imgur


client = discord.Client()


@client.event
async def on_ready():
    print(client.user.name)


@client.event
async def on_message(msg):
    if msg.channel.id == '502656152702681089':
        if msg.content.startswith('.girl'):
            embed = discord.Embed(
                title='*How to rate*', description='`.rate 1-10 to rate this image`', color=0x00BFFF, timestamp=msg.timestamp)
            embed.set_author(name='Hot or Not')
            embed.add_field(name='Average rating:', value=2.5, inline=True)
            embed.set_image(url='https://i.imgur.com/3vW8pdd.jpg')
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

client.run('TOKEN')
