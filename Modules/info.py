'''
Information & help
'''

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from typing import Optional


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

    @commands.command(aliases=['github'])
    async def source(self, ctx):
        '''Source for Cici'''
        source_embed = discord.Embed(
            color=self.bot.embed_color,
            title='https://github.com/archwl/Cici',
            )
        await ctx.send(embed=source_embed)

    @commands.command(aliases=['commands'])
    async def help(self, ctx, cog_or_command: Optional[str]):
        '''Shows this message'''
        if not cog_or_command:
            help_embed=discord.Embed(
                color=self.bot.embed_color,
                title='Cici'
                )
            cogs_desc = ''
            for x in self.bot.cogs:
                cogs_desc += (f'• **{x}**\n')
            help_embed.add_field(name='Modules:', value=cogs_desc[0:len(cogs_desc)-1],inline=True)
            help_embed.add_field(name='placeholder', value='[Invite me](https://discord.com/api/oauth2/authorize?client_id=749613150701092984&permissions=329792&scope=bot)')
            help_embed.set_footer(text='Use cc!help <command/category> for more information.')
            cmds_desc = ''
            for y in self.bot.walk_commands():
                if not y.cog_name and not y.hidden:
                    cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
            await ctx.send(embed=help_embed)
        else:
            found = False
            for x in self.bot.cogs:
                if x == cog_or_command:
                    help_embed=discord.Embed(color=self.bot.embed_color, title=cog_or_command, description=self.bot.cogs[cog_or_command].__doc__)
                    for c in self.bot.get_cog(cog_or_command).get_commands():
                        if not c.hidden:
                            help_embed.add_field(name=c.name,value=c.help,inline=False)
                    found = True
            if not found:
                command = None
                for x in self.bot.walk_commands():
                    if not x.hidden and x.name == cog_or_command:
                        command = x
                    elif x.name == cog_or_command:
                        await ctx.send(embed=discord.Embed(color=self.bot.embed_color, title='You shouldn\'t be seeing that.'))
                if command:
                    help_embed = discord.Embed(
                        color=self.bot.embed_color,
                        title=f'{command.qualified_name} {command.signature if command.signature else ""}',
                        description=command.help if command.help else f'There is no description for **{command.name}**'
                        )
                    await ctx.send(embed=help_embed)
            else:
                await ctx.send(embed=help_embed)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Info(bot))
