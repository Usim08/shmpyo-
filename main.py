from typing import Any
import discord
import random
import os
from discord.interactions import Interaction
import pymongo
from discord.ext import commands
from discord import DMChannel
from discord.ui import Button, View
from discord.ui import Select, View
from discord.ui import Button, Select
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.all()

bot = commands.Bot(command_prefix="!", intents=intents, application_id="1193950006714040461")


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new client and connect to the server
client = pymongo.MongoClient("mongodb+srv://Usim:1234@cluster0.2mpijnh.mongodb.net/?retryWrites=true&w=majority")
db = client.UlsanVerify
Dilly_DB = client.PayNumber


@bot.event
async def on_ready():
    channel = bot.get_channel(1183426803889602631)
    await channel.send(content="울산봇이 준비되었습니다")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="DILLY, 울산"))
    print("봇 준비완료")

@bot.event
async def on_member_join(member):

    role_id = 1183361847034921050
    role = member.guild.get_role(role_id)

    if role:
        await member.add_roles(role)



@bot.tree.command(name="관리자전용", description="해당 슬래시는 울산광역시 관리자만 이용할 수 있어요")
async def password(interaction: discord.Interaction):
    if str(interaction.user.id) == str(751835293924982957):
        viewww = SelectAdmin()
        await interaction.response.send_message("선택사항을 선택하세요", view=viewww, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"{interaction.user.mention}님은 공지를 작성할 권한이 없어요")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SelectAdmin(View):
    @discord.ui.select(
        placeholder="선택사항 선택",
        options=[
            discord.SelectOption(
                label="서버 오픈하기",
                value='1',
                description="서버를 오픈합니다",
                emoji="🔑"
            ),
            discord.SelectOption(
                label="공지하기",
                value='2',
                description="전체 사용자들에게 다이렉트 메세지로 공지를 전송합니다",
                emoji="📣"
            ),
            discord.SelectOption(
                label="미전입자 공지하기",
                value='3',
                description="미전입자들에게 다이렉트 메세지로 공지를 전송합니다",
                emoji="📣"
            ),
            discord.SelectOption(
                label="인증데이터 삭제",
                value='4',
                description="인증된 유저의 데이터를 삭제합니다",
                emoji="🗑"
            ),
            discord.SelectOption(
                label="후원금 정산",
                value='5',
                description="후원금을 정산합니다",
                emoji="💙"
            ),
            discord.SelectOption(
                label="공문 안내",
                value='6',
                description="전체 사업자들에게 알림을 보냅니다",
                emoji="📣"
            ),
            discord.SelectOption(
                label="개인 공문 안내",
                value='7',
                description="개인 사업자들에게 알림을 보냅니다",
                emoji="📣"
            ),
            discord.SelectOption(
                label="도공단 합격",
                value='8',
                description="도공단에서 합격을 시킵니다",
                emoji="🚗"
            ),
            discord.SelectOption(
                label="팩션 서버 오픈",
                value='9',
                description="팩션 인원들에게만 오픈 알림을 보냅니다",
                emoji="💌"
            )
        ]
    )


    async def select_callback(self, interaction, select):
        select.disabled = True
        
        if select.values[0] == '1':
            channel = bot.get_channel(1183747394714742854)
            Openembed= discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 서버가 오픈되었습니다", description="> **서버가 정상적으로 오픈되었습니다**\n\n울산 광역시 서버가 정상적으로 오픈되었어요.\n서버를 플레이하실 유저분들께서는 아래 버튼을 통해 서버를 접속해보세요.")
            view = discord.ui.View()
            button = LetsGo("서버 접속하기")
            view.add_item(button)
            await channel.send(content="<@&1183361844212150312>", embed=Openembed, view=view)
        if select.values[0] == '2':
            await interaction.response.send_modal(SendNofi())
        
        if select.values[0] == '3':
            await interaction.response.send_modal(NoVerify())

        if select.values[0] == '4':
            await interaction.response.send_modal(DeleteData())

        if select.values[0] == '5':
            await interaction.response.send_modal(Support())
        if select.values[0] == '6':
            await interaction.response.send_modal(AllSaup())
        if select.values[0] == '7':
            await interaction.response.send_modal(OneSaup())
        if select.values[0] == '8':
            await interaction.response.send_message("어떤 분이 기능시험에 합격하셨나요?", ephemeral=True)
            await asyncio.sleep(1)

            try:
                message = await bot.wait_for('message', timeout=10)

                # 명령을 실행한 사용자와 메시지를 보낸 사용자가 일치하는지 확인
                if message.author.id != interaction.user.id:
                    await interaction.followup.send("명령어를 사용한 사용자만 멘션해주세요.", ephemeral=True)
                    return

                mentioned_users = message.mentions
                if mentioned_users:
                    for user in mentioned_users:
                        user_data = db.UlsanVerify.find_one({"DiscordId": str(user.id)})
                        name = user_data.get("PlrName")
                        Openembed= discord.Embed(color=0xC47A31, title=f"<:UlsanRoad:1226025111799205970> 울산광역시 도로교통공단", description=f"###\n{name}님의 기능시험 합격을 축하드립니다!\n지금 바로 면허증을 발급받으실 수 있습니다.\n\nhttps://discord.com/channels/1183359422324543489/1183420558025695323 채널로 이동하신 후,\n**/면허증발급받기** 명령어를 이용하세요!\n\n도로교통공단장")
                        await user.send(embed=Openembed)
                        await message.delete()  # 멘션된 사용자에게 보낸 메시지 삭제
                        channel = bot.get_channel(1225983649078317056)
                        await channel.send(content=f"{name}님이 합격하셨습니다.\n<@{user.id}>")  # 디스코드 채널에 합격 메시지 전송
                        data = db.UlsanCarPr.insert_one(
                            {
                                "PlrName": name,
                                "DiscordId" : str(user.id)
                            }
                        )
                else:
                    await interaction.followup.send("합격한 사용자를 멘션해주세요.", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.response.send_message("시간이 초과되었습니다. 다시 시도해주세요.")

        if select.values[0] == '9':
            channel = bot.get_channel(1264085280475054100)
            Openembed= discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 팩션 인원분들께서는 서버에 입장해주세요", description="> **서버가 임시 오픈되었습니다**\n\n팩션 준비를 위해 서버가 임시로 오픈 되었어요.\n팩션 인원분들께서는 아래 버튼을 통해 게임에 입장해주세요!")
            view = discord.ui.View()
            button = LetsGo("서버 접속하기")
            view.add_item(button)
            await channel.send(content="<@&1183361844212150312>", embed=Openembed, view=view)



class AllSaup(discord.ui.Modal, title="전체 사업자 공문 보내기"):
    Link = discord.ui.TextInput(label="공문 링크를 첨부하세요", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        for member in guild.members:
            unt = discord.utils.get(guild.roles, id=1209471162371801118)
            if member.bot or unt not in member.roles:
                continue

            try:
                embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 울산광역시 공문이 도착했습니다 (전체)", description=f"> To. `울산광역시 개인사업자 및 법인사업자 귀하`\n> **[지금 바로 공문 확인하기]({self.Link.value})**")
                await member.send(embed=embed)
                yes = discord.Embed(color=0xC47A31, title="공지 전송 완료!", description="공지를 성공적으로 보냈어요.")
                await interaction.response.edit_message(embed=yes, view=None)
            except discord.Forbidden:
                user = await bot.fetch_user(str(751835293924982957))
                await user.send(content=f"{member.name}님에게 메시지 보내기에 실패했어요.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


class OneSaup(discord.ui.Modal, title="개별 사업자 공문 보내기"):
    Link = discord.ui.TextInput(label="공문 링크를 첨부하세요", required=True, style=discord.TextStyle.short)
    SaupNumber = discord.ui.TextInput(label="공문을 보낼 사업자 등록번호를 알려주세요", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_data = db.UlsanSaup.find_one({"SaupNumber": str(self.SaupNumber.value)})

        if user_data :
            DiscordId = user_data.get("DiscordId")
            SaupName = user_data.get("SaupName")
            SaupEnglish = user_data.get("EnglishSaupName")
            
            member = guild.get_member(int(DiscordId))
            sendUser = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 울산광역시 공문이 도착했습니다 (개별)", description=f"> To. `{SaupName}({SaupEnglish}) 대표자 귀하`\n> **[지금 바로 공문 확인하기]({self.Link.value})**")
            await member.send(embed=sendUser)
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 전송 완료!", description=f"`{SaupName}({SaupEnglish}) 대표자`님에게 공문을 보냈어요.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class LetsGo(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, url="https://www.roblox.com/games/15927456527/BETA-OPEN-Ulsan")


@bot.tree.context_menu(name="🎫 사업자 등록 수락하기")
async def Con(interaction: discord.Interaction, message: discord.Message):
    getRole = discord.utils.get(interaction.guild.roles, id=1183359440934682634)
    userRole = interaction.user.roles

    if getRole in userRole:
        if interaction.channel_id == 1185932644844843070:
            embed = message.embeds[0]
            USid = embed.fields[1].value
            SaupName = embed.fields[2].value
            SaupNameEnglish = embed.fields[3].value

            user_data = db.UlsanVerify.find_one({"DiscordId": str(USid)})

            random_numbers_Two = ''.join(random.choices('0123456789', k=5))
            random_numbers_One = ''.join(random.choices('1234567', k=2))
            playerName = user_data.get('PlrName')

            data = db.UlsanSaup.insert_one(
                {
                    "DiscordId" : str(USid),
                    "PlrName" : playerName,
                    "SaupNumber" : str(f"135-{random_numbers_One}-{random_numbers_Two}"),
                    "SaupName" : SaupName,
                    "EnglishSaupName" : SaupNameEnglish,
                }
            )
            
            category_id = 1209470847740420166
            category = interaction.guild.get_channel(category_id)
            NewChannel = await interaction.guild.create_text_channel(name=f'│ㆍ🆕│{SaupName}', category=category)

            Newrole = await interaction.guild.create_role(name=f"{SaupName}ㆍ{SaupNameEnglish}", hoist=True)
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록이 완료되었습니다", description=f"<@{USid}>님의 사업자 등록({SaupName})이 성공적으로 승인되었습니다.\n\n> 사업자 등록번호 : `135-{random_numbers_One}-{random_numbers_Two}`\n> 등록된 역할 : {Newrole.mention}\n> 생성된 채널 : {NewChannel.mention}")
            await message.edit(content="",embed=Afterembed, view=None)
            await message.add_reaction("✅")
            role = 1183361841158705265
            roleTWo = 1209471162371801118
            guild = interaction.guild
            member = guild.get_member(int(USid))
            getRole = discord.utils.get(member.guild.roles, id=role)
            getRoleTwo = discord.utils.get(member.guild.roles, id=roleTWo)
            await member.add_roles(getRole)
            await member.add_roles(getRoleTwo)
            await member.add_roles(Newrole)
            await member.edit(nick=f"{SaupName}ㆍ{playerName}")
            sendUser = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록 승인 안내", description=f"> [Web발신]\n\n귀하의 사업자 등록이 승인되었음을 진심으로 축하드립니다.\n신청하신 사업자 등록 요청이 성공적으로 승인되셨습니다. 채널 생성 및 이름 변경은 완료되었으나, 역할 등 지급은 최대 3일 이내로 운영팀에서 처리해드릴 예정입니다.\n\n소중한 시간 내어 신청해주셔서 감사합니다.\n-")
            sendUser.add_field(name="> 사업의 상호명", value=SaupName, inline= True)
            sendUser.add_field(name="> 등록된 사업자 등록번호", value=f"135-{random_numbers_One}-{random_numbers_Two}", inline= True)
            await member.send(embed=sendUser)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"사업자 전용 채널에서 이용해주세요.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 울산광역시장만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)




@bot.tree.context_menu(name="❌ 사업자 등록 거절하기")
async def Con(interaction: discord.Interaction, message: discord.Message):
    getRole = discord.utils.get(interaction.guild.roles, id=1183359440934682634)
    userRole = interaction.user.roles

    if getRole in userRole:
        if interaction.channel_id == 1185932644844843070:

            embed = message.embeds[0]
            field1_value = embed.fields[3].value
            bangsik = embed.fields[6].value
            USid = embed.fields[1].value
            SaupName = embed.fields[2].value


            member = interaction.guild.get_member(int(USid))
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록 거절 안내", description=f"> [Web발신]\n\n귀하의 사업자 등록 요청({SaupName})이 아쉽게도 거절되었음을 알려드립니다.\n\n> 요청이 거절되는 대표적인 이유 :\n- 저작권 침해 우려가 있는 상호명으로 신청하신 경우\n- 운영방식을 구체적으로 기재하지 않은 경우\n- 사업을 운영하는 데에 이득적으로 얻는 부분이 없다고 판단된 경우\n\n소중한 시간 내어 신청해주셔서 감사합니다.")
            embed.add_field(name="> 사업의 상호명", value=SaupName, inline= True)
            embed.add_field(name="> 작성하신 운영방식", value=bangsik, inline= True)
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 거절된 사업자 등록 요청", description=f"<@{USid}>님의 사업자 등록 요청이 거절되었습니다.")
            await message.edit(content="",embed=Afterembed, view=None)
            await message.add_reaction("❌")
            await member.send(embed=embed)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 사업자 전용 채널에서 이용해주세요")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 울산광역시장만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)




@bot.tree.context_menu(name="✅ 인증 수락하기")
async def Con(interaction: discord.Interaction, message: discord.Message):
    getRole = discord.utils.get(interaction.guild.roles, id=1183360336812838963)
    userRole = interaction.user.roles

    if getRole in userRole:
        if interaction.channel_id == 1183411371254235207:
            embed = message.embeds[0]
            field1_value = embed.fields[3].value
            RobloxNickName = embed.fields[0].value
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 수락된 인증요청", description=f"<@{field1_value}>님의 요청이 수락되었습니다")
            await message.edit(content="",embed=Afterembed, view=None)
            await message.add_reaction("✅")
            role = 1183361844212150312
            guild = interaction.guild
            member = guild.get_member(int(field1_value))
            getRole = discord.utils.get(member.guild.roles, id=role)
            rmRole = discord.utils.get(member.guild.roles, id=1183361847034921050)
            await member.add_roles(getRole)
            await member.remove_roles(rmRole)
            await member.edit(nick=f"울산시민ㆍ{RobloxNickName}")
            sendUser = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청이 수락됐어요!", description=f"> 🎊 **인증요청이 수락되었습니다**\n\n축하합니다! {RobloxNickName}님이 요청하셨던 인증이 수락되었어요.\n이제, 울산광역시를 마음껏 즐기실 수 있어요.")
            await member.send(embed=sendUser)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 인증 전용 임베드에서만 이용해주세요")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 울산광역시 운영팀만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.context_menu(name="❌ 인증 거절하기")
async def Con(interaction: discord.Interaction, message: discord.Message):
    getRole = discord.utils.get(interaction.guild.roles, id=1183360336812838963)
    userRole = interaction.user.roles

    if getRole in userRole:
        if interaction.channel_id == 1183411371254235207:

            embed = message.embeds[0]
            field1_value = embed.fields[3].value
            guild = interaction.guild
            member = guild.get_member(int(field1_value))


            member = guild.get_member(int(field1_value))
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청이 거절됐어요", description=f"> 🔴 **인증요청이 거절되었습니다**\n\n> **인증이 거절되는 대표적인 이유**\n* 그룹 미가입\n* 부계정 의심\n* 조직, 정치 그룹 가입")
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 거절된 인증요청", description=f"<@{field1_value}>님의 요청이 거절되었습니다.")
            db.UlsanVerify.delete_one({"DiscordId": str(field1_value)})
            await message.edit(content="",embed=Afterembed, view=None)
            await message.add_reaction("❌")
            await member.send(embed=embed)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 인증 전용 임베드에서만 이용해주세요")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 울산광역시 운영팀만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="나의후원금찾기", description="나의 후원금을 찾을 수 있어요.")
async def password(interaction: discord.Interaction):
    channelId = 1183420558025695323
    user_data = db.UlsanSupport.find_one({"DiscordId": str(interaction.user.id)})
    if interaction.channel_id == channelId:
        if user_data:
            HideMoney = user_data.get("HideMoney")
            if HideMoney != "0":
                converted_amount_str = f"{HideMoney:,}"
                print("True")
                button = getMoney("후원금 나의 딜리계좌로 입금하기")
                view = discord.ui.View()
                view.add_item(button)
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 나의 후원금 찾기", description=f"현재 {interaction.user.mention}님이 받을 수 있는 후원금은 총 **{converted_amount_str}원** 입니다.")
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            else:
                Error = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"현재 {interaction.user.mention}님이 받을 수 있는 후원금이 없어요.")
                await interaction.response.send_message(embed=Error, ephemeral=True)
        else:
            NotSupport = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 후원을 1회 이상 하신 분들만 이용할 수 있는 명령어예요.")
            await interaction.response.send_message(embed=NotSupport, ephemeral=True)
    else:
        NotAllow = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 <#1183420558025695323>에서만 이용할 수 있어요")
        await interaction.response.send_message(embed=NotAllow, ephemeral=True)
        print("false")

@bot.tree.command(name="후원금계산기", description="후원 시 지급되는 돈을 계산해줘요")
async def password(interaction: discord.Interaction, 얼마를후원하시나요:str):
    ratio = 6500000 / 5000

    amount = int(얼마를후원하시나요)

    converted_amount = amount * ratio
    Conv_Money = int(converted_amount)
    HowMuch = f"{int(얼마를후원하시나요):,}"
    converted_amount_str = f"{Conv_Money:,}"

    embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 후원금 계산기", description=f"**{HowMuch}원**을 후원할 경우\n**{converted_amount_str}원**의 인게임 머니를 받습니다.")
    await interaction.response.send_message(embed=embed, ephemeral=True)

class getMoney(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="💵")

    async def callback(self, interaction):
        user_data = db.UlsanSupport.find_one({"DiscordId": str(interaction.user.id)})
        Dilly_Data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        if Dilly_Data:
            HideMoney = user_data.get("HideMoney")
            To_money = Dilly_Data.get("Money")
            Money = int(To_money)+int(HideMoney)

            db.UlsanSupport.update_one(
                {"DiscordId": str(interaction.user.id)},
                {"$set": {"HideMoney": "0"}}
            )

            Dilly_DB.PayNumber.update_one(
                {"discordId": str(interaction.user.id)},
                {"$set": {"Money": Money}}
            )
            Allow = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 입금 완료!", description=f"딜리 **/계좌정보확인하기** 명령어를 통해 계좌 잔액을 확인하실 수 있어요.\n후원해주셔서 감사합니다!")
            await interaction.response.send_message(embed=Allow, ephemeral=True)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"아직 딜리계좌를 개설하지 않으신 것 같아요.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class Support(discord.ui.Modal, title="후원금 정산하기"):
    User_DiscordId = discord.ui.TextInput(label="후원금을 정산할 유저의 디스코드 아이디를 알려주세요", required=True, style=discord.TextStyle.short)
    What_Money = discord.ui.TextInput(label="유저분께서 얼마를 후원하셨나요?", required=True, min_length=1, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(int(self.User_DiscordId.value))
        role_id = 1194590600893321276
        role = member.guild.get_role(role_id)

        user_data = db.UlsanSupport.find_one({"DiscordId": str(self.User_DiscordId.value)})
        Dilly_Data = Dilly_DB.PayNumber.find_one({"discordId": str(self.User_DiscordId.value)})

        if user_data:
            To_money = user_data.get("Money")
            Money = int(To_money)+int(self.What_Money.value)

            ratio = 6500000 / 5000

            amount = int(self.What_Money.value)

            converted_amount = amount * ratio
            Left_Conv_Money = user_data.get("HideMoney")
            Conv_Money = int(Left_Conv_Money)+int(converted_amount)

            converted_amount_str = f"{Conv_Money:,}"

            embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원금 정산완료!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하였습니다.")
            CnSend = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금을 성공적으로 정산하였습니다.\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
            CnSend.add_field(name="> 후원하신 금액", value="비공개", inline= True)

            if Dilly_Data:
                Dilly_Money = Dilly_Data.get("Money")
                JonghapMoney = int(Dilly_Money)+int(converted_amount)

                Dilly_DB.PayNumber.update_one(
                    {"discordId": str(self.User_DiscordId.value)},
                    {"$set": {"Money": JonghapMoney}}
                )

                USERSEND = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하여\n{converted_amount_str}원을 **나의 딜리계좌**로 입금해드렸습니다.\n딜리 **/계좌정보확인하기** 명령어를 통해 잔액을 확인하세요.\n\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
            else:
                USERSEND = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하였지만\n아직 딜리계좌가 없어 {converted_amount_str}원을 입금해드릴 수 없는 상태이므로 딜리계좌 개설 후 **/나의후원금찾기** 명령어를 통해 나의 후원금을 찾을 수 있습니다.\n\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
                db.UlsanSupport.update_one(
                    {"DiscordId": str(self.User_DiscordId.value)},
                    {"$set": {"HideMoney": Conv_Money}}
                )

            USERSEND.add_field(name="> 후원하신 금액", value=self.What_Money.value, inline= True)
            USERSEND.add_field(name="> 누적 후원금액", value=Money, inline= True)

            db.UlsanSupport.update_one(
                    {"DiscordId": str(self.User_DiscordId.value)},
                    {"$set": {"Money": Money}}
            )
            
                    
            if Money >= 200000:
                USERSEND.add_field(name="> 등급", value="프리미엄", inline=False)
                CnSend.add_field(name="> 등급", value="프리미엄", inline=True)
                await member.add_roles(member.guild.get_role(1194592850143359038))
            elif Money >= 100000:
                USERSEND.add_field(name="> 등급", value="다이아몬드", inline=False)
                CnSend.add_field(name="> 등급", value="다이아몬드", inline=True)
                await member.add_roles(member.guild.get_role(1194887238039896064))
            # ... (중략)
            elif Money >= 50000:
                USERSEND.add_field(name="> 등급", value="골드", inline=False)
                CnSend.add_field(name="> 등급", value="골드", inline=True)
                await member.add_roles(member.guild.get_role(1194592777472843888))
            elif Money >= 25000:
                USERSEND.add_field(name="> 등급", value="실버", inline=False)
                CnSend.add_field(name="> 등급", value="실버", inline=True)
                await member.add_roles(member.guild.get_role(1194592711374802965))
            elif Money >= 10000:
                USERSEND.add_field(name="> 등급", value="브론즈", inline=False)
                CnSend.add_field(name="> 등급", value="브론즈", inline=True)
                await member.add_roles(member.guild.get_role(1194592594445996122))
            elif Money >= 5000:
                USERSEND.add_field(name="> 등급", value="아이언", inline=False)
                CnSend.add_field(name="> 등급", value="아이언", inline=True)
                await member.add_roles(member.guild.get_role(1194590600893321276))
            else:
                USERSEND.add_field(name="> 등급", value="없음", inline=False)
                CnSend.add_field(name="> 등급", value="없음", inline=True)
                await member.add_roles(role)
                

            await member.send(embed=USERSEND)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            channel = bot.get_channel(1194284070197276782)
            await channel.send(embed=CnSend)

            Log_Send = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원 로그", description=f"<@{self.User_DiscordId}>님이 ({self.What_Money.value}원)을 후원하여 {converted_amount_str}원을 받았습니다.")
            channel = bot.get_channel(1185932712536719451)
            await channel.send(embed=Log_Send)
        else:
            disId = self.User_DiscordId.value
            data = db.UlsanSupport.insert_one(
                {
                    "Money": str(self.What_Money.value),
                    "DiscordId" : str(disId),
                    "HideMoney": str("0")
                }
            )
            Money = int(self.What_Money.value)

            ratio = 6500000 / 5000

            amount = int(self.What_Money.value)

            converted_amount = amount * ratio
            Conv_Money = int(converted_amount)

            converted_amount_str = f"{Conv_Money:,}"

            embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원금 정산완료!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하였습니다.")
            CnSend = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금을 성공적으로 정산하였습니다.\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
            CnSend.add_field(name="> 후원하신 금액", value="비공개", inline= True)

            if Dilly_Data:
                Dilly_Money = Dilly_Data.get("Money")
                JonghapMoney = int(Dilly_Money)+int(converted_amount)

                Dilly_DB.PayNumber.update_one(
                    {"discordId": str(self.User_DiscordId.value)},
                    {"$set": {"Money": JonghapMoney}}
                )

                USERSEND = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하여\n{converted_amount_str}원을 **나의 딜리계좌**로 입금해드렸습니다.\n딜리 **/계좌정보확인하기** 명령어를 통해 잔액을 확인하세요.\n\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
            else:
                USERSEND = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원해주셔서 감사합니다!", description=f"<@{self.User_DiscordId}>님의 후원금({self.What_Money.value}원)을 성공적으로 정산하였지만\n아직 딜리계좌가 없어 {converted_amount_str}원을 입금해드릴 수 없는 상태이므로 딜리계좌 개설 후 **/나의후원금찾기** 명령어를 통해 나의 후원금을 찾을 수 있습니다.\n\n후원해주신 소중한 자금은 울산광역시의 발전을 위해 소중히 사용하겠습니다.")
                db.UlsanSupport.update_one(
                    {"DiscordId": str(self.User_DiscordId.value)},
                    {"$set": {"HideMoney": Conv_Money}}
                )

            USERSEND.add_field(name="> 후원하신 금액", value=self.What_Money.value, inline= True)
            USERSEND.add_field(name="> 누적 후원금액", value=Money, inline= True)

            db.UlsanSupport.update_one(
                    {"DiscordId": str(self.User_DiscordId.value)},
                    {"$set": {"Money": Money}}
            )
            
                    
            if Money >= 200000:
                USERSEND.add_field(name="> 등급", value="프리미엄", inline=False)
                CnSend.add_field(name="> 등급", value="프리미엄", inline=True)
                await member.add_roles(member.guild.get_role(1194592850143359038))
            elif Money >= 100000:
                USERSEND.add_field(name="> 등급", value="다이아몬드", inline=False)
                CnSend.add_field(name="> 등급", value="다이아몬드", inline=True)
                await member.add_roles(member.guild.get_role(1194887238039896064))

            elif Money >= 50000:
                USERSEND.add_field(name="> 등급", value="골드", inline=False)
                CnSend.add_field(name="> 등급", value="골드", inline=True)
                await member.add_roles(member.guild.get_role(1194592777472843888))
            elif Money >= 25000:
                USERSEND.add_field(name="> 등급", value="실버", inline=False)
                CnSend.add_field(name="> 등급", value="실버", inline=True)
                await member.add_roles(member.guild.get_role(1194592711374802965))
            elif Money >= 10000:
                USERSEND.add_field(name="> 등급", value="브론즈", inline=False)
                CnSend.add_field(name="> 등급", value="브론즈", inline=True)
                await member.add_roles(member.guild.get_role(1194592594445996122))
            elif Money >= 5000:
                USERSEND.add_field(name="> 등급", value="아이언", inline=False)
                CnSend.add_field(name="> 등급", value="아이언", inline=True)
                await member.add_roles(member.guild.get_role(1194590600893321276))
            else:
                USERSEND.add_field(name="> 등급", value="없음", inline=False)
                CnSend.add_field(name="> 등급", value="없음", inline=True)
                await member.add_roles(role)
                

            await member.send(embed=USERSEND)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            channel = bot.get_channel(1194284070197276782)
            await channel.send(embed=CnSend)

            Log_Send = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 후원 로그", description=f"<@{self.User_DiscordId}>님이 ({self.What_Money.value}원)을 후원하여 {converted_amount_str}원을 받았습니다.")
            channel = bot.get_channel(1185932712536719451)
            await channel.send(embed=Log_Send)

class SendNofi(discord.ui.Modal, title="공지 작성하기"):
    Title = discord.ui.TextInput(label="공지 제목을 입력하세요", required=True, style=discord.TextStyle.short)
    SubTitle = discord.ui.TextInput(label="공지 본문을 입력하세요", required=True, min_length=1, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        for member in guild.members:
            unt = discord.utils.get(guild.roles, id=1183361844212150312)
            if member.bot or unt not in member.roles:
                continue

            try:
                embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> {self.Title.value}", description=f"{self.SubTitle.value}")
                await member.send(embed=embed)
                yes = discord.Embed(color=0xC47A31, title="공지 전송 완료!", description="공지를 성공적으로 보냈어요.")
                await interaction.response.edit_message(embed=yes, view=None)
            except discord.Forbidden:
                user = await bot.fetch_user(str(751835293924982957))
                await user.send(content=f"{member.name}님에게 메시지 보내기에 실패했어요.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

class NoVerify(discord.ui.Modal, title="미전입자) 공지 작성하기"):
    Title = discord.ui.TextInput(label="공지 제목을 입력하세요", required=True, style=discord.TextStyle.short)
    SubTitle = discord.ui.TextInput(label="공지 본문을 입력하세요", required=True, min_length=1, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        for member in guild.members:
            unt = discord.utils.get(guild.roles, id=1183361847034921050)
            if member.bot or unt not in member.roles:
                continue

            try:
                embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> {self.Title.value}", description=f"{self.SubTitle.value}")
                await member.send(embed=embed)
                yes = discord.Embed(color=0xC47A31, title="공지 전송 완료!", description="공지를 성공적으로 보냈어요.")
                await interaction.response.edit_message(embed=yes, view=None)
            except discord.Forbidden:
                user = await bot.fetch_user(str(751835293924982957))
                await user.send(content=f"{member.name}님에게 메시지 보내기에 실패했어요.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

class Saup(discord.ui.Modal, title="사업 신청하기"):
    Title = discord.ui.TextInput(label="상호명을 알려주세요",placeholder="예)스타벅스", required=True, style=discord.TextStyle.short)
    EnglishTitle = discord.ui.TextInput(label="운영하실 사업의 상호명을 알려주세요 (영어)",placeholder="예)StarBucks", required=True, style=discord.TextStyle.short)
    upjong = discord.ui.TextInput(label="운영하시려는 사업의 업종을 알려주세요",placeholder="예)요식업", required=True, style=discord.TextStyle.short)
    areyouneedScript = discord.ui.TextInput(label="건물과 스크립트가 준비되어 있으신가요?",placeholder="예/아니요", required=True, min_length=1, style=discord.TextStyle.short)
    unyongbangsik = discord.ui.TextInput(label="사업을 운영하시려는 방식을 구체적으로 알려주세요", required=True,min_length=100, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        user = await bot.fetch_user(interaction.user.id)
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록 신청 완료 안내", description="> [Web발신]\n\n귀하의 사업자 등록 신청이 완료되었습니다.\n\n- 사업자 등록 신청은 최대 1주일 내로 결과가 통보 됩니다.\n- 검토 기간 중 변경 또는 취소를 원하시는 경우, <@751835293924982957>의 다이렉트 메세지로 연락해야 합니다. 다만, 신청 결과 통보 이후에는 변경 또는 취소가 불가하며, 취소 요청이 승인되시더라도 수수료가 부과될 수 있음을 알려드립니다.\n- 검토결과가 최종 승인되면, 3일 이내로 디스코드 채널 등이 지급됩니다.\n-")
        embed.add_field(name="> 사업의 상호명", value=f"{self.Title}({self.EnglishTitle})", inline=True)
        embed.add_field(name="> 사업의 업종", value=self.upjong.value, inline= True)
        await user.send(embed=embed)
        Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 등록 신청 완료!", description=f"자세한 사항은 보내드린 다이렉트 메세지를 확인해주세요")
        await interaction.response.send_message(embed=Afterembed, ephemeral=True)
        PleaseEmbed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록 신청이 접수 되었어요")
        PleaseEmbed.add_field(name="> 멘션", value=f"<@{interaction.user.id}>", inline= False)
        PleaseEmbed.add_field(name="> 아이디", value=interaction.user.id, inline= False)
        PleaseEmbed.add_field(name="> 상호명", value=self.Title.value, inline= False)
        PleaseEmbed.add_field(name="> 상호명(영어)", value=self.EnglishTitle.value, inline= False)
        PleaseEmbed.add_field(name="> 업종", value=self.upjong.value, inline= False)
        PleaseEmbed.add_field(name="> 건물 및 스크립트 준비여부", value=self.areyouneedScript.value, inline= False)
        PleaseEmbed.add_field(name="> 운영방식", value=self.unyongbangsik.value, inline= False)

        channel = bot.get_channel(1185932644844843070)
        await channel.send(embed=PleaseEmbed)



class StartVerify(discord.ui.Modal, title="울산 광역시 인증 시작하기"):
    RBLXName = discord.ui.TextInput(label="로블록스 닉네임을 알려주세요", placeholder="디스플레이 닉네임으로 입력하지 마세요", required=True, style=discord.TextStyle.short)
    RBLXURL = discord.ui.TextInput(label="로블록스 프로필 링크를 첨부하세요", placeholder="https://www.roblox.com/users/687871238/profile", required=True, style=discord.TextStyle.short)
    Real = discord.ui.TextInput(label="울산광역시 그룹 요청을 완료하셨나요?", placeholder="예/아니요", required=True, min_length=1, max_length=3, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        try:
            user = await bot.fetch_user(interaction.user.id)
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청을 전송했어요", description=f"> 📃 **인증요청이 접수되었습니다**\n\n{self.RBLXName.value}님의 인증요청을 운영팀이 신속하게 처리할 예정이며,\n최대 3일 정도 소요될 수 있다는 점, 참고해주세요.\n추가로 문의하실 사항이 있으시면, 언제든지 문의해주세요!\n울산 광역시를 찾아주셔서 감사합니다.")
            await user.send(embed=embed)
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 접수 완료!", description=f"자세한 사항은 보내드린 다이렉트 메세지를 확인해주세요")
            await interaction.response.send_message(embed=Afterembed, ephemeral=True)
            PleaseEmbed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청이 접수 되었어요")
            PleaseEmbed.add_field(name="> 닉네임", value=self.RBLXName.value, inline= False)
            PleaseEmbed.add_field(name="> 프로필 링크", value=self.RBLXURL.value, inline= False)
            PleaseEmbed.add_field(name="> 그룹요청 여부", value=self.Real.value, inline= False)
            PleaseEmbed.add_field(name="> 유저 아이디", value=interaction.user.id, inline= False)
            channel = bot.get_channel(1183411371254235207)
            await channel.send(content="<@&1183360336812838963>",embed=PleaseEmbed)
            data = db.UlsanVerify.insert_one(
                {
                    "PlrName": self.RBLXName.value,
                    "DiscordId" : str(interaction.user.id),
                }
            )
        except discord.Forbidden:
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"**`서버 멤버가 보내는 다이렉트 메시지 허용하기`**를 끄신 것 같아요.\n활성화 하신 후, 재시도 해주세요.")
            await interaction.response.send_message(embed=Afterembed, ephemeral=True)

class DeleteData(discord.ui.Modal, title="유저 데이터 삭제"):
    DCID = discord.ui.TextInput(label="삭제할 유저의 디코 아이디를 입력하세요", placeholder="0", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        data = db.UlsanVerify.delete_one(
            {
                "DiscordId" : str(self.DCID.value)
            }
        )


class PleaseVerify(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="📑")

    async def callback(self, interaction):
        user_data = db.UlsanVerify.find_one({"DiscordId": str(interaction.user.id)})

        if not user_data:
            await interaction.response.send_modal(StartVerify())
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"이미 인증을 요청 중이시거나, 인증을 완료하신 것 같아요")
            await interaction.response.send_message(embed=embed, ephemeral=True)



@bot.tree.command(name="인증메세지", description="유저의 인증을 위해 인증 메세지를 보냅니다")
async def password(interaction: discord.Interaction):
    channelId = 1183411349758410853
    if interaction.channel_id == channelId:
        print("True")
        button = PleaseVerify("인증 시작하기")
        view = discord.ui.View()
        view.add_item(button)
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 울산광역시 인증 시작하기", description=f"인증을 시작하고 싶다면, 아래 버튼을 눌러주세요")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        NotAllow = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 <#1183411349758410853> 채널에서만 사용할 수 있어요")
        await interaction.response.send_message(embed=NotAllow, ephemeral=True)
        print("false")


class SudongVerify(discord.ui.Modal, title="인증하기"):
    RBLXName = discord.ui.TextInput(label="인증하실 유저의 로블록스 닉네임을 알려주세요", placeholder="디스플레이 닉네임으로 입력하지 마세요", required=True, style=discord.TextStyle.short)
    DiscordId = discord.ui.TextInput(label="인증하실 유저의 디스코드 아이디를 알려주세요", placeholder="751835293924982957", required=True, style=discord.TextStyle.short)
    How = discord.ui.TextInput(label="인증을 허가할까요? (1=허가, 2=불허가)", placeholder="1", required=True, style=discord.TextStyle.short)
    IfNotThen = discord.ui.TextInput(label="인증이 불허라면 그 사유를 알려주세요", placeholder="그룹 미가입", required=False, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        try:
            if self.How.value == "1":
                role = 1183361844212150312
                guild = interaction.guild
                member = guild.get_member(int(self.DiscordId.value))
                getRole = discord.utils.get(member.guild.roles, id=role)
                rmRole = discord.utils.get(member.guild.roles, id=1183361847034921050)
                await member.add_roles(getRole)
                await member.remove_roles(rmRole)
                await member.edit(nick=f"울산시민ㆍ{self.RBLXName}")
                Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 수락된 인증요청", description=f"<@{self.DiscordId}>님의 요청이 수락되었습니다")
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청이 수락됐어요!", description=f"> 🎊 **인증요청이 수락되었습니다**\n\n축하합니다! {self.RBLXName.value}님이 요청하셨던 인증이 수락되었어요.\n이제, 울산광역시를 마음껏 즐기실 수 있어요.")
                await member.send(embed=embed)
                await interaction.response.send_message(embed=Afterembed, view=None)
                message = interaction.channel.fetch_message(int(self.MessageId))
                await interaction.channel.purge(message)
            elif self.How.value == "2":
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 인증요청이 거절됐어요", description=f"> 🔴 **인증요청이 거절되었습니다**\n\n거절된 사유 : {self.IfNotThen.value}")
                guild = interaction.guild
                member = guild.get_member(int(self.DiscordId.value))
                db.UlsanVerify.delete_one({"DiscordId": str(self.DiscordId.value)})
                if member:
                    await member.send(embed=embed)
                    Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 거절된 인증요청", description=f"<@{self.DiscordId}>님의 요청이 거절되었습니다.\n거절 사유 : {self.IfNotThen.value}")
                    await interaction.response.edit_message(embed=Afterembed, view=None)

        except:
            print("실패")

class SaupHeoGa(discord.ui.Modal, title="사업 관리하기"):
    RBLXName = discord.ui.TextInput(label="사업을 신청한 유저의 로블록스 닉네임을 알려주세요", placeholder="디스플레이 닉네임으로 입력하지 마세요", required=True, style=discord.TextStyle.short)
    DiscordId = discord.ui.TextInput(label="사업을 신청한 유저의 디스코드 아이디를 알려주세요", placeholder="751835293924982957", required=True, style=discord.TextStyle.short)
    SaupName = discord.ui.TextInput(label="사업을 신청한 사업명을 알려주세요", placeholder="감성채널", required=True, style=discord.TextStyle.short)
    How = discord.ui.TextInput(label="사업자 등록을 허가할까요? (1=허가, 2=불허가)", placeholder="1", required=True, style=discord.TextStyle.short)
    IfNotThen = discord.ui.TextInput(label="사업자 등록이 불허라면 그 사유를 알려주세요", placeholder="공무업 불가", required=False, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(int(self.DiscordId.value))
        if self.How.value == "1":
            Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 수락된 사업자 등록", description=f"<@{self.DiscordId}>님의 {self.SaupName.value} 사업자 등록이 수락되었습니다")
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록이 최종적으로 수락됐어요!", description=f"> 🎊 **사업자 등록 수락**\n\n축하합니다! {self.RBLXName.value}님이 신청하셨던 {self.SaupName.value}(이)가 최종적으로 승인되었습니다.\n역할과 채널이 생기기에는 최대 3일 정도 소요되오니, 이 점 양해바랍니다.")
            await member.send(embed=embed)
            await interaction.response.send_message(embed=Afterembed, view=None)
        elif self.How.value == "2":
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 사업자 등록이 거절되었어요", description=f"> 🔴 **사업자 등록이 거절되었습니다**\n\n거절된 사유 : {self.IfNotThen.value}")

            if member:
                await member.send(embed=embed)
                Afterembed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 거절된 사업자 등록", description=f"<@{self.DiscordId.value}>님의 사업자 등록이 거절되었습니다.\n거절 사유 : {self.IfNotThen.value}")
                await interaction.response.send_message(embed=Afterembed, view=None)

@bot.tree.command(name="문의하기", description="사업신청,후원,신고 등을 할수 있는 명령어입니다")
async def password(interaction: discord.Interaction):
    if interaction.channel_id == 1183420558025695323:
        viewww = SelectReport()
        await interaction.response.send_message("어떤 문의를 하시나요?", view=viewww, ephemeral=True)
    else:
        NotAllow = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 <#1183420558025695323>에서만 이용할 수 있어요")
        await interaction.response.send_message(embed=NotAllow, ephemeral=True)


class SelectReport(View):
    @discord.ui.select(
        placeholder="문의 선택",
        options=[
            discord.SelectOption(
                label="사업 신청",
                value='1',
                description="사업 신청과 관련된 문의를 처리합니다",
                emoji="🛴"
            ),
            discord.SelectOption(
                label="일반 문의",
                value='2',
                description="종합적인 문의를 처리합니다",
                emoji="🎈"
            )
        ]
    )

    async def select_callback(self, interaction, select):
        select.disabled = True
        
        if select.values[0] == '1':
            await interaction.response.send_modal(Saup())
        if select.values[0] == '2':
            embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 문의채널을 생성할까요?", description="문의채널을 생성하면, 삭제하실 수 없어요.\n문의를 시작하시려면, 문의 시작하기 버튼을 눌러주세요.")
            button = MadeChannel("문의 시작하기")
            view = discord.ui.View(timeout=None)
            view.add_item(button)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class MadeChannel(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="📩")

    async def callback(self, interaction):
        user_data = db.UlsanVerify.find_one({"DiscordId": str(interaction.user.id)})
        rbNickName = user_data.get("PlrName")
        category_id = 1213021041069133824
        category = interaction.guild.get_channel(category_id)
        NwChannel = await interaction.guild.create_text_channel(name=f"│ㆍ{rbNickName}", category=category, overwrites={
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, attach_files=True, embed_links=True),
        interaction.guild.get_role(1183360336812838963): discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)})
        embed = discord.Embed(color=0xC47A31, title=f"<:ulsan:1183391095900602378> 문의채널을 생성했어요.", description=f"{rbNickName}님의 문의채널을 생성하였습니다.\n무엇을 도와드릴까요?")
        button = CanCelChannel("문의 종료하기", NwChannel)
        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=None, content=f"채널 생성이 완료되었습니다.\n생성된 채널로 바로가기 > {NwChannel.mention}", ephemeral=True)
        await NwChannel.send(content=f"{interaction.user.mention} <@&1183360336812838963>", embed=embed, view=view)

        
class CanCelChannel(discord.ui.Button):
    def __init__(self, label, channel):
        super().__init__(label=label, style=discord.ButtonStyle.red)
        self.Nwchannel = channel
    
    async def callback(self, interaction):
        getRole = discord.utils.get(interaction.guild.roles, id=1183360336812838963)
        userRole = interaction.user.roles

        if getRole in userRole:

            message = await interaction.channel.send("채널이 곧 삭제됩니다.")
            for i in range(3, 0, -1):
                await asyncio.sleep(1)
                await message.edit(content=f"{i}초 뒤에 삭제됩니다.")
            await asyncio.sleep(1)
            await self.Nwchannel.delete()


class BuyCar(View):
    @discord.ui.select(
        placeholder="차량 선택",
        options=[
            discord.SelectOption(
                label="Hyundai Ioniq5",
                value='1',
                description="차량 가격 : 17,000,000원",
                emoji="🚘"
            ),
            discord.SelectOption(
                label="Genesis G70",
                value='2',
                description="차량 가격 : 21,000,000원",
                emoji="🚘"
            )
        ]
    )

    async def select_callback(self, interaction, select):
        select.disabled = True
        
        if select.values[0] == '1':
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> Hyundai Ioniq5", description=f"###\n`차량 가격 : 17,000,000원`\n구매를 진행하시려면 `다음`버튼을 눌러주세요")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1205101456311459931/1225084352048926810/946402cee8c70b37.png?ex=661fd7b6&is=660d62b6&hm=b4f939d38bd4f7b835118f60e76823986522af0a8baf6670e4c1a20d642512f6&=&format=webp&quality=lossless&width=676&height=676")
            button = Buy_HyundaiIoniq5("다음")
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.edit_message(embed=embed, view=view)
        if select.values[0] == '2':
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> Genesis G70", description=f"###\n`차량 가격 : 21,000,000원`\n구매를 진행하시려면 `다음`버튼을 눌러주세요")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1179793861028102215/1225088339611353218/G70.png?ex=661fdb6d&is=660d666d&hm=c91911b4dc06163d0a720a97ab8e168ef9837f4df1d81453ede2ea7a1804e151&=&format=webp&quality=lossless&width=676&height=676")
            button = Buy_GenesisG70("다음")
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.edit_message(embed=embed, view=view)




class SelectCar(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="🚘")

    async def callback(self, interaction):
        viewww = BuyCar()
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 울산광역시 딜러쉽", description=f"구매하실 차량을 선택해주세요.")
        await interaction.response.edit_message(embed=embed, view=viewww)

class SeeMyCar(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="📂")

    async def callback(self, interaction):
        user_data = db.UlsanCar.find_one({"DiscordId": str(interaction.user.id)})
        
        if user_data:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 내 차량 조회하기", description=f"{interaction.user.mention}님이 소지하고 계산 차량 목록입니다.")
            car_names = [car_name for car_name in user_data.keys() if car_name not in ["_id", "DiscordId"]]
            view = self.create_car_navigation_view(car_names)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"차량을 찾을 수 없어요.")
            await interaction.response.edit_message(embed=embed, view=None)
    
    def create_car_navigation_view(self, car_names):
        view = discord.ui.View()
        for car_name in car_names:
            button = CarInfoButton(car_name)
            view.add_item(button)
        return view


class CarInfoButton(discord.ui.Button):
    def __init__(self, car_name):
        super().__init__(label=car_name, style=discord.ButtonStyle.blurple, emoji="🚗")
        self.car_name = car_name

    async def callback(self, interaction):

        user_data = db.UlsanCar.find_one({"DiscordId": str(interaction.user.id)})

        if user_data:
            if self.car_name == "HyundaiIoniq5":
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> Hyundai Ioniq5", description=f"* `차량 가격 : 17,000,000원`\n* `차량 ins 번호 : {user_data.get('HyundaiIoniq5')}`")
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1205101456311459931/1225084352048926810/946402cee8c70b37.png?ex=661fd7b6&is=660d62b6&hm=b4f939d38bd4f7b835118f60e76823986522af0a8baf6670e4c1a20d642512f6&=&format=webp&quality=lossless&width=676&height=676")
                await interaction.response.edit_message(embed=embed)
            elif self.car_name == "GenesisG70":
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> Genesis G70", description=f"* `차량 가격 : 21,000,000원`\n* `차량 ins 번호 : {user_data.get('GenesisG70')}`")
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1179793861028102215/1225088339611353218/G70.png?ex=661fdb6d&is=660d666d&hm=c91911b4dc06163d0a720a97ab8e168ef9837f4df1d81453ede2ea7a1804e151&=&format=webp&quality=lossless&width=676&height=676")
                await interaction.response.edit_message(embed=embed)



class Buy_HyundaiIoniq5(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="🚘")

    async def callback(self, interaction):
        user_data = db.UlsanCar.find_one({"DiscordId": str(interaction.user.id)})
        dillyData = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})

        if user_data:
            if dillyData:
                if not user_data.get("HyundaiIoniq5"):
                    button = Buying("동의하기", "HyundaiIoniq5", "17000000")
                    view = discord.ui.View()
                    view.add_item(button)
                    embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 울산 딜러쉽 이용약관에 동의해주세요", description=f"차량을 이용하기 위해선 아래 약관에 동의해야해요.\n##\n울산 차량 구매 약관\n###\n차량 인수 및 환불\n* 차량 인수 시, 구매자는 차량의 상태 및 보증 내용을 확인해야 합니다.\n* 차량 인수 후에는 환불이 제공되지 않습니다.\n###\n운전의 의무\n* 차량 운전 시, 울산광역시 도로교통법에 준수하여 운전한다는 것으로 간주됩니다.\n###\n소유권 이전\n* 차량의 소유권은 구매자가 전액 지불한 후에 판매자로부터 이전됩니다.\n###\n유효성\n* 해당 약관에 동의하게 되면 구매자가 해당 약관의 모두 동의한 것으로 간주됩니다.")
                    await interaction.response.edit_message(embed=embed, view=view)
                else:
                    embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"이미 해당 차량을 소지하고 있어요.")
                    await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"울산 딜러십은 딜리계좌를 소지하고 계신 분만 이용할 수 있어요.")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"울산 딜러십은 면허 소지자만 이용할 수 있어요.")
            await interaction.response.edit_message(embed=embed, view=None)



class Buy_GenesisG70(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="🚘")

    async def callback(self, interaction):
        user_data = db.UlsanCar.find_one({"DiscordId": str(interaction.user.id)})
        dillyData = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})

        if user_data:
            if dillyData:
                if not user_data.get("GenesisG70"):
                    button = Buying("동의하기", "GenesisG70", "21000000")
                    view = discord.ui.View()
                    view.add_item(button)
                    embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 울산 딜러쉽 이용약관에 동의해주세요", description=f"차량을 이용하기 위해선 아래 약관에 동의해야해요.\n##\n울산 차량 구매 약관\n###\n차량 인수 및 환불\n* 차량 인수 시, 구매자는 차량의 상태 및 보증 내용을 확인해야 합니다.\n* 차량 인수 후에는 환불이 제공되지 않습니다.\n###\n운전의 의무\n* 차량 운전 시, 울산광역시 도로교통법에 준수하여 운전한다는 것으로 간주됩니다.\n###\n소유권 이전\n* 차량의 소유권은 구매자가 전액 지불한 후에 판매자로부터 이전됩니다.\n###\n유효성\n* 해당 약관에 동의하게 되면 구매자가 해당 약관의 모두 동의한 것으로 간주됩니다.")
                    await interaction.response.edit_message(embed=embed, view=view)
                else:
                    embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"이미 해당 차량을 소지하고 있어요.")
                    await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"울산 딜러십은 딜리계좌를 소지하고 계신 분만 이용할 수 있어요.")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"울산 딜러십은 면허 소지자만 이용할 수 있어요.")
            await interaction.response.edit_message(embed=embed, view=None)



