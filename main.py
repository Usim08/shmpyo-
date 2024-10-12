from typing import Any
import os
import discord
import pymongo
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import motor.motor_asyncio
from roblox import Client
from roblox import AvatarThumbnailType  # AvatarThumbnailType을 임포트


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.all()

bot = commands.Bot(command_prefix="!", intents=intents, application_id="1193950006714040461")

# MongoDB 클라이언트 연결
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Usim:1234@cluster0.2mpijnh.mongodb.net/?retryWrites=true&w=majority")
db = client.shmpyo
roblox_client = Client("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_46E968A6B38AFE39D46A99D9598B6AB1A503F5C18DBE7942D048DECC21638F427F9C4FCB0BDE061025519D04A7369CE8C1248D08EF471DF0DFF0D7A4FA4A4B505C31369346355E7CDBFF67D79C8A3D8CE2E122CB5F288B35AF5893D1118AA64D794256C4C33AB5D19F56DAA2F0C9E3BEDE8303F0EB3AF749A99EEBCF1AD33C76AC968DDDCD2E1691E063ED7E63D8E51BB51679D59E2C6A2A04DB60EE629B20DAA84D77F3916FFBD3A50831ED9C74374D6AE113E23F2DC0865E346041265A3512A72787BE3010BCB743C730C44C8C3D8A1F2BF996AF3E70B0D832380A63FBF4971170B1AAB321E61EEAEDA0CFAEBF11609EA76D72168E068E4BBED4E27DBA06C54613D536CA13930AA8BDB6034535C98B39ADC2FCA8D09819FFD84BCF0030C0726355A3EB8B89351765295C56E095DD4090AE924B1385C7646F241F04A87BA28EB672CFC907746196B819AC741797B6F9FDE631DFDEC367FABB554965CF73EA52A49DC54CAA05A04F671D9496A89AF182504250E5BF227233F1B49B1C9E2BBFB4892079BCE84F6E1BCAF9509721AF1C777B45F80E17A8A1FA6B7EFEE41AA09D6FAFD2E7EDEED0E4B3F5A01E48BFFC77CC9FF0D6C56421A0625A5D7F71BC3BD1EB2D254E887FF3DD8B0285706393C56466DD38A424D2017F5F38E8C0F6938D24EB0943FFDF15D1909D973E9E71691DF5767D8195DF419DAE189FB6695D12AE79961AC5550CE531B43BB901BADC62BD0D584D31F95D91D22B6C2F132441281B8FEB29870CDA50C44FCE97B3302DB15E64B6B4393B585ECEE9DB123B98E7FA17E52C12FF99FB45B8F85DFA6D5C1041341312E4BFA5473C3FAF22B0D108AF4E6071915C84716022DDCF5DB6F8BD4F96466F3A11A86E0C3384CBE551ACC748492445CBC5C095C0A7000DFC3AB2BAD98F5FF8C17B002317")

@bot.event
async def on_ready():
    channel = bot.get_channel(1284347203204415539)
    await channel.send(content="쉼표봇이 준비되었습니다")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="쉼표, shmpyo"),status=discord.Status.idle)
    print("봇 준비완료")

    # MongoDB Change Stream 설정
    asyncio.create_task(monitor_db_changes())


@bot.event
async def on_member_join(member):

    role_id = 1193969637226987600
    role = member.guild.get_role(role_id)

    if role:
        user_data = await db.userinfo.find_one({"discordId": str(member.id)})
        if not user_data:
            await member.add_roles(role)
        else:
            guild = bot.get_guild(1193811936673026129)  # 디스코드 서버 ID 입
            roblox_name = user_data.get("playerName")

            cus = guild.get_role(1284389914032476181)  # 부여할 디스코드 역할 ID 입력
            await member.add_roles(cus)
            await member.edit(nick=f"{roblox_name}")

            embed = discord.Embed(color=0x2c4bce, title="다시 돌아오셨네요 👋", description=f"{roblox_name}님의 인증 이력이 있어 자동인증 해드렸어요. 쉼표샵으로 돌아가보세요!")
            button = discord.ui.Button(label="쉼표샵으로 돌아가기", style=discord.ButtonStyle.blurple, emoji="↩️", url="https://discord.gg/FW6AxEe8Xj")
            view = discord.ui.View()
            view.add_item(button)
            embed.set_image(url="https://media.discordapp.net/attachments/1193969295881933010/1284440329038200903/38318689a95b6feb.png?ex=66e6a3c6&is=66e55246&hm=95e6816a1f4f25e3e2dc2408f45374b673c98079499a21faf6832b02f19f6c59&=&format=webp&quality=lossless")
            await member.send(embed=embed, view=view)





