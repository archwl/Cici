'''
Cici
Modules.error-handling
'''

from typing import Optional
import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def try_send(self, ctx, embed: discord.Embed = None, *args, **kwargs) -> Optional[discord.Message]:
        '''Tries to send the given text to ctx, but failing that, tries to send it to the author
        instead. If it fails that too, it just stays silent.'''
        try:
            return await ctx.send(embed=embed, *args, **kwargs)
        except discord.Forbidden:
            try:
                return await ctx.author.send(embed=embed, *args, **kwargs)
            except discord.Forbidden:
                pass
        except discord.NotFound:
            pass
        return None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored_errors = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored_errors):
            return

        setattr(ctx, 'original_author_id', getattr(ctx, 'original_author_id', ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()

        # Command is on Cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            return await self.try_send(ctx, discord.Embed(title='This command is on cooldown', description=f'**Try again in `{int(error.retry_after)}` seconds**'), delete_after=15.0)

        # Missing argument
        elif isinstance(error, commands.MissingRequiredArgument):
            return await self.try_send(ctx, discord.Embed(title=str(error)))

        # Missing Permissions
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f'You\'re missing the required permission: `{error.missing_perms[0]}`')

        # Missing Permissions
        elif isinstance(error, commands.BotMissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f'I\'m missing the required permission: `{error.missing_perms[0]}`')

        # Discord Forbidden
        elif isinstance(error, discord.Forbidden):
            return await self.send_to_ctx_or_author(ctx, 'I\'m being rate limited by the API.')

        # User who invoked command is not owner
        elif isinstance(error, commands.NotOwner):
            return await self.send_to_ctx_or_author(ctx, 'You can\'t do that, sweetie!')

        # Maximum concurrency reached
        elif isinstance(error, commands.MaxConcurrencyReached):
            return await self.send_to_ctx_or_author(ctx, 'Someone is already using this command in this channel. Please wait for them to finish!')

        raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
