from typing import Any
import os
import discord
import pymongo
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import motor.motor_asyncio


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.all()

bot = commands.Bot(command_prefix="!", intents=intents, application_id="1193950006714040461")

# MongoDB 클라이언트 연결
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Usim:1234@cluster0.2mpijnh.mongodb.net/?retryWrites=true&w=majority")
db = client.shmpyo

@bot.event
async def on_ready():
    channel = bot.get_channel(1284347203204415539)
    await channel.send(content="버블봇이 준비되었습니다")
    await bot.tree.sync()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="쉼표 shmpyo"),
        status=discord.Status.idle
    )
    print("봇 준비완료")

    # MongoDB Change Stream 설정
    asyncio.create_task(monitor_db_changes())

@bot.event
async def on_member_join(member):

    role_id = 1193969637226987600
    role = member.guild.get_role(role_id)

    if role:
        await member.add_roles(role)





@bot.event
async def on_message(message):

    channel_id = 1193969935593001091
    if message.channel.id == channel_id:
        await message.delete()

@bot.tree.command(name="인증하기", description="쉼표샵을 이용하기 위한 인증을 진행합니다")
async def password(interaction: discord.Interaction):
    channelId = 1193969935593001091
    if interaction.channel_id == channelId:
        button = PleaseVerify("인증 시작하기")
        view = discord.ui.View()
        view.add_item(button)
        embed = discord.Embed(color=0x2c4bce, title="안녕하세요, 쉼표샵입니다 👋", description=f"반가워요, {interaction.user.mention}님! 쉼표샵을 이용하기 위해선 인증이 필요해요.\n아래 **`인증 시작하기`** 버튼을 눌러보세요!")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        NotAllow = discord.Embed(color=0x2c4bce, title="🚨 오류가 발생했어요", description=f"해당 명령어는 <#{channelId}> 채널에서만 사용할 수 있어요")
        await interaction.response.send_message(embed=NotAllow, ephemeral=True)


class PleaseVerify(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.gray, emoji="📑")

    async def callback(self, interaction):
        user_data = await db.userinfo.find_one({"discordId": str(interaction.user.id)})
        if not user_data:
            await interaction.response.send_modal(DillyMadePay())
        else:
            embed = discord.Embed(color=0x2c4bce, title="🚨 오류가 발생했어요", description=f"이미 인증을 요청 중이시거나, 인증을 완료하신 것 같아요")
            await interaction.response.edit_message(embed=embed, view=None)

class DillyMadePay(discord.ui.Modal, title="shmpyo# Verify"):
    RBLXName = discord.ui.TextInput(
        label="로블록스 닉네임을 알려주세요",
        placeholder="닉네임 이외엔 다른 문자를 삽입하지 마세요.",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(
            color=0x2c4bce,
            title="알려주신 정보를 확인 할게요 📃",
            description="입력하신 정보가 맞나요?\n입력하신 정보가 맞다면 **`다음`**을 눌러주세요!"
        )
        
        button = StartVr("다음", user.name)

        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.edit_message(embed=embed, view=view)
                

class StartVr(discord.ui.Button):
    def __init__(self, label, rblox):
        super().__init__(label=label, style=discord.ButtonStyle.gray, emoji="✅")
        self.rblox = rblox

    async def callback(self, interaction):
        existing_data = await db.verify.find_one({"discordId": str(interaction.user.id)})
        if existing_data:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title="🚨 오류가 발생했어요",
                description="해당 계정은 이미 인증 진행 중이에요."
            )
            button = Cancel("인증 취소하기", existing_data.get("discordId"))
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await db.verify.insert_one({
                "plrName": self.rblox,
                "discordId": str(interaction.user.id),
                "discordName": interaction.user.name
            })
            embed = discord.Embed(color=0x2c4bce, title="✅ 인게임 본인인증을 완료해 주세요!", description=f"{self.rblox}님의 본인확인을 위해,\n아래 **`인게임 본인인증`** 버튼을 눌러 인게임 본인인증을 완료해 주세요!")
            button = discord.ui.Button(label="인게임 본인인증", style=discord.ButtonStyle.blurple, emoji="✅", url="https://www.roblox.com/ko/games/97269068004341/unnamed")
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.edit_message(embed=embed, view=view)


class Cancel(discord.ui.Button):
    def __init__(self, label, rblox):
        super().__init__(label=label, style=discord.ButtonStyle.red, emoji="💥")
        self.rblox = rblox

    async def callback(self, interaction):
        await interaction.response.send_message(f"<@{self.rblox}>님의 인증이 취소되었어요.\n재인증을 시도하시려면, `/인증하기` 명령어를 이용해주세요!", ephemeral=True)
        await db.verify.delete_one({"discordId": self.rblox})
        self.disabled = True


as_token = os.environ['BOT_TOKEN']
bot.run(as_token)
