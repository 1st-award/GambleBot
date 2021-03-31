import asyncio
import discord
import play_game as game
import os
import random
from discord.ext import commands

dirctory = os.path.dirname(__file__)
bot = commands.Bot(command_prefix='!')
join_players = []
s_status = 0


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
    user_mention = ctx.message.author.mention  # 플레이어의 멘션 언급
    msg = ctx.message.content.replace("!포커 ", "")  # 클라이언트의 메세지에서 !포커를 제거
    print(msg)

    if msg in "족보":
        file = dirctory + "\\k_poker_jokbo.jpg"
        await ctx.send(file=discord.File(file))


@bot.command()
async def 야추(ctx):
    global join_players  # 플레이어의 id를 리스트로 저장
    user_mention = ctx.message.author.mention  # 플레이어의 멘션 언급
    msg = ctx.message.content.replace("!야추 ", "")  # 클라이언트의 메세지에서 !야추를 제거
    # user_id= ctx.message.author.id# 플레이어의 id를 출력
    print(msg)

    if msg in "시작":  # 시작 프로그램
        join_players = ['<@!455957324624953354>']
        global s_status  # 0:시작, 1:준비, 2:준비완료, 3: 게임중
        if s_status == 1:
            await ctx.send("준비 시간입니다.")
        elif s_status == 2:
            await ctx.send("이미 시작하셨습니다.")
        else:
            s_status = 1
            await ctx.send("10초안에 '!야추 참여'를 입력하시고, 완료 후 !야추 시작완료를 입력해주세요.")
            await asyncio.sleep(3)
            s_status = 2
            await ctx.send("10초가 끝났습니다.")

    elif msg in "참여":  # 준비 프로그램
        if s_status == 1:
            if str(user_mention) in str(join_players):
                await ctx.send(format(user_mention) + "님은 이미 참가하셨습니다.")
            else:
                join_players.append(ctx.message.author.mention)
                print(join_players)
                await ctx.send(format(user_mention) + "님이 참가하셨습니다.")
        else:
            await ctx.send("참여 시간이 아닙니다.")

    elif msg in "시작완료":  # 게임 프로그램
        if s_status == 2:
            s_status = 3
            cnt = 0

            await ctx.send("모두 준비가 완료되었습니다. 게임을 시작합니다.")
            # await asyncio.sleep(3)
            await ctx.send("첫번째 순서를 뽑습니다.")
            first_gamer = random.randrange(len(join_players))
            await ctx.send(join_players[first_gamer] + "님이 첫번째 입니다.")
            temp = join_players.pop(first_gamer)
            join_players.insert(0, temp)
            temp = join_players
            temp = game.clean_str(str(temp), len(join_players) * 2)
            await ctx.send("순서는 " + temp + "입니다.\n" + join_players[0] + "님 시작해주세요.")
            # 게임시작
            while cnt < 12:
                for i in join_players:
                    dice = game.roll_dice()
                    dice = game.clean_str(dice, 0)
                    await ctx.send(i + "님의 주사위 " + dice + "   제한시간: 30초")
                    await asyncio.sleep(10)
                    await ctx.send(i + " 20초 남앗습니다.")
                    await asyncio.sleep(10)
                    await ctx.send(i + " 10초 남앗습니다.")
                    await asyncio.sleep(10)
                    await ctx.send(i + " 시간이 끝났습니다. 다음 차례로 넘어갑니다.")

                cnt += 1
                print(cnt)
        elif msg in "선택":  # 선택 프로그램
            msg = ctx.message.content.replace("선택 ", "")
            game.select(int(msg))

        else:
            await ctx.send("게임시작 시간이 아닙니다.")

    elif msg in "강제다시시작":
        s_status = 0
        await ctx.send("처음부터 다시 시작해 주세요.")


@bot.command()
async def test(ctx):
    print(ctx.message.author.id)


# 봇 토큰 유출 방지를 위해 Heroku에 토큰 저장
# access_token = os.environ["BOT_TOKEN"]
# bot.run(access_token)
bot.run('NDU1OTU3MzI0NjI0OTUzMzU0.Wx9RWQ.7ASqG1ETqZF1mV7h1iEQ_RfyH1k')