@bot.event
async def on_message(message):

    channel_id = 1193969935593001091
    if message.channel.id == channel_id:
        await message.delete()

role_id = 1284390999904489596  # 특정 역할 ID
CATEGORY_ID = 1294588527560097913  # 특정 카테고리 ID
message_collection = db["channel_messages"]

@bot.event
async def on_guild_channel_create(channel):
    # 카테고리 확인
    if isinstance(channel, discord.TextChannel) and channel.category_id == CATEGORY_ID:
        embed = discord.Embed(
            title="<:shmpyo_loading:1294601454048510033> 담당 매니저 배정을 기다리고 있어요",
            description="### 상담 전, 안내사항 📃\n\n> - 배정되는 동안 안내해드린 양식을 미리 작성해 주시면, 보다 빠르게 담당 매니저를 배정받으실 수 있습니다.\n> - 상담이 시작되면, 담당 매니저 보호와 행정 서비스 품질 향상을 위해 상담 내용은 모두 기록됩니다.",
            color=0x2c4bce
        )
        await asyncio.sleep(1)
        message = await channel.send(embed=embed)
        
        # 메시지 정보를 DB에 저장
        await message_collection.insert_one({"channel_id": channel.id, "message_id": message.id})

async def get_message_id(channel_id):
    # DB에서 채널 ID로 메시지 ID 찾기
    message_data = await message_collection.find_one({"channel_id": channel_id})
    return message_data["message_id"] if message_data else None

@bot.event
async def on_message(msg):
    if msg.content == "!담당하기":
        member = msg.author
        role = discord.utils.get(member.guild.roles, id=role_id)

        if role in member.roles:
            # 저장된 메시지 ID로 메시지 찾기
            message_id = await get_message_id(msg.channel.id)
            userName = await db.userinfo.find_one({"discordId": str(member.id)})
            if message_id:
                try:
                    old_message = await msg.channel.fetch_message(int(message_id))
                    await old_message.delete()  # 기존 임베드 메시지 삭제
                    await msg.delete()

                    # 새로운 임베드 전송
                    embed = discord.Embed(

                        title="상담이 시작되었습니다!",
                        description=f"### 담당 매니저 : <:shmpyo_manager:1294603617990348800> {userName.get('playerName')}\n담당 매니저에게 폭언, 욕설 등은 삼가해주세요.\n담당 매니저 보호와 행정 서비스 품질 향상을 위해 상담 내용은 모두 기록됩니다.",
                        color=0x2c4bce
                    )
                    await msg.channel.send(embed=embed)

                    await message_collection.delete_one({"channel_id": msg.channel.id})

                except discord.NotFound:
                    await msg.channel.send("이전 메시지를 찾을 수 없습니다.", delete_after=5)
            else:
                await msg.channel.send("메시지 ID를 찾을 수 없습니다.", delete_after=5)
        else:
            await msg.channel.send(f"{member.mention}, 이 명령어를 사용할 권한이 없습니다.", delete_after=5)

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

        user = await roblox_client.get_user_by_username(self.RBLXName.value)

        user_thumbnails = await roblox_client.thumbnails.get_user_avatar_thumbnails(
            users=[user.id],  # 사용자 ID를 사용
            size=(420, 420),
            type=AvatarThumbnailType.headshot  # AvatarThumbnailType 설정
        )
        
        # 썸네일 URL 추출
        user_thumbnail_url = None
        if user_thumbnails:
            user_thumbnail_url = user_thumbnails[0].image_url if user_thumbnails else None
        
        embed = discord.Embed(
            color=0x2c4bce,
            title="알려주신 정보를 확인 할게요 📃",
            description="입력하신 정보가 맞나요?\n입력하신 정보가 맞다면 **`다음`**을 눌러주세요!"
        )
        if user_thumbnail_url:
            embed.set_thumbnail(url=user_thumbnail_url)
            embed.add_field(name="> 로블록스 닉네임", value=f"{user.name}", inline= True)
            embed.add_field(name="> 로블록스 아이디", value=f"{user.id}", inline= True)
        
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