class Buying(discord.ui.Button):
    def __init__(self, label, Carname, CarPrice):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="📃")
        self.Cname = Carname
        self.Cprs = CarPrice

    async def callback(self, interaction):
        embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 쉽고 간편한 결제, Dilly Pay", description=f"결제를 진행하기 위해 다이렉트 메세지로 결제 확인 메세지를 보내드렸어요.\n다이렉트 메세지를 확인해주세요!")
        Dm = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 결제를 진행할까요?", description=f"###\n{self.Cname}({self.Cprs}원) 을(를) 구매할까요?\n구매를 원하시면 아래 버튼을 눌러주세요.")
        button = Buyed("일시불로 결제하기", self.Cname, self.Cprs)
        view = discord.ui.View()
        view.add_item(button)
        user = await bot.fetch_user(interaction.user.id)
        await user.send(embed=Dm, view=view)
        await interaction.response.edit_message(embed=embed, view=None)



class Buyed(discord.ui.Button):
    def __init__(self, label, Carname, CarPrice):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="<:dilly:1209793389176819722>")
        self.Cname = Carname
        self.CarPs = CarPrice

    async def callback(self, interaction):
        dillyData = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        user_data = db.UlsanCar.find_one({"DiscordId": str(interaction.user.id)})

        SetName = dillyData.get("SetName")
        To_money = dillyData.get("Money")
        money = self.CarPs

        Sd_Money_Money = int(To_money)-int(money)

        if int(To_money) >= int(money):
            embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 결제가 완료되었어요", description=f"결제가 성공적으로 완료되었어요.\n###\n결제내역 📃\n* 차량 명(모델명) : {self.Cname}\n* 차량 가격 : {self.CarPs}원(일시불 결제)")
            Diller = discord.Embed(color=0x5F1F91, title="<:ulsan_Road:1225061996613992479> 울산광역시 도로교통공단", description=f"###\n차량 등록 안내\n{SetName}님의 차량 구매가 완료되어 차량 등록 안내 드립니다.\n차량 등록은 차량 결제일로부터 최대 7일 정도 소요될 수 있습니다.\n추후 차량 등록이 허가되면, 다이렉트 메세지를 통해 안내 해 드리겠습니다.\n\n도로교통공단")
            
            Dilly_DB.PayNumber.update_one(
                {"discordId": str(interaction.user.id)},
                {"$set": {"Money": Sd_Money_Money}}
            )

            db.UlsanCar.update_one(
                {"DiscordId": str(interaction.user.id)},
                {"$set": {self.Cname: "차량 등록 대기중"}}
            )

            
            user = await bot.fetch_user(interaction.user.id)
            await user.send(embed=Diller, view=None)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=0x1a3bc6, title="오류가 발생했어요", description="계좌의 잔액이 부족해요.")
            await interaction.response.edit_message(embed=embed, view=None)

