import discord
import asyncio
import pymongo
import uvloop
import configparser
from collections import OrderedDict
from mongo import Mongo
from embeds import Embeds


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

config = configparser.ConfigParser()
config.read('config.ini')

mongo = Mongo(config['IMGUR_CLIENT']['CLIENT_ID'])
client = discord.Client()
embeds = Embeds(client)

rating_cache = OrderedDict()


def add_rating(new_rating, requester):
    if new_rating <= 10 and new_rating > 0:
        if rating_cache[requester][1] == 'girl':
            mongo.update_girl(rating_cache[requester][0], new_rating)
        else:
            mongo.update_boy(rating_cache[requester][0], new_rating)
        del rating_cache[requester]
    else:
        raise ValueError('Rating must be between 1-10.')


def add_to_cache(image_hash, gender, id):
    if len(rating_cache) > 4:
        rating_cache.popitem(last=False)
    if gender == 'girl':
        rating_cache[id] = (image_hash, 'girl')
    else:
        rating_cache[id] = (image_hash, 'boy')


def prepare_image(gender, msg):
    if gender == 'girl':
        image = mongo.random_girl()
    else:
        image = mongo.random_boy()
    add_to_cache(image['_id'], gender, msg.author.id)
    return embeds.rate_embed(image['link'], image['rating'], image['count'])


@client.event
async def on_ready():
    print(client.user.name)
    await client.change_presence(game=discord.Game(name='.help'), status=discord.Status.dnd)


@client.event
async def on_message(msg):
    if msg.channel.id == config['DISCORD_CLIENT']['BOT_CHANNEL']:
        if msg.content.startswith('.girl'):
            await client.send_message(msg.channel, embed=prepare_image('girl', msg))

        elif msg.content.startswith('.boy'):
            await client.send_message(msg.channel,  embed=prepare_image('boy', msg))

        elif msg.content.startswith('.rate'):
            try:
                add_rating(
                    int(msg.content[len('.rate'):].strip()), msg.author.id)
                await client.send_message(msg.channel, '`Rating added.`')
            except KeyError:
                await client.send_message(msg.channel, '`Nothing to rate.`')
            except ValueError:
                await client.send_message(msg.channel, '`Rating must be between 1-10.`')

        elif msg.content.startswith('.upload album girl'):
            if msg.author.id == config['DISCORD_CLIENT']['ADMIN_ID']:
                mongo.upload_album(
                    msg.content[len('.upload album girl'):].strip())
            else:
                await client.send_message(msg.channel, '`You must be an administator to perform this command.`')

        elif msg.content.startswith('.upload album boy'):
            if msg.author.id == config['DISCORD_CLIENT']['ADMIN_ID']:
                mongo.upload_album(
                    msg.content[len('.upload album boy'):].strip(), girl=False)
            else:
                await client.send_message(msg.channel, '`You must be an administator to perform this command.`')

        elif msg.content.startswith('.top girls'):
            await client.send_message(msg.channel, embed=embeds.top_embed(mongo.top_girls()))

        elif msg.content.startswith('.top boys'):
            await client.send_message(msg.channel, embed=embeds.top_embed(mongo.top_boys()))

        elif msg.content.startswith('.help'):
            await client.send_message(msg.channel, embed=embeds.help_embed(msg))


client.run(config['DISCORD_CLIENT']['BOT_TOKEN'])
