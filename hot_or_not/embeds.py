import discord


class Embeds(object):
    def __init__(self, client):
        self._client = client

    def create_embed(self):
        return discord.Embed(color=0xff3232). \
            set_author(name='Hot or Not', icon_url=self._client.user.avatar_url)

    def rate_embed(self, link, rating, count):
        embed = self.create_embed()
        embed.title = 'How to rate'
        embed.description = '`.rate 1-10 to rate this image`'
        embed.add_field(name='Average rating:', value=rating, inline=True)
        embed.add_field(name='Votes:', value=count, inline=True)
        embed.set_image(url=link)
        return embed

    def help_embed(self, msg):
        embed = self.create_embed()
        embed.title = 'Help Documentation'
        embed.description = '`Displays photos of boys and girls to rate.`'
        embed.add_field(name='Show girl', value='`.girl` - Display a girl to rate.', inline=False)
        embed.add_field(name='Show boy', value='`.boy` - Display a boy to rate.', inline=False)
        embed.add_field(
            name='rate', value='`.rate value` - Rate between 1-10.', inline=False)
        embed.add_field(name='Top five girls',
                        value='`.top girls` - Display top 5 rated girls.', inline=False)
        embed.add_field(name='Top five boys',
                        value='`.top boys` - Display top 5 rated boys.', inline=False)
        embed.set_thumbnail(url=msg.channel.server.icon_url)
        return embed

    def top_embed(self, tops):
        embed = self.create_embed()
        embed.title = '*TOP 5 HOTTEST*'
        count = 5
        for top in reversed(tops):
            embed.add_field(name='{}.'.format(count), value='`Rating: {} | Votes: {}` \
                [Imgur link]({})'.format(top['rating'], top['count'], top['link']), inline=False)
            count -= 1
        embed.set_image(url=tops[0]['link'])
        return embed