@bot.tree.command(name="공무원전용", description="해당 슬래시는 울산광역시 공무원분들만 이용할 수 있어요")
async def Ulsan(interaction: discord.Interaction):
    if str(interaction.user.id) == str(751835293924982957):
        viewww = SelectUlsan()
        await interaction.response.send_message("선택사항을 선택하세요", view=viewww, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"{interaction.user.mention}님은 해당 명령어를 이용할 수 있는 권한이 없어요")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SelectUlsan(View):
    @discord.ui.select(
        placeholder="선택사항 선택",
        options=[
            discord.SelectOption(
                label="장내기능시험 합격",
                value='1',
                description="면허증 발급을 허가합니다",
                emoji="💳"
            ),
                discord.SelectOption(
                label="면허 정지하기",
                value='2',
                description="면허를 정지시킵니다",
                emoji="✂"
            ),
                discord.SelectOption(
                label="기능시험 등록하기",
                value='3',
                description="기능시험을 응시할 유저를 등록합니다",
                emoji="📑"
            )
        ]
    )

    async def select_callback(self, interaction, select):
        select.disabled = True
        
        if select.values[0] == '1':
            await interaction.response.send_message("어떤 분이 기능시험에 합격하셨나요?", ephemeral=True)
            await asyncio.sleep(1)

            try:
                message = await bot.wait_for('message', timeout=10)

                # 명령을 실행한 사용자와 메시지를 보낸 사용자가 일치하는지 확인
                if message.author.id != interaction.user.id:
                    await interaction.followup.send("명령어를 사용한 사용자만 멘션해주세요.", ephemeral=True)
                    return

                mentioned_users = message.mentions
                if mentioned_users:
                    for user in mentioned_users:
                        user_data = db.UlsanVerify.find_one({"DiscordId": str(user.id)})
                        name = user_data.get("PlrName")
                        Openembed= discord.Embed(color=0xC47A31, title=f"<:UlsanRoad:1226025111799205970> 울산광역시 도로교통공단", description=f"###\n {name}님의 기능시험 합격을 축하드립니다!\n지금 바로 면허증을 발급받으실 수 있습니다.\n\nhttps://discord.com/channels/1183359422324543489/1183420558025695323 채널로 이동하신 후,\n**/면허증발급받기** 명령어를 이용하세요!\n\n도로교통공단장")
                        await user.send(embed=Openembed)
                        await message.delete()  # 멘션된 사용자에게 보낸 메시지 삭제
                        channel = bot.get_channel(1225983649078317056)
                        await channel.send(content=f"{name}님이 합격하셨습니다.\n<@{user.id}>")  # 디스코드 채널에 합격 메시지 전송
                        data = db.UlsanCarPr.insert_one(
                            {
                                "PlrName": name,
                                "DiscordId" : str(user.id)
                            }
                        )
                else:
                    await interaction.followup.send("합격한 사용자를 멘션해주세요.", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.response.send_message("시간이 초과되었습니다. 다시 시도해주세요.")




                

        if select.values[0] == '2':
            await interaction.response.send_message("어떤 분의 면허를 정지할까요?")
            await asyncio.sleep(1)
            try:
                message = await bot.wait_for('message', timeout=10)
                mentioned_users = message.mentions
                if mentioned_users:
                    for user in mentioned_users:
                        user_data = db.UlsanVerify.find_one({"DiscordId": str(user.id)})
                        name = user_data.get("PlrName")
                        Openembed= discord.Embed(color=0xC47A31, title=f"<:UlsanRoad:1226025111799205970> 울산광역시 도로교통공단", description="###\n{name}님의 기능시험 합격을 축하드립니다!\n지금 바로 면허증을 발급받으실 수 있습니다.\n\nhttps://discord.com/channels/1183359422324543489/1183420558025695323 채널로 이동하신 후,\n**/면허증발급받기** 명령어를 이용하세요!\n\n도로교통공단장")
                        await user.send(embed=Openembed)
                        await message.delete()  # 멘션된 사용자에게 보낸 메시지 삭제
                        channel = bot.get_channel(1180092853158944808)
                        await channel.send(content=f"{name}님이 합격하셨습니다.\n<@{user.id}>")  # 디스코드 채널에 합격 메시지 전송
                        data = db.UlsanCarPr.insert_one(
                            {
                                "PlrName": name,
                                "DiscordId" : str(user.id)
                            }
                        )
                else:
                    await interaction.followup.send("합격한 사용자를 멘션해주세요.", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.response.send_message("시간이 초과되었습니다. 다시 시도해주세요.")
        if select.values[0] == '3':
            await interaction.response.send_message("어떤 분을 기능시험에 등록할까요?", ephemeral=True)
            await asyncio.sleep(1)

            try:
                message = await bot.wait_for('message', timeout=10)

                # 명령을 실행한 사용자와 메시지를 보낸 사용자가 일치하는지 확인
                if message.author.id != interaction.user.id:
                    await interaction.followup.send("명령어를 사용한 사용자만 멘션해주세요.", ephemeral=True)
                    return

                mentioned_users = message.mentions
                if mentioned_users:
                    for user in mentioned_users:
                        user_data = db.UlsanVerify.find_one({"DiscordId": str(user.id)})
                        name = user_data.get("PlrName")
                        Openembed= discord.Embed(color=0xC47A31, title=f"<:UlsanRoad:1226025111799205970> 울산광역시 도로교통공단", description=f"###\n {name}님의 기능시험이 접수되었습니다\n**[여기를 클릭하여](https://discord.gg/kBxyajtP7A)** 도로교통공단 디스코드 서버에 가입하세요.\n***(미가입 시, 기능시험 응시가 불가합니다)***\n###\n시험 응시 시, 유의사항\n* 반드시 **[도로교통공단서버](https://discord.gg/kBxyajtP7A)**에서 코스를 숙지하세요 (코스를 숙지하지 않아 발생하는 감점 또는 실격처리는 책임져드리지 않습니다.)\n* 감점안내 채널로 이동하시면, 운전면허 취득 안내문 파일(pdf, 한글파일)이 있습니다. 안내문 파일에는 감점기준, 유의사항 등이 안내되어있으니 반드시 확인해주시기 바랍니다.\n* 안내된 고시시각 전까지 대기실에 미입실 할 경우, 자동 탈락처리 됩니다.\n\n도로교통공단")
                        await user.send(embed=Openembed)
                        await message.delete()  # 멘션된 사용자에게 보낸 메시지 삭제
                        channel = bot.get_channel(1236876509822582844)
                        await channel.send(content=f"{name}님의 기능시험이 등록되었습니다.\n<@{user.id}>")  # 디스코드 채널에 합격 메시지 전송
                else:
                    await interaction.followup.send("합격한 사용자를 멘션해주세요.", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.response.send_message("시간이 초과되었습니다. 다시 시도해주세요.")



@bot.tree.command(name="면허증발급받기", description="해당 슬래시는 장내기능시험 합격자만 이용할 수 있어요")
async def Ulsan(interaction: discord.Interaction):
    user_data = db.UlsanCarPr.find_one({"DiscordId": str(interaction.user.id)})
    if user_data:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 면허증을 발급 받을까요?", description=f"{interaction.user.mention}님은 면허증을 발급 받으실 수 있어요.\n운전면허증을 발급 받으려면 ₩12,900을 지불해야해요.")
        button = BuyCardCar("딜리페이로 결제하기")
        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 장내기능시험 합격자만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class BuyCardCar(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="<:dilly:1209793389176819722>")

    async def callback(self, interaction):
        embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 쉽고 간편한 결제, Dilly Pay", description=f"결제를 진행하기 위해 다이렉트 메세지로 결제 확인 메세지를 보내드렸어요.\n다이렉트 메세지를 확인해주세요!")
        Dm = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 결제를 진행할까요?", description=f"###\n도로교통공단 면허증 발급(12900원) 을(를) 구매할까요?\n구매를 원하시면 아래 버튼을 눌러주세요.")
        button = BuyedCardCar("일시불로 결제하기", "12900")
        view = discord.ui.View()
        view.add_item(button)
        user = await bot.fetch_user(interaction.user.id)
        await user.send(embed=Dm, view=view)
        await interaction.response.edit_message(embed=embed, view=None)




class BuyedCardCar(discord.ui.Button):
    def __init__(self, label, CardPrice):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="<:dilly:1209793389176819722>")
        self.CardPs = CardPrice

    async def callback(self, interaction):
        dillyData = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        user_data = db.UlsanVerify.find_one({"DiscordId": str(interaction.user.id)})

        SetName = dillyData.get("SetName")
        To_money = dillyData.get("Money")
        playerName = user_data.get("PlrName")
        money = self.CardPs

        Sd_Money_Money = int(To_money)-int(money)

        if int(To_money) >= int(money):
            random_numbers = ''.join(random.choices('0123456789', k=6))
            CardCarNumber = "26-24-" + random_numbers + "-01"


            embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1183243842279985194> 결제가 완료되었어요", description=f"결제가 성공적으로 완료되었어요.\n###\n결제내역 📃\n* 상품명 : 도로교통공단 면허증 발급\n* 가격 : 12900원(일시불 결제)")
            Diller = discord.Embed(color=0x5F1F91, title="<:ulsan_Road:1225061996613992479> 울산광역시 도로교통공단", description=f"###\n면허증이 발급 되었습니다\n{SetName}님의 운전면허증이 발급되었습니다.\n\n`면허번호 : {CardCarNumber}`\n\n도로교통공단")
            
            Dilly_DB.PayNumber.update_one(
                {"discordId": str(interaction.user.id)},
                {"$set": {"Money": Sd_Money_Money}}
            )

            data = db.UlsanCar.insert_one(
                {
                    "PlrName": playerName,
                    "DiscordId" : str(interaction.user.id),
                    "Value" : True,
                    "CardNumber" : CardCarNumber
                }
            )

            db.UlsanCarPr.delete_one({"DiscordId": str(interaction.user.id)})

            
            user = await bot.fetch_user(interaction.user.id)
            await user.send(embed=Diller, view=None)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=0x1a3bc6, title="오류가 발생했어요", description="계좌의 잔액이 부족해요.")
            await interaction.response.edit_message(embed=embed, view=None)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

@bot.tree.command(name="딜리dilly", description="딜리를 이용할 수 있는 명령어예요")
async def password(interaction: discord.Interaction):
    if interaction.channel_id == 1183420558025695323:
        viewww = DillySelect()
        await interaction.response.send_message("딜리의 무슨 서비스를 이용해볼까요?", view=viewww, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 <#1183420558025695323> 채널에서만 이용하실 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class DillySelect(View):
    @discord.ui.select(
        placeholder="서비스 선택",
        options=[
            discord.SelectOption(
                label="딜리계좌 개설하기",
                value='1',
                description="딜리계좌를 개설하여 딜리가 제공하는 서비스를 이용해보세요.",
                emoji="🏧"
            ),
            discord.SelectOption(
                label="계좌정보 확인하기",
                value='2',
                description="나의 딜리계좌 정보를 확인해보세요.",
                emoji="💳"
            ),
            discord.SelectOption(
                label="딜리계좌로 송금하기",
                value='3',
                description="딜리계좌에서 딜리계좌로 간편하게 송금해보세요.",
                emoji="💸"
            ),
            discord.SelectOption(
                label="비밀번호 찾기",
                value='4',
                description="비밀번호를 분실하셨나요? 딜리가 찾아드릴게요.",
                emoji="🔍"
            ),
            discord.SelectOption(
                label="딜리프로 신청하기",
                value='5',
                description="딜리페이와 딜리프로 서비스를 신청하실 수 있어요.",
                emoji="👔"
            )
        ]
    )


    async def select_callback(self, interaction, select):
        select.disabled = True
        
        if select.values[0] == '1':
            await interaction.response.send_modal(DillyMadePay())
        if select.values[0] == '2':
            user_data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})  # 컬렉션 이름 수정
    
            if user_data:
                dcId = user_data.get("discordId")
                if dcId == str(interaction.user.id):
                    # 사용자 데이터에서 PayNumberBar 필드의 값을 가져옴
                    pay_number = user_data.get('PayNumberBar', '계좌번호가 없습니다.')
                    # 사용자에게 디렉트 메시지 보내기
                    button = Check("계좌 정보 확인하기")
                    view = discord.ui.View()
                    view.add_item(button)

                    await interaction.response.send_message(f"{interaction.user.mention}님의 명의로 개설된 계좌정보를 디엠으로 보내드릴게요.\n`서버 멤버가 보내는 다이렉트 메시지 허용하기`를 활성화 하셨다면,\n아래 버튼을 눌러주세요", view=view , ephemeral=True)
                else:
                    await interaction.response.send_message(f"예금주 이외엔 계좌번호를 확인할 수 없어요.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{interaction.user.mention}님의 명의로 개설된 계좌를 찾지 못했어요.", ephemeral=True)
        
        if select.values[0] == '3':
            user_data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})

            if user_data :
                await interaction.response.send_modal(alreadySend())
            else:
                embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description=f"{interaction.user.mention}님은 아직 딜리계좌가 없는 것 같아요.\n`/딜리계좌개설하기` 명령어를 통해 계좌를 개설하신 후, 다시 시도해주세요")

                await interaction.response.send_message(embed=embed, ephemeral= True)

        if select.values[0] == '4':
            await interaction.response.send_modal(PasswordReset())

        if select.values[0] == '5':
            await interaction.response.send_modal(DillyPro())


