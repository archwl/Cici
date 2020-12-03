'''
Information & help
'''

from os import path
import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand


class Info(commands.Cog):
    '''Information & help'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def cog_unload(self):
        self.bot.get_command('help').hidden = False
        self.bot.help_command = DefaultHelpCommand()

    @commands.command()
    async def invite(self, ctx):
        '''Invite me to your server!'''
        invite_embed = discord.Embed(
            color=self.bot.embed_color,
            title='Invite me to your server!',
            url='https://discord.com/api/oauth2/authorize?client_id=760285595259502603&permissions=19456&scope=bot'
        )
        await ctx.send(embed=invite_embed)

    @commands.command()
    async def source(self, ctx):
        '''Source for Cici'''
        source_embed = discord.Embed(
            color=self.bot.embed_color,
            title='Cici is currently **not** open source.',
            )
        await ctx.send(embed=source_embed)


def setup(bot):
    bot.add_cog(Info(bot))
