from discord.ext import commands
import aiosqlite


class Prefix(commands.Cog):
    '''Custom per-user and per-server prefixes'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def myprefix(self, ctx, prefix: str):
        '''Set a personal prefix'''
        try:
            if self.bot.dict_bool_eval(self.bot.config, 'max_prefix_length'):
                max_prefix_length = int(self.bot.config, 'max_prefix_length')
            else:
                max_prefix_length = 15
        except Exception:
            max_prefix_length = 15

        if len(prefix) < max_prefix_length:
            async with aiosqlite.connect(self.bot.db_path) as db:
                await db.execute(f'DELETE from user_prefixes where user_id = {ctx.author.id}')
                await db.execute('REPLACE INTO user_prefixes (user_id, prefix) VALUES(?, ?)', (ctx.author.id, prefix))
                await db.commit()
                # aiosqlite handles closing connections automatically
            await ctx.send(f'**{prefix}** is now your prefix.')
        elif len(prefix) > max_prefix_length:
            await ctx.send(f'Your prefix cannot exceed **{max_prefix_length}** characters.')
        else:
            await ctx.send(f'**{prefix}** cannot be set as a prefix.')

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def serverprefix(self, ctx, prefix: str):
        '''Set a prefix for the current server'''
        try:
            if self.bot.dict_bool_eval(self.bot.config, 'max_prefix_length'):
                max_prefix_length = int(self.bot.config, 'max_prefix_length')
            else:
                max_prefix_length = 15
        except Exception:
            max_prefix_length = 15

        if len(prefix) < max_prefix_length:
            async with aiosqlite.connect(self.bot.db_path) as db:
                await db.execute(f'DELETE from server_prefixes where server_id = {ctx.guild.id}')
                await db.execute('REPLACE INTO server_prefixes (server_id, prefix) VALUES(?, ?)', (ctx.guild.id, prefix))
                await db.commit()
                # aiosqlite handles closing connections automatically
            await ctx.send(f'**{prefix}** is now the prefix for **{ctx.guild.name}**')
        elif len(prefix) > max_prefix_length:
            await ctx.send(f'Server prefix cannot exceed **{max_prefix_length}** characters.')
        else:
            await ctx.send(f'**{prefix}** cannot be set as a prefix')


def setup(bot):
    if bot.dict_bool_eval(bot.config, 'custom_prefixes'):
        bot.add_cog(Prefix(bot))
