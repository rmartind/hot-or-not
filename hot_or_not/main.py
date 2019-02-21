import discord
import asyncio
import configparser
from collections import OrderedDict
import pymongo
from mongo import Mongo


config = configparser.ConfigParser()
config.read('config.ini')
mongo = Mongo(config['IMGUR_CLIENT']['CLIENT_ID'])
client = discord.Client()
rating_cache = OrderedDict()


def create_embed(link, rating, count, msg):
    embed = discord.Embed(
        title='*How to rate*', description='`.rate 1-10 to rate this image`', color=0xff3232, timestamp=msg.timestamp)
    embed.set_author(name='Hot or Not', icon_url=client.user.avatar_url)
    embed.add_field(name='Average rating:', value=rating, inline=True)
    embed.add_field(name='Votes:', value=count, inline=True)
    embed.set_image(url=link)
    return embed

def help_embed(msg):
    embed = discord.Embed(
        title='*Instructions*', description='`displays photos of boys and girls to rate.`', color=0xff3232, timestamp=msg.timestamp)
    embed.set_author(name='Hot or Not', icon_url=client.user.avatar_url)
    embed.add_field(name='Show girl:', value='`.girl`', inline=True)
    embed.add_field(name='Show boy:', value='`.boy`', inline=True)
    embed.add_field(name='rate:', value='`.rate value - value must be 1-10`', inline=True)
    embed.set_thumbnail(url=msg.channel.server.icon_url)
    return embed    

def add_rating(new_rating, requester):
    if new_rating <= 10 and new_rating > 0:
        if rating_cache[requester][1] == 'girl':
            mongo.update_girl(rating_cache[requester][0], new_rating)
        else:
            mongo.update_boy(rating_cache[requester][0], new_rating)
        del rating_cache[requester]
    else:
        raise ValueError('Rating must be between 0-10.')


@client.event
async def on_ready():
    print(client.user.name)
    await client.change_presence(game=discord.Game(name='.help'), status=discord.Status.dnd)


@client.event
async def on_message(msg):
    if msg.channel.id == config['DISCORD_CLIENT']['BOT_CHANNEL']:
        if msg.content.startswith('.girl'):
            image = mongo.random_girl()
            hash = None
            url = None
            rating = None
            count = None
            for e in image:
                url = e['link']
                rating = e['rating']
                hash = e['_id']
                count = e['count']

            if len(rating_cache) < 4:
                rating_cache[msg.author.id] = (hash, 'girl')
            else:
                rating_cache.popitem(last=False)

            embed = create_embed(url, rating, count, msg)
            await client.send_message(msg.channel, embed=embed)
        elif msg.content.startswith('.boy'):
            image = mongo.random_boy()
            hash = None
            url = None
            rating = None
            count = None
            for e in image:
                url = e['link']
                rating = e['rating']
                hash = e['_id']
                count = e['count']

            if len(rating_cache) < 4:
                rating_cache[msg.author.id] = (hash, 'boy')
            else:
                rating_cache.popitem(last=False)
            embed = create_embed(url, rating, count, msg)
            await client.send_message(msg.channel, embed=embed)
    
        elif msg.content.startswith('.rate'):
            try:
                add_rating(int(msg.content[len('.rate'):].strip()), msg.author.id)
                await client.send_message(msg.channel, '`Rating added.`')
            except KeyError:
                await client.send_message(msg.channel, '`Nothing to rate.`')
            except ValueError:
                await client.send_message(msg.channel, '`Rating must be between 0-10.`')

        elif msg.content.startswith('.upload album girl'):
            if msg.author.id == config['DISCORD_CLIENT']['ADMIN_ID']:
                mongo.upload_album(msg.content[len('.upload album girl'):].strip())
            else:
                await client.send_message(msg.channel, '`You must be an administator to perform this command.`')

        elif msg.content.startswith('.upload album boy'):
            if msg.author.id == config['DISCORD_CLIENT']['ADMIN_ID']:
                mongo.upload_album(msg.content[len('.upload album boy'):].strip(), girl=False)
            else:
                await client.send_message(msg.channel, '`You must be an administator to perform this command.`')
        elif msg.content.startswith('.help'):
            await client.send_message(msg.channel, embed=help_embed(msg))


client.run(config['DISCORD_CLIENT']['BOT_TOKEN'])
