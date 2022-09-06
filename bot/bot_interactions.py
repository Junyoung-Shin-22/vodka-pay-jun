import discord
import re

from db.db import *

_CALLBACKS = {}

def add_callback(label):
    def _inner_add_callback(callback):
        _CALLBACKS[label] = callback

        return callback
    return _inner_add_callback

class InteractionButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction):
        if self.label in _CALLBACKS:
            await _CALLBACKS[self.label](self, interaction)
        else:
            await _CALLBACKS['default'](self, interaction)

@add_callback('default')
async def _default_callback(item, interaction):
    response = interaction.response
    
    await response.send_message(content=item.label, ephemeral=True)

@add_callback('도움말')
async def _help_callback(item, interaction):
    response = interaction.response

    embed = discord.Embed()
    embed.title = '도움말'
    embed.description = """도움말 내용"""
    
    await response.send_message(embed=embed, ephemeral=True)

@add_callback('가입하기')
async def _sign_in_callback(item, interaction):
    user = interaction.user
    response = interaction.response

    # User DB 읽기
    users_id = db_get_users_id()
    if str(user.id) in users_id: # 이미 가입한 유저
        embed_main = discord.Embed(
        title='가입하기',
        description = f'`{str(user)}`님은 이미 가입된 유저입니다!')
        await response.send_message(embed=embed_main, ephemeral=True)

        return
    
    # 메인 채널에서 가입 시작
    embed_main = discord.Embed(
        title='가입하기',
        description = f'`{str(user)}`님, 보드카페이 가입을 도와드릴게요! DM을 확인해주세요!')
    await response.send_message(embed=embed_main, ephemeral=True)
    
    flag = False # 가입 성공 여부 flag

    while not flag:
        # DM에서 계좌 입력받기
        dm_channel = await user.create_dm()
        embed_dm_start = discord.Embed(
            title='가입하기',
            description = '''월말 정산에 필요한 계좌번호를 1분 내로 입력해주세요.
            (예시: 대구 508141574830)''')
        await dm_channel.send(embed=embed_dm_start)
        
        # 계좌 입력 정규표현식 검사 및 1분 대기
        client = interaction.client
        def _check_account(message):
            return message.channel == dm_channel and re.fullmatch(r'[가-힣]+ \d+', message.content)
        try:
            message_account = await client.wait_for('message', check=_check_account, timeout=60)
        except:
            embed_dm_timeout = discord.Embed(
            title='가입하기',
            description = '입력 시간이 초과되었습니다. 가입을 처음부터 다시 진행해주세요')
            await dm_channel.send(embed=embed_dm_timeout)

            return
        
        # 입력한 계좌 확인받기
        embed_dm_confirm = discord.Embed(
            title='가입하기',
            description = f'사용하실 계좌가 `{message_account.content}`가 맞나요? 1분 내로 반응을 눌러주세요.')
        message_dm_confirm = await dm_channel.send(embed=embed_dm_confirm)
        await message_dm_confirm.add_reaction('⭕')
        await message_dm_confirm.add_reaction('❌')

        # 반응 확인 및 1분 대기
        def _check_confirm(reaction, usr):
            return usr == user and reaction.emoji in ('⭕', '❌')
        try:
            reaction, _ = await client.wait_for('reaction_add', check=_check_confirm, timeout=60)
        except:
            embed_dm_timeout = discord.Embed(
            title='가입하기',
            description = '입력 시간이 초과되었습니다. 가입을 처음부터 다시 진행해주세요')
            await dm_channel.send(embed=embed_dm_timeout)

            return
        
        if reaction.emoji == '⭕':
            flag = True

            db_add_user(str(user.id), message_account.content)

            embed_dm_success = discord.Embed(
            title='가입하기',
            description = '보드카페이 가입에 성공하였습니다!')
            await dm_channel.send(embed=embed_dm_success)
