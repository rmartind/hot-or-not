import discord
import random
import asyncio
import configparser
from pymongo import MongoClient
import pymongo
from imgur import Imgur
from collections import OrderedDict


config = configparser.ConfigParser()
config.read('config.ini')

imgur_client_id = config['IMGUR_CLIENT']['CLIENT_ID']
imgur = Imgur(imgur_client_id)

client = discord.Client()

mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client.hotornot
girl_collection = db.girls

rating_cache = OrderedDict()

def create_embed(link, rating, msg):
    embed = discord.Embed(
        title='*How to rate*', description='`.rate 1-10 to rate this image`', color=0x00BFFF, timestamp=msg.timestamp)
    embed.set_author(name='Hot or Not')
    embed.add_field(name='Average rating:', value=rating, inline=True)
    embed.set_image(url=link)
    embed.set_footer(text='sent')
    return embed


@client.event
async def on_ready():
    print(client.user.name)


@client.event
async def on_message(msg):
    if msg.channel.id == config['DISCORD_CLIENT']['BOT_CHANNEL']:
        if msg.content.startswith('.girl'):

           
            count = girl_collection.count()
            number = random.randrange(count)
            image = girl_collection.find().limit(1).skip(number)

            hash = None
            url = None
            rating = None
            for e in image:
                url = e['link']
                rating = e['rating']
                hash = e['_id']

            if len(rating_cache) < 4:
                rating_cache[msg.author.id] = hash
            else:
                rating_cache.popitem()

            embed = create_embed(url, rating, msg)
            await client.send_message(msg.channel, embed=embed)

        elif msg.content.startswith('.boy'):
            pass

        elif msg.content.startswith('.rate'):
            try: 
                hash = rating_cache[msg.author.id]
                image = girl_collection.find_one({'_id': hash})
                print(image)


                del rating_cache[msg.author.id]
                await client.send_message(msg.channel, 'Rating added.')

            except KeyError:
                await client.send_message(msg.channel, 'Nothing to rate')
              

        elif msg.content.startswith('.upload album'):
            if msg.author.id == '537741349961859099':
                hash = msg.content[len('.upload album'):].strip()
                images = imgur.album_images(hash)['data']
                for image in images:
                    girl = {
                        '_id': image['id'],
                        'rating': 0.0,
                        'count': 0,
                        'link': image['link']
                    }

                    try:
                        girl_collection.insert_one(girl)
                    except pymongo.errors.DuplicateKeyError:
                        continue
            else:
                await client.send_message(msg.channel, 'You must be an administator to perform this command.')
        elif msg.content.startswith('.upload image'):
            if msg.author.id == '537741349961859099':
                pass


client.run(config['DISCORD_CLIENT']['BOT_TOKEN'])
