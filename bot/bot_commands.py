import discord
from discord.ext import commands

from .bot_interactions import *
from db.db import _URL

COMMANDS = []
def append_command(command):
    COMMANDS.append(command)
    return command

@append_command
@commands.command(name='hello')
async def _hello(ctx):
    await ctx.channel.send('hello, vodka games!')

@append_command
@commands.command(name='.')
async def _main(ctx):
    view = discord.ui.View()
    items =\
        [
            InteractionButton(label='도움말'),
            InteractionButton(label='가입하기'),
            InteractionButton(label='정산 등록하기'),
            InteractionButton(label='정산 참여하기'),
            InteractionButton(label='장부 확인하기', url=_URL),
        ]
    
    for item in items:
        view.add_item(item)

    await ctx.channel.send(view=view)