import discord
import asyncio
import configparser
from collections import OrderedDict
import pymongo
from mongo import Mongo
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

config = configparser.ConfigParser()
config.read('config.ini')
mongo = Mongo(config['IMGUR_CLIENT']['CLIENT_ID'])
client = discord.Client()
rating_cache = OrderedDict()


def create_embed():
    return discord.Embed(color=0xff3232). \
        set_author(name='Hot or Not', icon_url=client.user.avatar_url)


def rate_embed(link, rating, count):
    embed = create_embed()
    embed.title = '*How to rate*'
    embed.description = '`.rate 1-10 to rate this image`'
    embed.add_field(name='Average rating:', value=rating, inline=True)
    embed.add_field(name='Votes:', value=count, inline=True)
    embed.set_image(url=link)
    return embed


def help_embed(msg):
    embed = create_embed()
    embed.title = '*Instructions*'
    embed.description = '`displays photos of boys and girls to rate.`'
    embed.add_field(name='Show girl:', value='`.girl`', inline=True)
    embed.add_field(name='Show boy:', value='`.boy`', inline=True)
    embed.add_field(
        name='rate:', value='`.rate value - value must be 1-10`', inline=True)
    embed.set_thumbnail(url=msg.channel.server.icon_url)
    return embed


def top_embed(tops):
    embed = create_embed()
    embed.title = '*TOP 5 HOTTEST*'
    count = 5
    for top in reversed(tops):
        embed.add_field(name='{}.'.format(count), value='`Rating: {} | Votes: {}` \
            [Imgur link]({})'.format(top['rating'], top['count'],top['link']), inline=False)
        count -= 1
    embed.set_image(url=tops[0]['link'])
    return embed


def add_rating(new_rating, requester):
    if new_rating <= 10 and new_rating > 0:
        if rating_cache[requester][1] == 'girl':
            mongo.update_girl(rating_cache[requester][0], new_rating)
        else:
            mongo.update_boy(rating_cache[requester][0], new_rating)
        del rating_cache[requester]
    else:
        raise ValueError('Rating must be between 1-10.')


def prepare_image(gender, msg):
    if gender == 'girl':
        image = mongo.random_girl()
    else:
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
        if gender == 'girl':
            rating_cache[msg.author.id] = (hash, 'girl')
        else:
            rating_cache[msg.author.id] = (hash, 'boy')
    else:
        rating_cache.popitem(last=False)
    return rate_embed(url, rating, count)


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
                await client.send_message(msg.channel, '`Rating must be between 0-10.`')

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
            tops = mongo.top_girls()
            embed = top_embed(tops)
            await client.send_message(msg.channel, embed=embed)

        elif msg.content.startswith('.top boys'):
            tops = mongo.top_boys()
            embed = top_embed(tops)
            await client.send_message(msg.channel, embed=embed)

        elif msg.content.startswith('.help'):
            await client.send_message(msg.channel, embed=help_embed(msg))


client.run(config['DISCORD_CLIENT']['BOT_TOKEN'])
