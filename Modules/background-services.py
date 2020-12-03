'''
Cici
Modules.background-services
'''

from discord.ext import commands, tasks
import json


class Background_services(commands.Cog, name='Background services'):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def refresh_config(self):
        try:
            with open(f'{self.bot.enclosing_dir}/config.json') as f:
                self.bot.config = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f'Invalid config.\n\n{e}')

    @commands.Cog.listener()
    async def on_ready(self):
        self.refresh_config.start()


def setup(bot):
    bot.add_cog(Background_services(bot))
