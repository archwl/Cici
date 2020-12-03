'''
Essential functions for Cici
'''

import discord
import os
import aiosqlite
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter


class Essentials(commands.Cog):
    '''Essential functions for Cici'''
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, something: str):
        '''Makes the bot say something'''
        await ctx.send(something)

    @commands.is_owner()
    @commands.command()
    async def leave(self, ctx):
        '''Leaves the current server.'''
        leave_embed = discord.Embed(
            color=self.bot.embed_color,
            title=f'Goodbye, **{ctx.guild.name}**'
        )
        await ctx.send(embed=leave_embed)
        await ctx.guild.leave()

    @commands.is_owner()
    @commands.command(aliases=['shutdown'])
    async def close(self, ctx):
        close_embed = discord.Embed(
            color=self.bot.embed_color,
            title='Clossing session'
        )
        await ctx.send(embed=close_embed)
        await self.bot.close()

    @commands.command()
    async def ping(self, ctx):
        '''Pong!'''
        ping_embed = discord.Embed(
            color=self.bot.embed_color,
            title=f'{round(self.bot.latency * 1000)}ms'
        )
        await ctx.send(embed=ping_embed)

    @commands.is_owner()
    @commands.command()
    async def resetdb(self, ctx):
        '''Reset the system database'''
        if os.path.exists(self.bot.db_path):
            os.remove(self.bot.db_path)

        async with aiosqlite.connect(self.bot.db_path) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS user_prefixes (user_id integer, prefix text)')
            await db.execute('CREATE TABLE IF NOT EXISTS server_prefixes (server_id integer, prefix text)')
            await db.execute('CREATE TABLE IF NOT EXISTS global_prefixes (prefix text)')
            await db.commit()

    @commands.is_owner()
    @commands.command()
    async def reloadall(self, ctx):
        '''Reloads all extensions. '''
        initial_msg = await ctx.send('**Reloading...**')
        success = True
        try:
            self.bot.config = self.bot.load_config()
        except FileNotFoundError:
            success = False
            print('Configuration file does not exist. Reverting back to last working state')
        except Exception as e:
            success = False
            print('Something unexpected occured\n\n{e}')
        try:
            for module in self.bot.config['modules']:
                try:
                    self.bot.load_extension(module)
                except commands.ExtensionAlreadyLoaded:
                    self.bot.unload_extension(module)
                    self.bot.load_extension(module)
                except Exception as e:
                    await ctx.send(f'Failed: **{module}**\n```py\n{e}```')
                    success = False
        except Exception as e:
            await ctx.send(f'Something unexpected occured. Please check the configuration file at {self.bot.enclosing_dir}/config.json\n\n{e}')

        for module in os.listdir(f'{self.bot.enclosing_dir}/Modules'):
            if module.endswith('.py'):
                noext = module[:-3]
                try:
                    self.bot.load_extension(f'Modules.{noext}')
                except commands.ExtensionAlreadyLoaded:
                    self.bot.unload_extension(f'Modules.{noext}')
                    self.bot.load_extension(f'Modules.{noext}')

                except Exception as e:
                    await ctx.send(f'Failed: **{noext}**\n```py\n{e}```')
                    success = False
        if success:
            await initial_msg.add_reaction('✅')
        else:
            await initial_msg.add_reaction('‼️')

    @commands.is_owner()
    @commands.command()
    async def python(self, ctx, *, code: str):
        '''Evaluate python code'''
        cog = self.bot.get_cog('Jishaku')
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)


def setup(bot):
    bot.add_cog(Essentials(bot))

    silent_bool = bot.dict_bool_eval(bot.config, 'silent')
    if bot.dict_has(bot.config, 'extra_modules'):
        for module in bot.config['extra_modules']:
            try:
                bot.load_extension(module)
                if silent_bool:
                    print(f'Ready: {module}')
            except Exception as e:
                if silent_bool:
                    print(f'Failed: {module}\n{e}')

    if not bot.dict_bool_eval(bot.config, 'no_auto_load'):
        for module in os.listdir(f'{bot.enclosing_dir}/Modules'):
            if module.endswith('.py'):
                base_module = module[:-3]
                try:
                    bot.load_extension(f'Modules.{base_module}')
                    if silent_bool:
                        print(f'Ready: {base_module}')
                except Exception as e:
                    if silent_bool:
                        print(f'Failed: {base_module}\n{e}')
