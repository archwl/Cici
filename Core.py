'''
The heart of Cici
'''

import discord
import os
import json
import aiosqlite
from functools import lru_cache
from aiohttp import ClientSession
from discord.ext.commands import Bot

enclosing_dir = os.path.dirname(os.path.realpath(__file__))


def dict_bool_eval(_dict, _key):
    return _key in _dict and bool(_key)


def dict_has(_dict, _key):
    return _key in _dict


def load_config():
    try:
        with open(f'{enclosing_dir}/config.json') as config_json:
            try:
                return json.load(config_json)
            except Exception as exception:
                print(f'Bad configuration file. Exiting...\n{exception}')
                raise SystemExit(1)
    except FileNotFoundError:
        print('Configuration file not found. Exiting...')
        raise SystemExit(1)


config = load_config()
db_path = f'{enclosing_dir}/data.db'


class Cici(Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.load_config = load_config
        self.dict_bool_eval = dict_bool_eval
        self.dict_has = dict_has
        self.config = load_config()
        self.enclosing_dir = enclosing_dir
        self.db_path = db_path
        self.embed_color = int(config['embed_color']) if dict_has(config, 'embed_color') else 0x2F3136

    async def start(self, *args, **kwargs):
        self.session = ClientSession()
        if dict_has(config, 'bot_token'):
            await super().start(self.config['bot_token'], *args, **kwargs)
        else:
            print('Couldn\'t find bot token in the configuration file. Exiting...')
            raise SystemExit(1)

    async def close(self):
        await self.session.close()
        await super().close()


@lru_cache(maxsize=12)
async def get_prefix(bot, message):
    prefixes = config['prefix_list'] if dict_has(config, 'prefix_list') else ['cc!']
    async with aiosqlite.connect(bot.db_path) as db:
        try:
            async with db.execute(f'SELECT prefix from user_prefixes WHERE user_id = {message.author.id}') as cursor:
                prefixes.append(''.join(await cursor.fetchone()))
        except Exception:
            pass
        try:
            async with db.execute(f'SELECT prefix from server_prefixes WHERE server_id = {message.guild.id}') as cursor:
                prefixes.append(''.join(await cursor.fetchone()))
        except Exception:
            pass
    return prefixes


bot = Cici(
    command_prefix=get_prefix,
    description='Cici',
    intents=discord.Intents.all()
    )


@bot.event
async def on_ready():
    if dict_bool_eval(config, 'silent'):
        print('Connected to Discord!')
    return True


def start_cici():
    bot.load_extension('Essentials')
    bot.run()


if __name__ == '__main__':
    start_cici()