class PasswordReset(discord.ui.Modal, title="딜리계좌 비밀번호 찾기"):
    user_name = discord.ui.TextInput(label="로블록스 닉네임을 알려주세요",placeholder="디스플레이 닉네임X", required=True, min_length=2, style=discord.TextStyle.short)
    user_paynumber = discord.ui.TextInput(label="계좌번호를 알려주세요 (-포함)",placeholder="계좌번호에서 -를 포함해서 입력해주세요", required=True, min_length=15, max_length=15, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        user_data = Dilly_DB.PayNumber.find_one({"PlayerName": f"{self.user_name.value}"})


        if user_data:
            get_PayNumber = Dilly_DB.PayNumber.find_one({"PayNumberBar": f"{self.user_paynumber.value}"})

            if get_PayNumber :
                discord_Id = user_data.get("discordId")
                rbloxId = user_data.get("PlayerName")

                await interaction.response.send_message(content="계좌를 만들 때, 인증된 디스코드 계정 디엠으로 인증 확인 메세지를 보내드렸어요.", ephemeral= True)
                embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 딜리계좌 인증요청", description=f"계좌 비밀번호 변경 요청이 들어왔습니다.\n요청을 보내신 분이 본인이시라면 '네, 제가 맞습니다'버튼을 눌러주세요.")

                button = verify("네, 제가 맞습니다")
                view = discord.ui.View()
                view.add_item(button)

                user = await bot.fetch_user(discord_Id)
                await user.send(embed=embed, view=view)
            else:
                embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description="입력한 정보로 계좌정보를 불러올수 없어요.\n닉네임과 계좌번호에 오타가 있는지 확인해주세요")
                embed.add_field(name="입력하신 로블록스 닉네임", value=f"{self.user_name.value}", inline=True)
                embed.add_field(name="입력하신 계좌번호", value=f"{self.user_paynumber.value}", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral= True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description="입력한 정보로 계좌정보를 불러올수 없어요.\n닉네임과 계좌번호에 오타가 있는지 확인해주세요")
            embed.add_field(name="입력하신 로블록스 닉네임", value=f"{self.user_name.value}", inline=True)
            embed.add_field(name="입력하신 계좌번호", value=f"{self.user_paynumber.value}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral= True)




class verify(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="👤")

    async def callback(self, interaction):
        await interaction.response.send_modal(NewPassword())



class NewPassword(discord.ui.Modal, title="딜리계좌 비밀번호 변경하기"):
    newpas = discord.ui.TextInput(label="변경할 비밀번호를 입력하세요", placeholder="변경할 비밀번호를 입력", required=True, min_length=1, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        user_data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})

        if user_data:
            pay_Number = user_data.get("PayNumberBar")
            NickName = user_data.get("PlayerName")
            SetName = user_data.get("SetName")
            print(NickName)

            current_password = user_data.get('Password')

            # Check if the current password matches before updating
            if current_password == self.newpas.value:
                await interaction.response.send_message("현재 비밀번호와 동일한 비밀번호는 사용할 수 없어요.")
                return

            # Update the password
            Dilly_DB.PayNumber.update_one(
                {"PlayerName": NickName},
                {"$set": {"Password": self.newpas.value}}
            )

            embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 비밀번호가 변경되었습니다", description=f"{NickName}님의 딜리계좌 비밀번호가 정상적으로 변경되었습니다")
            embed.add_field(name="예금주", value=f"{SetName}", inline=True)
            embed.add_field(name="계좌번호", value=f"{pay_Number}", inline=True)
            embed.add_field(name="예금주 닉네임", value=f"{NickName}", inline=True)
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message("사용자 데이터를 찾을 수 없습니다.")