async def monitor_db_changes():
    pipeline = [{'$match': {'operationType': 'insert'}}]
    try:
        async with db.userinfo.watch(pipeline) as stream:
            async for change in stream:
                if change.get('fullDocument'):
                    discord_id = change['fullDocument'].get('discordId')
                    roblox_name = change['fullDocument'].get('playerName')

                    if discord_id and roblox_name:
                        guild = bot.get_guild(1193811936673026129)  # 디스코드 서버 ID 입력
                        if guild:
                            member = guild.get_member(int(discord_id))
                            if member:
                                try:
                                    # 로블록스 사용자 객체 가져오기

                                    role = guild.get_role(1284389914032476181)  # 부여할 디스코드 역할 ID 입력
                                    if role:
                                        await member.add_roles(role)
                                        await member.remove_roles(guild.get_role(1193969637226987600))
                                        await member.edit(nick=f"{roblox_name}")

                                    # DM 전송
                                    try:
                                        embed = discord.Embed(color=0x2c4bce, title="쉼표샵 인증이 완료됐어요 👏", description=f"{roblox_name}님의 인증이 완료됐어요. 이제 쉼표샵 상품을 구매할 수 있어요!")
                                        button = discord.ui.Button(label="쉼표샵으로 돌아가기", style=discord.ButtonStyle.blurple, emoji="↩️", url="https://discord.gg/FW6AxEe8Xj")
                                        view = discord.ui.View()
                                        view.add_item(button)
                                        embed.set_image(url="https://media.discordapp.net/attachments/1193969295881933010/1284440329038200903/38318689a95b6feb.png?ex=66e6a3c6&is=66e55246&hm=95e6816a1f4f25e3e2dc2408f45374b673c98079499a21faf6832b02f19f6c59&=&format=webp&quality=lossless")
                                        await member.send(embed=embed, view=view)
                                    except discord.Forbidden:
                                        print(f"DM 전송 실패 - 사용자: {discord_id}")
                                except Exception as e:
                                    print(f"로블록스에서 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
                        else:
                            print(f"디스코드 서버를 찾을 수 없습니다 - 서버 ID: 1170751784608858172")
    except Exception as e:
        print("전송 안됨")


@bot.tree.command(name="관리자전용", description="해당 명령어는 쉼표샵 매니저만 이용할 수 있어요")
async def password(interaction: discord.Interaction):
    if str(interaction.user.id) == str(751835293924982957):
        viewww = SelectAdmin()
        await interaction.response.send_message("선택사항을 선택하세요", view=viewww, ephemeral=True)
    else:
        embed = discord.Embed(color=0xC47A31, title="🚨 오류가 발생했어요", description=f"해당 명령어는 쉼표샵 매니저만 이용할 수 있어요.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SelectAdmin(View):
    @discord.ui.select(
        placeholder="선택사항 선택",
        options=[
            discord.SelectOption(
                label="파트너 등록하기",
                value='1',
                description="파트너를 등록합니다",
                emoji="🔑"
            ),
            discord.SelectOption(
                label="사전예약 등록하기",
                value='2',
                description="사전예약을 진행합니다",
                emoji="📃"
            )
        ]
    )

    async def select_callback(self, interaction, select):
        select.disabled = True

        if select.values[0] == '1':
            await interaction.response.send_modal(add_partner())

        if select.values[0] == '2':
            embed = discord.Embed(title="상품코드 목록", description="원하는 상품코드를 선택해주세요", color=0x00ff00)

            product_codes = db.goodNumber.find({})
            for product in await product_codes.to_list(length=None):
                code = product.get("code")
                name = product.get("name")
                embed.add_field(name=code, value=name, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

            try:
                def check(msg):
                    return msg.author == interaction.user and msg.channel == interaction.channel

                message = await bot.wait_for('message', timeout=30, check=check)

                selected_code = message.content

                await interaction.followup.send("사전예약 대상자를 멘션해주세요.", ephemeral=True)
                message = await bot.wait_for('message', timeout=30, check=check)

                mentioned_users = message.mentions
                if not mentioned_users:
                    await interaction.followup.send("사전예약 대상 유저를 멘션해주세요.", ephemeral=True)
                    return

                user = mentioned_users[0]
                secret_code_data = await db.secretcodes.find_one({"userid": ""})
                gn = await db.goodNumber.find_one({"code": selected_code})
                goodsName = gn["name"]

                if secret_code_data:
                    db.secretcodes.update_one(
                        {"_id": secret_code_data["_id"]},
                        {"$set": {"userid": str(user.id), "goodsnumber": selected_code, "goodsname":goodsName}}
                    )
                    # 유저에게 DM 보내기
                    secret_key = secret_code_data["secret"]

                    dm_embed = discord.Embed(color=0x2c4bce, title="사전예약이 완료되었어요 👏", description=f"## 사전예약이 정상적으로 처리되었어요!\n아래에서 비밀코드를 확인해 보세요.\n-# 비밀코드 유출 시, 이용규정에 따라 처벌받으실 수 있으니, 유의해주세요!")
                    button = discord.ui.Button(label="쉼표샵으로 돌아가기", style=discord.ButtonStyle.blurple, emoji="↩️", url="https://discord.gg/FW6AxEe8Xj")
                    view = discord.ui.View()
                    dm_embed.add_field(name="사전예약 상품", value=goodsName, inline=True)
                    dm_embed.add_field(name="상품의 비밀코드", value=f"||{secret_key}||", inline=True)
                    view.add_item(button)
                    dm_embed.set_image(url="https://media.discordapp.net/attachments/1291811758830518313/1294531011706617927/376674b49149509f.png?ex=670b5974&is=670a07f4&hm=21687593cae6d6042122e0f175665708c4bd99b6fd490e3d64b58808b01dfd6c&=&format=webp&quality=lossless")
                    await user.send(embed=dm_embed)
                    await interaction.followup.send(f"{user.mention}에게 DM으로 상품 코드를 보냈습니다.", ephemeral=True)
                else:
                    await interaction.followup.send("사용 가능한 시크릿 코드가 없습니다.", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.followup.send("시간이 초과되었습니다. 다시 시도해주세요.", ephemeral=True)



class add_partner(discord.ui.Modal, title="파트너 서버 등록하기"):
    serverId = discord.ui.TextInput(label="파트너 서버 아이디를 알려주세요", required=True, style=discord.TextStyle.short)
    serverName = discord.ui.TextInput(label="파트너 서버 이름을 알려주세요", required=True, style=discord.TextStyle.short)
    playerId = discord.ui.TextInput(label="파트너 서버장 아이디를 알려주세요", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        svid = self.serverId.value
        svn = self.serverName.value
        plrid = self.playerId.value
        guild = interaction.guild

        user_data = db.partner.insert_one({
            "serverId" : str(svid),
            "playerId" : plrid,
            "serverName" : svn
        })



        try:
            embed = discord.Embed(color=0x2c4bce, title="안녕하세요, 쉼표샵입니다 👋", description=f"# 쉼표샵 파트너가 되신 것을 축하드려요!\n안녕하세요, {svn} 서버장님! 쉼표샵 파트너가 되신 것을 축하드려요! 서버장님께서는 원활한 파트너 관리를 위하여, 디스코드 서버 파트너 채널에 아래 쉼표샵 소개글을 올려주세요.\n\n```# [로블록스 시스템 전문 판매 :: 쉼표샵](https://www.shmpyoshop.com/home)\n> ## :clipboard: **저희 쉼표샵은요..**\n> \n> \n> - 다른 샵에서는 찾아볼 수 없었던 퀄리티가 남다른 로블록스 상품들을 판매하고 있어요.\n> - 최고의 시스템 환경을 제공하여 유저가 보다 서버를 쾌적할 수 있게 도와드리고 있어요.\n> - 홈페이지에서 직접 상품 비밀코드를 입력하여 등록하기 때문에 보다 안전하고, 간편하게 이용할 수 있어요.\n\n> :house:  **홈페이지 바로가기**\n> ↪ https://www.shmpyoshop.com/home\n> \n> :speech_balloon:  **디스코드 바로가기**\n> ↪ https://discord.gg/FW6AxEe8Xj\n\n-# 간편하게 똑똑하게```")
            button = discord.ui.Button(label="쉼표샵으로 돌아가기", style=discord.ButtonStyle.blurple, emoji="↩️", url="https://discord.gg/FW6AxEe8Xj")

            view = discord.ui.View()
            view.add_item(button)
            guild = bot.get_guild(1193811936673026129)
            member = guild.get_member(int(plrid))
            await member.send(embed=embed, view=view)

            embed = discord.Embed(
                color=0x2c4bce,
                title="✅ 파트너 체결이 완료되었어요!",
                description=f"{svn}과(와) 파트너 체결이 완료되었습니다."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title="🚨 오류가 발생했어요",
                description="서버장님에게 디엠 보내기를 실패했어요."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

as_token = os.environ['BOT_TOKEN']
bot.run(as_token)
