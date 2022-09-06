import discord
from discord.ext import commands


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
            discord.ui.Button(label='도움말'),
            discord.ui.Button(label='가입하기'),
            discord.ui.Button(label='정산 등록하기'),
            discord.ui.Button(label='정산 참여하기'),
        ]
    
    for item in items:
        view.add_item(item)

    await ctx.channel.send(view=view)