class alreadySend(discord.ui.Modal, title="딜리계좌로 송금하기"):
    payNumber = discord.ui.TextInput(label="어떤 계좌로 돈을 보낼까요?", placeholder="계좌번호 입력 (-포함)", required=True, min_length=15, max_length=15, style=discord.TextStyle.short)
    howMoney = discord.ui.TextInput(label="얼마를 보낼까요?", placeholder="숫자 입력", required=True, min_length=1, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        Send_User = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        To_User = Dilly_DB.PayNumber.find_one({"PayNumberBar": self.payNumber.value})

        def is_number(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        if not is_number(self.howMoney.value):
            embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 오류가 발생했어요", description="금액은 숫자로만 입력해주세요.")
            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
            return

        if To_User:
            User_Number = Send_User.get("PayNumberBar")
            pay_Number = To_User.get("PayNumberBar")
            SetName = To_User.get("SetName")
            To_DiscordId = To_User.get("discordId")
            To_money = To_User.get("Money")
            money = self.howMoney.value

            Sd_Money = Send_User.get("Money")
            Sd_Name = Send_User.get("SetName")
            Sd_DiscordId = Send_User.get("discordId")
            Sd_PayNumber = Send_User.get("PayNumberBar")
            Sd_Money_Money = int(Sd_Money) - int(money)
            To_Money_Money = int(To_money) + int(money)

            if pay_Number != User_Number:
                if int(self.howMoney.value) > 0 :
                    if int(Sd_Money) >= int(money):
                            Dilly_DB.PayNumber.update_one(
                                {"discordId": str(interaction.user.id)},
                                {"$set": {"Money": Sd_Money_Money}}
                            )

                            Dilly_DB.PayNumber.update_one(
                                {"PayNumberBar": self.payNumber.value},
                                {"$set": {"Money": To_Money_Money}}
                            )

                            embed = discord.Embed(color=0x1a3bc6, title=f"<:dilly:1209793389176819722> {SetName}님에게 {money}원 송금완료!")
                            embed.add_field(name="보내시는 분", value=Sd_Name, inline=True)
                            embed.add_field(name="받는 분", value=SetName, inline=True)
                            embed.add_field(name="보낸 금액", value=f"{money}원", inline=True)

                            toEmbed = discord.Embed(color=0x1a3bc6, title=f"<:dilly:1209793389176819722> {Sd_Name}님이 내 계좌로 {money}원을 보냈어요", description=f"남은 잔액 : {To_Money_Money}")
                            SdEmbed = discord.Embed(color=0x1a3bc6, title=f"<:dilly:1209793389176819722> {SetName}님에게 {money}원을 보냈어요", description=f"남은 잔액 : {Sd_Money_Money}")

                            user = await bot.fetch_user(To_DiscordId)
                            Sduser = await bot.fetch_user(Sd_DiscordId)
                            await user.send(embed=toEmbed)
                            await Sduser.send(embed=SdEmbed)
                            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    else:
                        embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 오류가 발생했어요", description="계좌의 잔액이 부족해요.")
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                else:
                    embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 오류가 발생했어요", description="올바른 값을 입력해주세요.")
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
            else:
                embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 오류가 발생했어요", description="자신에겐 돈을 보낼 수 없습니다.")
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

# ...

        else:
            embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 오류가 발생했어요", description="존재하지 않는 계좌번호 입니다.\n송금하시려는 계좌번호를 다시한번 확인해주세요")
            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)



class Check(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="📄")
            
    async def callback(self, interaction):
        user_data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        paynumberBar = user_data.get('PayNumberBar')
        paynumber = user_data.get('PayNumber')
        SetName = user_data.get('SetName')
        UserMoney = user_data.get('Money')
        robloxName = user_data.get('PlayerName')
        Dcid = user_data.get('discordName')

        embed = discord.Embed(color=0x1a3bc6, title=f"<:dilly:1209793389176819722> {SetName}님의 계좌정보")
        embed.add_field(name="> 계좌번호 (-포함)", value=paynumberBar, inline=True)
        embed.add_field(name="> 계좌번호 (-제외)", value=paynumber, inline=True)
        embed.add_field(name="> 예금주 명", value=SetName, inline=True)
        embed.add_field(name="> 계좌 잔액", value=f"{UserMoney}원", inline=True)
        embed.add_field(name="> 로블록스", value=robloxName, inline=True)
        embed.add_field(name="> 디스코드", value=Dcid, inline=True)
        view = discord.ui.View()
        user = await bot.fetch_user(interaction.user.id)
        await user.send(embed=embed)
        await interaction.response.edit_message(content=f"{SetName}님의 다이렉트 메세지로 계좌정보를 보내드렸어요!", view=None)

class DillyMadePay(discord.ui.Modal, title="딜리계좌 개설 시작하기"):
    RBLXName = discord.ui.TextInput(label="로블록스 닉네임을 알려주세요", placeholder="닉네임 이외엔 다른 문자를 삽입하지 마십시오. 예) Dev_Usim", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        existing_data = Dilly_DB.verify.find_one({"DiscordId": str(interaction.user.id)})
        user_data = Dilly_DB.PayNumber.find_one({"discordId": str(interaction.user.id)})
        UserId = interaction.user.id

        if user_data :
            embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description=f"{interaction.user.mention}님의 계정으로 개설된 계좌가 이미 존재합니다.\n계좌번호를 조회하시려면 `/내계좌번호확인하기` 명령어를 이용해주세요!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if existing_data:
                DcoName = existing_data.get("DiscordName") if existing_data else None
                # 이미 데이터가 존재할 경우 실패 메시지 전송
                embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description=f"해당 계정은 이미 인증 진행중입니다")
                button = Cancel("인증 취소하기", existing_data.get("DiscordId"))
                view = discord.ui.View()
                view.add_item(button)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            else:
                # 데이터가 없을 경우 계좌 개설
                data = Dilly_DB.verify.insert_one(
                    {
                        "PlrName": self.RBLXName.value,
                        "DiscordId" : str(interaction.user.id),
                        "DiscordName": interaction.user.name
                    }
                )
                embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 딜리 인증 시작하기", description=f"{self.RBLXName.value}님의 계좌 개설을 위해 아래 버튼을 클릭하여\n인증을 진행해주세요!")

                button = discord.ui.Button(label="인증하러 가기", style=discord.ButtonStyle.blurple, emoji="✅", url="https://www.roblox.com/games/15503722646/Dilly")
                view = discord.ui.View()
                view.add_item(button)

                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class Cancel(discord.ui.Button):
    def __init__(self, label, rblox):
        super().__init__(label=label, style=discord.ButtonStyle.red, emoji="💥")
        self.rblox = rblox

    async def callback(self, interaction):

        await interaction.response.send_message(f"<@{self.rblox}> 님의 인증이 취소되었어요.\n재인증을 시도하시려면, `/딜리계좌 개설하기` 명령어를 이용해주세요!", ephemeral=True)
        Dilly_DB.verify.delete_one({"DiscordId": self.rblox})
        Button.disabled = False


class ImageSelect(discord.ui.Modal, title="이미지 선택하기"):
    ImageLink = discord.ui.TextInput(label="이미지 링크를 첨부하세요", placeholder="Link", required=True, min_length=2, style=discord.TextStyle.short)

    def __init__(self, message):
        super().__init__()
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.message.embeds[0]
        discordId = embed.fields[2].value
        user_data = db.UlsanSaup.find_one({"DiscordId": str(discordId)})

        Afterembed = discord.Embed(color=0x1a3bc6, title="<:ulsan:1183391095900602378> 딜리페이 가맹점 신청 승인 완료", description=f"<@{discordId}>님의 딜리페이 가맹점 신청이 성공적으로 승인되었습니다.")
        Afterembed.set_image(url=self.ImageLink.value)
        await self.message.edit(content="", embed=Afterembed, view=None)
        await self.message.add_reaction("✅")
        guild = interaction.guild
        member = guild.get_member(int(discordId))
        sendUser = discord.Embed(color=0x1a3bc6, title="<:ulsan:1183391095900602378> 딜리페이 가맹점 승인 안내", description=f"> [Web발신]\n\n귀하의 가맹점이 딜리페이 가맹점으로 승인되었음을 진심으로 축하드립니다.\n자세한 사항은 딜리매니저가 조만간 상세히 설명을 도와드릴 예정입니다.\n딜리와 함께 할 수 있어서 영광입니다! 소중한 시간 내어 신청해주셔서 고맙습니다.\n\n** 본인이 신청하지 않았다면, 반드시 문의하시기 바랍니다.\n\n딜리페이 가맹점 이미지 다운로드 받기 > {self.ImageLink.value}")
        await member.send(embed=sendUser)

@bot.tree.context_menu(name="💳 딜리페이 가맹점 신청 수락하기")
async def Con(interaction: discord.Interaction, message: discord.Message):
    getRole = discord.utils.get(interaction.guild.roles, id=1183359440934682634)
    userRole = interaction.user.roles

    if getRole in userRole:
        if interaction.channel_id == 1209861763621720175:
            image_select = ImageSelect(message)
            await interaction.response.send_modal(image_select)
        else:
            embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"전용 채널에서 이용해주세요.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"해당 명령어는 울산광역시장만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class DillyPro(discord.ui.Modal, title="딜리페이 가맹점 신청하기"):
    SaupNumber = discord.ui.TextInput(label="사업자 등록 번호를 알려주세요",placeholder="135-12-34567", required=True, min_length=2, style=discord.TextStyle.short)
    haveMoney = discord.ui.TextInput(label="현재 얼마를 소지하고 계신가요?",placeholder="0원", required=True, min_length=2, style=discord.TextStyle.short)
    howToUse = discord.ui.TextInput(label="딜리프로를 어떻게 사용하실 예정이신가요?",placeholder="구체적으로 알려주세요", required=True, min_length=30, style=discord.TextStyle.long)
    Why = discord.ui.TextInput(label="딜리페이를 선택하신 이유를 알려주세요",placeholder="구체적으로 알려주세요", required=True, min_length=30, style=discord.TextStyle.long)
    

    async def on_submit(self, interaction: discord.Interaction):
        user_data = db.UlsanSaup.find_one({"SaupNumber": f"{self.SaupNumber.value}"})

        if user_data:
                discord_Id = user_data.get("DiscordId")
                SaupName = user_data.get("SaupName")

                embed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 입력하신 정보가 맞나요?", description=f"- 딜리프로 심사는 최대 1주일 소요되실 수 있습니다.\n- 심사 중, 딜리페이 가맹점을 운영하는 데 부적합하다고 판단되면, 부결될 수 있습니다.\n- 딜리프로, 딜리페이 가입 시, 최대 500,000원 (오십만원)의 부과세가 부과됩니다.\n-")
                embed.add_field(name="사업의 상호명", value=f"{SaupName}", inline=True)
                embed.add_field(name="사업자 등록번호", value=f"{self.SaupNumber.value}", inline=True)
                embed.add_field(name="현재 소지금액", value= self.haveMoney.value, inline=True)
                embed.add_field(name="딜리프로 용도", value= self.howToUse.value, inline=True)
                embed.add_field(name="딜리프로를 신청하신 이유", value= self.Why.value, inline=True)
                button = StartDilly("신청하기", self.SaupNumber.value, self.haveMoney.value, self.howToUse.value, self.Why.value)
                view = discord.ui.View()
                view.add_item(button)

                await interaction.response.send_message(embed=embed, view=view, ephemeral= True)


        else:
            embed = discord.Embed(colour=discord.Colour.red(), title="<:dilly:1209793389176819722> 오류가 발생했어요", description="운영중이신 사업이 없으신 것 같아요.")
            await interaction.response.send_message(embed=embed, ephemeral= True)

class StartDilly(discord.ui.Button):
    def __init__(self, label, saupNumber, haveMoney, howtoUse, why):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji="👤")
        self.number= saupNumber
        self.money= haveMoney
        self.howtoUse= howtoUse
        self.why= why

    async def callback(self, interaction):
        user_data = db.UlsanSaup.find_one({"SaupNumber": f"{self.number}"})
        discord_Id = user_data.get("DiscordId")
        if interaction.user.id == int(discord_Id):
            SaupName = user_data.get("SaupName")
            user = await bot.fetch_user(int(discord_Id))
            AfterEmbed = discord.Embed(color=0x1a3bc6, title="<:dilly:1209793389176819722> 딜리페이 가맹점 신청 완료!", description=f"> [Web발신]\n\n딜리페이 가맹점 신청이 성공적으로 완료되었습니다.\n\n- 딜리프로 심사는 최대 1주일 소요되실 수 있습니다.\n- 심사 중, 딜리페이 가맹점을 운영하는 데 부적합하다고 판단되면, 부결될 수 있습니다.\n- 딜리프로, 딜리페이 가입 시, 최대 500,000원 (오십만원)의 부과세가 부과됩니다.\n- 신청일로부터 7일이 경과해도 승인 안내 문자를 받지 못한 경우, 이는 거절된 것으로 간주됩니다.\n-")
            AfterEmbed.add_field(name="> 사업의 상호명", value=f"{SaupName}", inline=True)
            AfterEmbed.add_field(name="> 사업자 등록번호", value=f"{self.number}", inline=True)
            AfterEmbed.add_field(name="> 현재 소지금액", value= self.money, inline=True)
            AfterEmbed.add_field(name="> 딜리프로 용도", value= self.howtoUse, inline=True)
            AfterEmbed.add_field(name="> 딜리프로를 신청하신 이유", value= self.why, inline=True)
            await user.send(embed=AfterEmbed)
            SendCn = discord.Embed(color=0x1a3bc6, title="<:ulsan:1183391095900602378> 등록 신청 완료!", description=f"자세한 사항은 보내드린 다이렉트 메세지를 확인해주세요")
            await interaction.response.edit_message(embed=SendCn, view=None)
            PleaseEmbed = discord.Embed(color=0x1a3bc6, title="<:ulsan:1183391095900602378> 딜리페이 가맹점 신청이 접수 되었어요")
            PleaseEmbed.add_field(name="> 신청하신 분 멘션", value=f"<@{interaction.user.id}>", inline= True)
            PleaseEmbed.add_field(name="> 해당 사업자 분 멘션", value=f"<@{discord_Id}>", inline= True)
            PleaseEmbed.add_field(name="> 아이디", value=discord_Id, inline= True)
            PleaseEmbed.add_field(name="> 상호명", value=SaupName, inline= True)
            PleaseEmbed.add_field(name="> 사업자 등록번호", value=f"{self.number}", inline=True)
            PleaseEmbed.add_field(name="> 현재 소지금액", value= self.money, inline=True)
            PleaseEmbed.add_field(name="> 딜리프로 용도", value= self.howtoUse, inline=True)
            PleaseEmbed.add_field(name="> 딜리프로를 신청하신 이유", value= self.why, inline=True)

            channel = bot.get_channel(1209861763621720175)
            await channel.send(embed=PleaseEmbed)
        else:
            embed = discord.Embed(color=0x1a3bc6, title="<:ulsan:1183391095900602378> 오류가 발생했어요", description=f"사업자 이외엔 신청하실 수 없어요.")
            await interaction.response.edit_message(embed=embed, view=None)

as_token = os.environ['BOT_TOKEN']
bot.run(as_token)
