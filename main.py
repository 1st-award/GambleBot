import asyncio
import discord
import logging
import os
import random
from discord.ext import commands
from PIL import Image

dirctory= os.path.dirname(__file__)
bot = commands.Bot(command_prefix='!')
join_players= []
s_status= 0
all_ready= 0

@bot.event
async def on_ready():  # 디스코드 봇 로그인
    print('Logged in as \nName: {}\n  ID: {}'.format(bot.user.name, bot.user.id))
    print('=' * 10)  # 상태 메세지 생성
    guilds = await bot.fetch_guilds(limit=150).flatten()
    print(guilds)
    await bot.change_presence(activity=discord.Activity(name="!도움말", type=0))

# !도움말을 위한 기존에 있는 help 제거
bot.remove_command('help')
############################
@bot.command()
async def 포커(ctx):
    user_mention = ctx.message.author.mention #플레이어의 멘션 언급
    msg =(ctx.message.content).replace("!포커 ","") #클라이언트의 메세지에서 !포커를 제거
    print(msg)

    if msg in "족보":
        file= dirctory+ "\\k_poker_jokbo.jpg"
        await ctx.send(file=discord.File(file))
    
@bot.command()
async def 야추(ctx):
    global join_players #플레이어의 id를 리스트로 저장
    user_mention = ctx.message.author.mention #플레이어의 멘션 언급
    msg =(ctx.message.content).replace("!야추 ","") #클라이언트의 메세지에서 !야추를 제거
    #user_id= ctx.message.author.id# 플레이어의 id를 출력
    print(msg)
    
    if msg in "시작": #시작 프로그램
        join_players= []
        global all_ready #0: 준비안됨, 1: 준비완료
        global s_status #0:시작, 1:준비, 2:게임중
        if s_status == 1:
            await ctx.send("준비 시간입니다.")
        elif s_status == 2:
            await ctx.send("이미 시작하셨습니다.")
        else:
            s_status= 1
            await ctx.send("10초안에 '!야추 참여'를 입력하시고, 완료 후 !야추 시작완료를 입력해주세요.")
            await asyncio.sleep(5)
            s_status= 0
            all_ready= 1
            await ctx.send("10초가 끝났습니다.")
        
    elif msg in "참여": #준비 프로그램
        if s_status== 1:
            if str(user_mention) in str(join_players):
                await ctx.send(format(user_mention)+"님은 이미 참가하셨습니다.")
            else:
                join_players.append(ctx.message.author.mention)
                await ctx.send(format(user_mention)+"님이 참가하셨습니다.")
        else:
            await ctx.send("참여 시간이 아닙니다.")

    elif msg in "시작완료": #게임 프로그램
        s_status= 2
        first_gamer= 0
        
        if all_ready==1:
            temp= []
            print(len(join_players))
            print(join_players)
            
            await ctx.send("모두 준비가 완료되었습니다. 게임을 시작합니다.")
            #await asyncio.sleep(3)
            await ctx.send("첫번째 순서를 뽑습니다.")
            first_gamer= random.randrange(len(join_players))
            await ctx.send(join_players[first_gamer] + "님이 첫번째 입니다.")
            if first_gamer>0:
                temp= join_players[:first_gamer]
                temp= temp.strip('[]')
                temp= temp.replace("'", "", len(temp)*2)
                print(temp)
                del join_players[:first_gamer]
                print(join_players)
                join_players.append(temp)
                print(join_players)
                join_players= str(join_players)
                print(join_players)
                join_players= join_players.strip('[]')
                print(join_players)
                join_players= join_players.replace("'", "", len(join_players)*2)
                print(join_players)
            else:
                join_players= str(join_players)
                print(join_players)
                join_players= join_players.strip('[]')
                print(join_players)
                join_players= join_players.replace("'", "", len(join_players)*2)
                print(join_players)
                
            await ctx.send("순서는 "+ str(join_players)+ "입니다.")
        else:
            await ctx.send("게임시작 시간이 아닙니다.")

    elif msg in "강제다시시작":
        s_status= 0
        await ctx.send("처음부터 다시 시작해 주세요.")

@bot.command()
async def 참가(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    
@bot.command()
async def 나가기(ctx):
    await ctx.voice_client.disconnect()
    
@bot.command()
async def test(ctx):
    print(ctx.message.author.id)

#기본적인 정보들을 로그에 출력해줍니다.
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)

# 봇 토큰 유출 방지를 위해 Heroku에 토큰 저장
#access_token = os.environ["BOT_TOKEN"]
#bot.run(access_token)
bot.run('')
