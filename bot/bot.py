import discord
from discord.ext import commands

from .bot_commands import COMMANDS

import os

_PATH = os.path.dirname(os.path.realpath(__file__))

_PREFIX = '/vp '
_INTENTS = discord.Intents.all()
BOT = commands.Bot(command_prefix=_PREFIX, intents=_INTENTS)

with open(os.path.join(_PATH, 'bot-token.txt')) as f:
    TOKEN = f.read()

@BOT.event
async def on_ready():
    print(f"{str(BOT.user)} is ready.")

for command in COMMANDS:
    BOT.add_command(command)

if __name__ == '__main__':
    BOT.run(TOKEN)