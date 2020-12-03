'''
Fun & games
'''

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import sr_api
import asyncio
from typing import Optional
from io import BytesIO
from datetime import datetime


class Fun(commands.Cog):
    '''Fun & games'''
    def __init__(self, bot):
        self.bot = bot
        self.sr_client = sr_api.Client()
        self.last_deleted_message = dict()

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message: discord.Message):
        self.last_deleted_message[message.guild.id] = message

    @commands.command()
    async def dong(self, ctx):
        '''Is your dickus biggus?'''
        dong = ['8', '=']
        additional_size = random.randint(0, 15)
        mega_dong = random.choices([False, True], weights=(95, 5), k=1)
        mega_dong_owner = random.choices([False, True], weights=(80, 20), k=1)
        if additional_size < 3:
            dong_title = 'Get dick enlargement pills'
        elif additional_size < 5:
            dong_title = 'It\'s cute'
        else:
            dong_title = 'Nice cock'
        for i in range(additional_size):
            dong.append('=')
        if mega_dong[0] or await self.bot.is_owner(ctx.author) and mega_dong_owner[0]:
            await asyncio.sleep(0.4)
            await ctx.send('Oh no! Something went wrong:\n```py\ndiscord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\n' +
                           'In embed.description: Must be 2048 or fewer in length.```')
            return
        dong.append('D')
        dong_embed = discord.Embed(
            title=dong_title,
            color=0x2F3136,
            description=f'**{"".join(dong)}**'
            )

        dong_embed.set_footer(text=f'This dong belongs to {str(ctx.author)}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=dong_embed)

    @commands.command(name='ask', aliases=['?'])
    async def callback(self, ctx, *, message: str):
        '''Ask me something!'''
        await ctx.send(await self.sr_client.chatbot(message))

    @commands.command()
    @commands.max_concurrency(1, per=BucketType.channel, wait=False)
    async def chat(self, ctx):
        '''Chat with me!'''
        await ctx.send(embed=discord.Embed(title='You\'re now chatting with me! Say "bye" to stop.', color=0x2F3136))
        while True:
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content.lower() == 'bye' or msg.content.lower() == 'stop':
                break

            await ctx.send(await self.sr_client.chatbot(msg.content))
        await ctx.send('Bye!')

    @commands.command()
    @commands.max_concurrency(1, per=BucketType.channel, wait=False)
    async def cookie(self, ctx):
        '''Eat the cookie as fast as possible!'''
        first_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='Be the first to eat the cookie!'
            )
        second_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='3'
            )
        third_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='2'
            )
        fourth_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='1'
            )
        fifth_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='EAT!'
            )
        timeout_embed = discord.Embed(
            title=':cookie:',
            color=0x2F3136,
            description='No one ate the cookie on time! I get to keep it.'
            )

        message = await ctx.send(embed=first_embed)
        await asyncio.sleep(1)
        await message.edit(embed=second_embed)
        await asyncio.sleep(1)
        await message.edit(embed=third_embed)
        await asyncio.sleep(1)
        await message.edit(embed=fourth_embed)
        await asyncio.sleep(1)
        await message.edit(embed=fifth_embed)
        await message.add_reaction('🍪')

        def check(reaction, user):
            return user != message.author and str(reaction) == '🍪'

        try:
            start_time = datetime.utcnow()

            reaction, winner_user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await message.edit(embed=timeout_embed)
        else:
            final_embed = discord.Embed(
                title=':cookie:',
                color=0x2F3136,
                description=f'{winner_user.mention} ate the cookie first!\n`{(datetime.utcnow() - start_time).total_seconds()}s`'
            )
            await message.edit(embed=final_embed)

    @commands.command(name='8ball')
    async def magicball(self, ctx):
        '''The magic eight ball knows all.'''
        response_list = ['It is certain.',
                         'It is decidedly so.',
                         'Without a doubt.',
                         'Yes – definitely.',
                         'You may rely on it.',
                         'As I see it, yes.',
                         'Most likely.',
                         'Outlook good.',
                         'Yes.',
                         'Signs point to yes.',
                         'Reply hazy, try again.',
                         'Ask again later.',
                         'Better not tell you now.',
                         'Cannot predict now.',
                         'Concentrate and ask again.',
                         'Don\'t count on it.',
                         'My reply is no.',
                         'My sources say no.',
                         'Outlook not so good.',
                         'Very doubtful.']

        await ctx.send(embed=discord.Embed(color=self.bot.embed_color, title=random.choice(response_list)))

    @commands.command()
    async def joke(self, ctx):
        '''Get a random joke'''
        await ctx.send(embed=discord.Embed(color=self.bot.embed_color, title=await self.sr_client.get_joke))

    @commands.command()
    async def aniquote(self, ctx):
        '''Get a random anime quote'''
        aniquote = await self.sr_client.anime_quote()
        aniquote_embed = discord.Embed(
            title=aniquote.anime,
            description=f'“{aniquote.quote}” \n\n– {aniquote.character}',
            color=self.bot.embed_color
        )
        await ctx.send(embed=aniquote_embed)

    @commands.command()
    async def wasted(self, ctx, member: Optional[discord.User]):
        '''Rockstar wen eta gta 6??'''
        if member:
            image = self.sr_client.filter('wasted', str(member.avatar_url_as(format='png')))
        else:
            image = self.sr_client.filter('wasted', str(ctx.author.avatar_url_as(format='png')))
        bytes_image = BytesIO(await image.read())
        wasted_embed = discord.Embed(
            title='WASTED.',
            color=0x2F3136,
            )
        wasted_file = discord.File(bytes_image, filename='image.png')

        wasted_embed.set_image(url="attachment://image.png")
        await ctx.send(file=wasted_file, embed=wasted_embed)

    @commands.command()
    async def gay(self, ctx, member: Optional[discord.User]):
        '''Makes you gay.'''
        if member:
            image = self.sr_client.filter('gay', str(member.avatar_url_as(format='png')))
        else:
            image = self.sr_client.filter('gay', str(ctx.author.avatar_url_as(format='png')))
        bytes_image = BytesIO(await image.read())
        gay_embed = discord.Embed(
            title='lol gay',
            color=0x2F3136,
            )
        gay_file = discord.File(bytes_image, filename='image.png')

        gay_embed.set_image(url='attachment://image.png')
        await ctx.send(file=gay_file, embed=gay_embed)

    @commands.command()
    async def pixelate(self, ctx, member: Optional[discord.User]):
        '''ENHANCE. '''
        if member:
            image = self.sr_client.filter('pixelate', str(member.avatar_url_as(format='png')))
        else:
            image = self.sr_client.filter('pixelate', str(ctx.author.avatar_url_as(format='png')))
        bytes_image = BytesIO(await image.read())
        pixelate_embed = discord.Embed(
            title='moar jpeg',
            color=0x2F3136,
            )
        pixelate_file = discord.File(bytes_image, filename='image.png')

        pixelate_embed.set_image(url='attachment://image.png')
        await ctx.send(file=pixelate_file, embed=pixelate_embed)

    @commands.command()
    async def youtube(self, ctx, comment: str):
        '''fakes a YouTube comment'''
        image = self.sr_client.youtube_comment(str(ctx.author.avatar_url_as(format='png')), str(ctx.author.name), comment)
        bytes_image = BytesIO(await image.read())
        youtube_embed = discord.Embed(
            color=0x2F3136,
            )
        youtube_file = discord.File(bytes_image, filename='image.png')

        youtube_embed.set_image(url='attachment://image.png')
        await ctx.send(file=youtube_file, embed=youtube_embed)

    @commands.command()
    async def snipe(self, ctx):
        '''Snipe a deleted message'''
        if self.last_deleted_message:
            try:
                message = self.last_deleted_message[ctx.guild.id]
                snipe_embed = discord.Embed(
                    color=0x2F3136,
                    description=message.content
                )
                snipe_embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                snipe_embed.set_footer(text=f'Requested by {str(ctx.author)}', icon_url=ctx.author.avatar_url)
                await ctx.send(embed=snipe_embed)
            except Exception as e:
                await ctx.send(f'Couldn\'t display the sniped message, sorry\n```py\n{e}```')
        else:
            await ctx.send('There\'s nothing to snipe!')

    @commands.command()
    @commands.cooldown(1, 250, BucketType.channel)
    async def emote(self, ctx, member: discord.Member, number: Optional[int]):
        '''emote'''
        if number and number > 20:
            await ctx.message.add_reaction('🚫')
            return

        message = discord.utils.get(await ctx.channel.history(limit=100).flatten(), author=member)
        el = list(ctx.guild.emojis)
        rand_e_5 = random.choices(el, weights=None, cum_weights=None, k=number if number else 7)

        for i in self.bot.emojis:
            for j in rand_e_5:
                if i.id == j.id:
                    await message.add_reaction(i)

        await asyncio.sleep(0.3)


def setup(bot):
    bot.add_cog(Fun(bot))
