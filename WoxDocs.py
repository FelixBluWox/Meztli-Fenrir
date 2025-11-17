#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord
from wox_sdb import db
from Chia import wreply, get_mention, user_auth, get_user_auth, get_author, on_guild
from discord.ext.commands import *
from Gaia import *
from Hati import color, embed_builder, user_banner, font_str, get_exp
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops, ImageColor
from functools import lru_cache as cache
from colorama import Fore
from random import randint
from time import time
from base64 import b64decode, b64encode
import hashlib
from dateutil.relativedelta import relativedelta
from datetime import datetime
from urllib.request import urlretrieve
from discord.ui import Button, Select, View, InputText, Modal, button, select
from discord.ext import tasks
from discord.ext.commands import Bot
import asyncio
import requests
#from e621 import E621
from math import sqrt

doc_log = Wox_log('WxDocs', color=Fore.LIGHTYELLOW_EX)
doc_log.info('loading...')

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#*   ROLCITY

def get_user(ctx=None, member=None, mcname=None, guild=None):

    if member:
        dcuser = member
        guild = member.guild
    elif mcname:
        if mcname in db['bots'][str(guild.id)]['extra']['players'] and guild:
            dcuser = guild.get_member(int(db['bots'][str(guild.id)]['extra']['players'][mcname]))
        else:
            dcuser = None
    else:
        if 'interaction' in vars(ctx):
            dcuser = ctx.user
            guild = ctx.guild
        elif 'prefix' in vars(ctx):
            dcuser = ctx.author
            guild = ctx.guild
        else:
            dcuser = None
            guild = None
            
    if dcuser:
        mcname = db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['mc'] if 'passport' in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra'] else None
    else:
        mcname = None

    return (dcuser, guild, mcname)

def construct_offline_player_uuid(username):
    #extracted from the java code:
    #new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));

    def add_uuid_stripes(string):
        string_striped = (
            string[:8] + '-' +
            string[8:12] + '-' +
            string[12:16] + '-' +
            string[16:20] + '-' +
            string[20:]
        )
        return string_striped

    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    #set the version to 3 -> Name based md5 hash
    byte_array[6] = hash[6] & 0x0f | 0x30
    #IETF variant
    byte_array[8] = hash[8] & 0x3f | 0x80

    hash_modified = bytes(byte_array)
    offline_player_uuid = add_uuid_stripes(hash_modified.hex())

    return offline_player_uuid

def get_player_skin(guild, username):

    url = "https://i.postimg.cc/ncRGvTNm/none.png"
    user_mcauth = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

    if username in db['bots'][str(guild.id)]['extra']['skins']:
        user_data = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['extra']['skins'][username], 'utf8')))
        url = user_data['textures']['SKIN']['url']

    elif user_mcauth.status_code == 200:
        user_data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user_mcauth.json()['id']}")
        db['bots'][str(guild.id)]['extra']['skins'][username] = user_data.json()['properties'][0]['value']
        
        user_data = json.loads(b64decode(bytes(user_data.json()['properties'][0]['value'], 'utf8')))
        url = user_data['textures']['SKIN']['url']

        db.save()
    
    urlretrieve(url, "./images/skin_temp.png")
    return './images/skin_temp.png'

async def render_passport(ctx=None, member=None, mcname=None):
    dcuser, guild, mcnick = get_user(ctx=ctx, member=member, mcname=mcname)
    if not dcuser:
        return None

    if "passport" not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
        return None
    
    type_colors = {
        "SV":"#BEBEBE",
        "PF":"#212939",
        "RG":"#00535F",
        "SP":"#DF2823",
        "DP":"#FAC200"
    }
    
    uuid = construct_offline_player_uuid(mcnick)

    num = str(db['bots']['1068420065692766308']['memberbase'][str(dcuser.id)]["number"])
    num = [*num]

    while len(num) < 3:
        num.insert(0, '0')
    num = ''.join(num)

    rolcity_txt = font_str("ROLCITY", ImageFont.truetype("./images/Antone.ttf", 56))

    pasaporte_txt = font_str("PASAPORTE", ImageFont.truetype("./images/Segoe UI.ttf", 24))
    tipo_txt = font_str("TIPO:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    pais_txt = font_str("PAIS:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    rc_txt = font_str("RC", ImageFont.truetype("./images/Instruction.otf", 44))
    dcid_txt = font_str("DCID:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    discord_txt = font_str("DISCORD:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    alias_txt = font_str("ALIAS:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    mcname_txt = font_str("MINECRAFT:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    edad_txt = font_str("EDAD:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    profesion_txt = font_str("PROFESION:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    nacimiento_txt = font_str("FECHA DE NACIMIENTO:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    expedicion_txt = font_str("FECHA DE EXPEDICION:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    sexo_txt = font_str("SEXO:", ImageFont.truetype("./images/Segoe UI.ttf", 19))
    ciudad_txt = font_str("CIUDAD DE ORIGEN:", ImageFont.truetype("./images/Segoe UI.ttf", 19))


    issuer = font_str(f"ALCALDIA DE {db['bots'][str(guild.id)]['extra']['cities'][db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issuer']].upper()}", ImageFont.truetype("./images/Antone.ttf", 44))

    passtype = font_str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['type'], ImageFont.truetype("./images/Instruction.otf", 44))
    userid = font_str(str(dcuser.id), ImageFont.truetype("./images/Instruction.otf", 44))
    username = font_str(dcuser.name, ImageFont.truetype("./images/Instruction.otf", 44))
    userdisc = font_str('#' + str(dcuser.discriminator), ImageFont.truetype("./images/Instruction.otf", 44))
    mcname = font_str(mcnick, ImageFont.truetype("./images/Instruction.otf", 44))
    age = font_str(str(relativedelta(datetime.now(), datetime(*db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['birth'])).years), ImageFont.truetype("./images/Instruction.otf", 44))
    profession = font_str(db['bots'][str(guild.id)]['extra']['professions'][db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['profession'][0]].upper(), ImageFont.truetype("./images/Instruction.otf", 44))
    birth = db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['birth']
    birth = font_str(f"{birth[2]}/{birth[1]}/{birth[0]}", ImageFont.truetype("./images/Instruction.otf", 44))
    issued = db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issued']
    issued = font_str(f"{issued[2]}/{issued[1]}/{issued[0]}", ImageFont.truetype("./images/Instruction.otf", 44))
    gender = font_str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['gender'], ImageFont.truetype("./images/Instruction.otf", 44))
    city = font_str(db['bots'][str(guild.id)]['extra']['cities'][db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issuer']].upper(), ImageFont.truetype("./images/Instruction.otf", 44))

    code = font_str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['code'][0], ImageFont.truetype("./images/Instruction.otf", 44))
    code2 = font_str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['code'][1], ImageFont.truetype("./images/Instruction.otf", 44))

    canvas = Image.open("./images/passportbg.png")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((0, 0, 1200, 800), outline=type_colors[db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['type']],width=20, radius=20)

    draw.text((40, 40), rolcity_txt.text, "Black", font=rolcity_txt.font)
    draw.text((80 + rolcity_txt.x, 40), issuer.text, "Black", font=issuer.font)
    draw.text((80 + rolcity_txt.x + round((issuer.x / 2) - (pasaporte_txt.x / 2)), 40 + issuer.y), pasaporte_txt.text, "Black", font=pasaporte_txt.font)

    draw.text((310, 132), tipo_txt.text, "#212930", font=tipo_txt.font)
    draw.text((330 + passtype.x, 132), pais_txt.text, "#212930", font=pais_txt.font)
    draw.text((1068 - 20 - userid.x, 132), dcid_txt.text, "#212930", font=dcid_txt.font)

    draw.text((310, 150), passtype.text, "Black", font=passtype.font)
    draw.text((330 + passtype.x, 150), rc_txt.text, "Black", font=rc_txt.font)
    draw.text((1068 - 20 - userid.x, 150), userid.text, "Black", font=userid.font)

    draw.text((310, 214), discord_txt.text, "#212930", font=discord_txt.font)

    draw.text((310, 232), username.text, "Black", font=username.font)
    draw.text((310 + username.x, 232), userdisc.text, "Black", font=userdisc.font)

    draw.text((310, 296), mcname_txt.text, "#212930", font=mcname_txt.font)
    draw.text((330 + mcname.x, 296), edad_txt.text, "#212930", font=edad_txt.font)

    draw.text((310, 314), mcname.text, "Black", font=mcname.font)
    draw.text((330 + mcname.x, 314), age.text, "Black", font=age.font)

    draw.text((310, 378), profesion_txt.text, "#212930", font=profesion_txt.font)

    draw.text((310, 396), profession.text, "Black", font=profession.font)

    draw.text((310, 460), nacimiento_txt.text, "#212930", font=nacimiento_txt.font)
    draw.text((390 + mcname.x, 460), expedicion_txt.text, "#212930", font=expedicion_txt.font)

    draw.text((310, 478), birth.text, "Black", font=birth.font)
    draw.text((390 + mcname.x, 478), issued.text, "Black", font=issued.font)

    draw.text((310, 542), sexo_txt.text, "#212930", font=sexo_txt.font)
    draw.text((390 + gender.x, 542), ciudad_txt.text, "#212930", font=ciudad_txt.font)

    draw.text((310, 560), gender.text, "Black", font=gender.font)
    draw.text((390 + gender.x, 560), city.text, "Black", font=city.font)

    draw.text((44, 760 - code.y - 44), code.text, "#212930", font=code.font)
    draw.text((44, 760 - code.y), code2.text, "#212930", font=code.font)

    await dcuser.avatar.save(fp = "./images/temp_image.webp")
    avatar = Image.open("./images/temp_image.webp")
    avatar = avatar.convert("RGBA")
    avatar = avatar.resize((250, 250))

    canvas.paste(avatar, (40, 132), avatar)

    skin_img = Image.open(get_player_skin(guild, mcnick))
    skin_img = skin_img.crop((8,8,16,16))
    skin_img = skin_img.resize((250, 250), resample=Image.NEAREST)

    canvas.paste(skin_img, (40, 392), skin_img)

    tag = font_str(f"{num}-{uuid[:4]}-{str(dcuser.id)[-4:]}", ImageFont.truetype("./images/LED Dot-Matrix.ttf", 70))
    tag_img = Image.new("RGBA", (tag.x, tag.y), (255,255,255,0))
    tag_draw = ImageDraw.Draw(tag_img)
    tag_draw.text((0,0), tag.text,font=tag.font, fill=(0, 0, 0, 92))
    tag_img = tag_img.rotate(90, expand=1)

    canvas.paste(tag_img, (1088,105), tag_img)
    
    passicon = Image.open("./images/passport_icon.png")
    passicon = passicon.resize((120, 60))
    canvas.paste(passicon, (1200 - 40 - 120,40), passicon)
    
    canvas.save('./passportbg_temp.png')
    return './passportbg_temp.png'

async def rank_banner(member):
    dcuser, guild, mcnick = get_user(member=member)

    user_info = db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]

    cargos = {
        'Ninguno':'rank-1',
        'Ciudadano':'rank-1',
        'Cadete':'rank1',
        'Cabo':'rank2',
        'Sargento':'rank3',
        'Sub teniente':'rank4',
        'Teniente':'rank5',
        'Capitan':'rank6',
        'Comandante':'rank7',
        'Jefe de policia':'rank8',
        'Consejal':'rank8',
        'Alcalde':'rank8',
        'General':'rank9',
        'Sub secretario':'rank10',
        'Secretario':'rank11',
        'Presidente':'rank12'
    }
            
    rank = font_str(user_info['extra']['passport']['cargo'], ImageFont.truetype("./images/Comfortaa-Bold.ttf", 30))
    name = font_str(dcuser.name, ImageFont.truetype("./images/Comfortaa-Regular.ttf", 30))
    nick = font_str((dcuser.nick if dcuser.nick else dcuser.name), ImageFont.truetype("./images/Comfortaa-Bold.ttf", 52))
    disc = font_str(f'#{dcuser.discriminator}', ImageFont.truetype("./images/Comfortaa-Light.ttf", 28))
    smal = lambda x: font_str(x, ImageFont.truetype("./images/Comfortaa-Regular.ttf", 26))

    dc_str = smal('DC:')
    mc_str = smal('MC:')

    lvl = user_info['level']
    mcname = font_str(user_info['extra']['passport']['mc'], ImageFont.truetype("./images/Comfortaa-Bold.ttf", 56))
    xp = user_info['xp']
    nextlvl = user_info['nxtlvl']
    exp = font_str(f'{get_exp(xp)}/{get_exp(nextlvl)} xp', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 32))
    lvl_str = font_str('nivel:', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 32))
    pos_str = font_str('rank:', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 32))
    level = font_str(f"{user_info['level']}", ImageFont.truetype("./images/Comfortaa-Bold.ttf", 96))
    pos_rank = font_str(f"#{user_info['ranking']}", ImageFont.truetype("./images/Comfortaa-Bold.ttf", 96))

    await dcuser.avatar.save(fp = "./images/temp_image.webp")
    template = Image.open("./images/gltemplatebg_old.png")
    mask = Image.open("./images/cicularmask_old.png").convert('L')
    pfp = Image.open("./images/temp_image.webp").convert("RGBA")
    symbol = Image.open(f"./images/{cargos.get(user_info['extra']['passport']['cargo'], 'rank-1')}.png")
    finalpfp = ImageOps.fit(pfp, (mask.size), centering=(0.5, 0.5))
    finalpfp.putalpha(mask)
    urs_color = ImageColor.getrgb(str(dcuser.color))
    decal = Image.new('RGBA', (1050, 330), urs_color)
    decalmask = Image.open("./images/templatedecalmask_old.png").convert('L')
    decal.putalpha(decalmask)
    bar = int((534 / nextlvl) * xp)
    xp_bar_placeholder = Image.new('RGBA', (534, 49), (45, 56, 50))
    xp_bar_full = Image.new('RGBA', (bar, 49), urs_color)
    xp_bar_full = ImageChops.invert(xp_bar_full)
    xp_bar_placeholder.paste(xp_bar_full, (0,0))
    xp_bar_mask = Image.open("./images/xpbar_old.png").convert('L')
    xp_bar_placeholder.putalpha(xp_bar_mask)

    template = Image.alpha_composite(template, decal)
    template.paste(finalpfp, (15,15), finalpfp)
    template.paste(symbol, (850,0), symbol)
    template.paste(xp_bar_placeholder, (315,266), xp_bar_placeholder)
    draw = ImageDraw.Draw(template)

    white = (255,255,255)
    gray = (170, 170, 170)

    mid = lambda text1, text2: (text1.y/2) - (text2.y/2)
    xpos = lambda text, vert: int(sqrt(abs((177 ** 2) - ((175 - (vert + (text.y * 2))) ** 2))))

    vertical = 15
    horizontal = 165 + xpos(rank, vertical)
    draw.text((horizontal, vertical), rank.text, urs_color, font=rank.font)
    horizontal += rank.x + 10
    draw.text((horizontal, vertical), name.text, gray, font=name.font)
    horizontal += name.x + 2
    draw.text((horizontal, vertical), disc.text, gray, font=disc.font)
    vertical += rank.y + 6
    horizontal = 165 + xpos(dc_str, vertical)
    draw.text((horizontal, vertical + mid(nick, dc_str)), dc_str.text, gray, font=dc_str.font)
    horizontal += dc_str.x + 5
    draw.text((horizontal, vertical), nick.text, white, font=nick.font)
    vertical += nick.y + 6
    horizontal = 165 + xpos(mc_str, vertical)
    draw.text((horizontal, vertical + mid(mcname, mc_str)), mc_str.text, gray, font=mc_str.font)
    horizontal += mc_str.x + 5
    draw.text((horizontal, vertical), mcname.text, white, font=mcname.font)
    vertical += mcname.y + 6
    horizontal = 165 + xpos(lvl_str, vertical)
    draw.text((horizontal, vertical + mid(level, lvl_str)), lvl_str.text, gray, font=lvl_str.font)
    horizontal += lvl_str.x + 6
    draw.text((horizontal, vertical), level.text, white, font=level.font)
    horizontal += level.x + 6
    draw.text((horizontal, vertical + mid(pos_rank, pos_str)), pos_str.text, gray, font=pos_str.font)
    horizontal += pos_str.x + 6
    draw.text((horizontal, vertical), pos_rank.text, white, font=pos_rank.font)
    horizontal = 582 - (exp.x / 2)
    vertical = 290.5 - (exp.y /2)
    draw.text((horizontal, vertical), exp.text, white, font=exp.font)

    template.save('./images/temp_image.png')
    return './images/temp_image.png'


class Continue_Button(Button):

    def __init__(self):
        super().__init__(label="Continuar", style=discord.ButtonStyle.green)
        self.spent = False

    async def callback(self, interaction):
        if self.spent:
            await interaction.response.defer()
            return
        self.spent = True

        code = "CPTL"
        for city in db['bots'][str(interaction.guild.id)]['extra']['cities']:
            if db['bots'][str(interaction.guild.id)]['extra']['cities'][city] == self.view.children[1].values[0]:
                code = city
        
        sex = {
            "Hombre":"H",
            "Mujer":"M",
            "Ninguno":"N"
        }
        sex = sex.get(self.view.children[0].values[0], "Ninguno")

        await interaction.response.send_modal(Prompt(code, sex, self.view.message))

class City_select(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="La Capital", description="no se k poner akhi"),
            discord.SelectOption(label="Seatle", description="no se k poner akhi"),
            discord.SelectOption(label="San Fierro", description="no se k poner akhi"),
            discord.SelectOption(label="Metropolis", description="no se k poner akhi")
        ]
        super().__init__( 
            placeholder = "Elige tu ciudad de procedencia", 
            min_values = 1,
            max_values = 1,
            options = options
        )
    async def callback(self, interaction):

        code = "CPTL"
        for city in db['bots'][str(interaction.guild.id)]['extra']['cities']:
            if db['bots'][str(interaction.guild.id)]['extra']['cities'][city] == self.values[0]:
                code = city

        embed = embed_builder(**{
            "title":db['bots'][str(interaction.guild.id)]['extra']['cities'][code],
            "description":db['bots'][str(interaction.guild.id)]['extra']['citydes'][code],
            "color":color("orange"),
            "img":db['bots'][str(interaction.guild.id)]['extra']['cityimg'][code],
            "footer":"Selecciona una ciudad para empezar"
        })
        await self.view.message.edit("", embed=embed)
        await interaction.response.defer()

class Registro(View):
    def __init__(self):
        super().__init__()
        self.add_item(City_select())
        self.add_item(Continue_Button())
    
    @select(placeholder = "Con que te identificas mas", min_values = 1, max_values = 1, options = [discord.SelectOption(label="Hombre", description="Elige la opcion con la que te identifiques mas"),discord.SelectOption(label="Mujer", description="Elige la opcion con la que te identifiques mas")])
    async def select_callback(self, select, interaction):
        await interaction.response.defer()

class Prompt(Modal):
    def __init__(self, city, sex, msg):
        super().__init__(title="Registrate para poder entrar :D")
        self.city=city
        self.sex=sex
        self.msg=msg

        self.add_item(InputText(label="Fecha de nacimiento", value="30/01/2023"))

        self.add_item(InputText(label="Nombre de minecraft", placeholder="Nombre"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="fecha", value=self.children[0].value)
        embed.add_field(name="nombre", value=self.children[1].value)
        await interaction.response.defer()

        if '/' in self.children[0].value:
            date = self.children[0].value.split('/')
            try:
                date = list(map(int, date))
                date.reverse()
            except:
                await interaction.response.send_message("Fecha invalida, intenta de nuevo", ephemeral=True)
                return
        else:
            await interaction.response.send_message("Fecha invalida, intenta de nuevo", ephemeral=True)
            return
        
        num = str(db['bots'][str(interaction.guild.id)]['memberbase'][str(interaction.user.id)]["number"])
        num = num.split()

        while len(num) < 3:
            num.insert(0, '0')
        num = ''.join(num)

        passport = {
                "birth": date,
                "code": [f"RG<<RC<{self.city}<<<DESMPL<<<<{interaction.user.id}<",f"<<{'<'.join(construct_offline_player_uuid(self.children[1].value).split('-'))}<<{num}"],
                "gender": self.sex,
                "issued": [datetime.now().year,datetime.now().month,datetime.now().day],
                "issuer": self.city,
                "cargo": "Ciudadano",
                "mc": self.children[1].value,
                "profession": [
                    "DESMPL"
                ],
                "type": "RG"
            }
        
        db['bots'][str(interaction.guild.id)]['extra']['players'][self.children[1].value] = interaction.user.id
        db['bots'][str(interaction.guild.id)]['memberbase'][str(interaction.user.id)]['extra']['passport'] = passport
        db.save()

        passport = discord.File(await render_passport(member=interaction.user), filename="passport.png")

        embed = embed_builder(**{
            "title":f"Felicidades {interaction.user.nick if interaction.user.nick else interaction.user.name}!",
            "description":"Ya eres ciudadadano de RolCity :D",
            "color":color("green"),
            'img':"attachment://passport.png",
            "footer":"Este es tu pasaporte"
        })

        view = View()
        await self.msg.edit("", file=passport, embed=embed, view=view)

class Register_button(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Registrate :D", style=discord.ButtonStyle.green, custom_id="3621-registerbutton-0")
    async def regs(self, button: discord.Button, interaction: discord.Interaction):
        if "passport" in db['bots'][str(interaction.guild.id)]['memberbase'][str(interaction.user.id)]['extra']:
            await interaction.response.send_message("Ya estas registrado ;)", ephemeral=True)
        else:
            embed = embed_builder(**{
                "title":"**Registro**",
                "description":"Para poder entrar al servidor deberar registrarte primero, una vez registrado obtendras tu pasaporte, acceso al servidor y a diversas funciones como el chat de voz de proximidad",
                "color":color("orange"),
                "img":"https://media.discordapp.net/attachments/1068739926503465000/1070387198949605548/ere.png",
                "footer":"El registro solo funciona cuando el servidor esta encendido"
            })
            await interaction.response.send_message("x3", embed=embed, view=Registro(), ephemeral=True)



class RolCity(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[RolCity]'
        self.bot.log.info(f'starting {self.__name__}...')
    
    async def ban(self, tiempo, razon, ctx=None, member=None, mcname=None, guild_id=None, issuer=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=self.bot.get_guild(guild_id) if guild_id else None)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        if not "ban_channel" in db['bots'][str(guild.id)]['chs']:
            return
        
        author =  self.bot.user.name
        author_img = self.bot.user.avatar.url
        if ctx:
            if get_user_auth(get_author(ctx)) <= get_user_auth(dcuser) - 1:
                await wreply(ctx, "No tienes el rango suficiente")
                return

            if 'interaction' in vars(ctx):
                author = ctx.user.nick if ctx.user.nick else ctx.user.name
                author_img = ctx.user.avatar.url
            elif 'prefix' in vars(ctx):
                author = ctx.author.nick if ctx.author.nick else ctx.author.name
                author_img = ctx.author.avatar.url
        elif issuer:
            issuer_user, issuer_gld, issuer_mc = get_user(mcname=issuer, guild=self.bot.get_guild(guild_id))
            if issuer_user:
                author = issuer_user.nick if issuer_user.nick else issuer_user.name
                author_img = issuer_user.avatar.url
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        if 'bans' not in record:
            record['bans'] = []
        
        if record['counter']['bans'] < 2:
            wlbl = ['primer', 'segundo']
            ban_num = wlbl[len(record['bans'])]
            record['counter']['bans'] += 1
        elif record['counter']['bans'] >= 2:
            ban_num = 'tercer'
            record['counter']['bans'] = record['counter']['bans'] - 2
        
        record['bans'].append(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}:{tiempo}:{razon}')

        db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'] = str(b64encode(bytes(json.dumps(record), 'utf8')), 'utf8')
        db.save()
        
        footers = {
            'primer':'Este es tu primer ban, si acumulas 3 baneos seras baneado permanentemente.',
            'segundo':'Este es tu segundo ban, si acumulas un ban mas seras baneado permanentemente.',
            'tercer':'Este es tu tercer ban, seras baneado permanentemente por acumular 3 ban.'
        }

        embed = embed_builder(**{
            "title":"**BAN**",
            "description":f"{dcuser.mention} Ha recibido su {ban_num} ban.",
            "fields":[
                {'name':'Razon', 'value':razon, 'inline':False},
                {'name':'Tiempo', 'value':f"{tiempo} horas", 'inline':False}
            ],
            "color":color("red"),
            "author":author,
            "author_img":author_img,
            "thumb":"https://media.discordapp.net/attachments/1068739926503465000/1068854653535653888/CPD_logo.png?width=434&height=453",
            "footer":footers[ban_num]
        })

        await self.bot.get_channel(db['bots'][str(guild.id)]['chs']["ban_channel"]).send(embed=embed)
    
    async def strike(self, razon, ctx=None, member=None, mcname=None, guild_id=None, issuer=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=self.bot.get_guild(guild_id) if guild_id else None)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        if not "ban_channel" in db['bots'][str(guild.id)]['chs']:
            return
        
        author =  self.bot.user.name
        author_img = self.bot.user.avatar.url
        if ctx:
            if get_user_auth(get_author(ctx)) <= get_user_auth(dcuser) - 1:
                await wreply(ctx, "No tienes el rango suficiente")
                return

            if 'interaction' in vars(ctx):
                author = ctx.user.nick if ctx.user.nick else ctx.user.name
                author_img = ctx.user.avatar.url
            elif 'prefix' in vars(ctx):
                author = ctx.author.nick if ctx.author.nick else ctx.author.name
                author_img = ctx.author.avatar.url
        elif issuer:
            issuer_user, issuer_gld, issuer_mc = get_user(mcname=issuer, guild=self.bot.get_guild(guild_id))
            if issuer_user:
                author = issuer_user.nick if issuer_user.nick else issuer_user.name
                author_img = issuer_user.avatar.url
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        if 'strikes' not in record:
            record['strikes'] = []
        
        if record['counter']['strikes'] < 2:
            wlbl = ['primer', 'segundo']
            strike_num = wlbl[len(record['strikes'])]
            record['counter']['strikes'] += 1
        elif record['counter']['strikes'] >= 2:
            strike_num = 'tercer'
            record['counter']['strikes'] = record['counter']['strikes'] - 2
            asyncio.run_coroutine_threadsafe(self.ban(db['bots'][str(guild.id)]['extra']['defultbantime'], "Acumular 3 strikes", ctx=ctx, member=member, mcname=mcname, guild_id=guild_id, issuer=issuer), self.bot.loop)
        
        record['strikes'].append(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}:{razon}')

        db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'] = str(b64encode(bytes(json.dumps(record), 'utf8')), 'utf8')
        db.save()
        
        footers = {
            'primer':'Este es tu primer strike, si acumulas 3 strikes seras baneado.',
            'segundo':'Este es tu segundo strike, si acumulas un strike mas seras baneado.',
            'tercer':'Este es tu tercer strike, seras baneado por acumular 3 strikes.'
        }

        embed = embed_builder(**{
            "title":"**STRIKE**",
            "description":f"{dcuser.mention} Ha recibido su {strike_num} strike.",
            "fields":[
                {'name':'Razon', 'value':razon, 'inline':False}
            ],
            "color":color("orange"),
            "author":author,
            "author_img":author_img,
            "thumb":"https://media.discordapp.net/attachments/1068739926503465000/1068854653535653888/CPD_logo.png?width=434&height=453",
            "footer":footers[strike_num]
        })

        await self.bot.get_channel(db['bots'][str(guild.id)]['chs']["ban_channel"]).send(embed=embed)


    async def multa(self, cantidad, razon, ctx=None, member=None, mcname=None, guild_id=None, issuer=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=self.bot.get_guild(guild_id) if guild_id else None)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        if not "ban_channel" in db['bots'][str(guild.id)]['chs']:
            return
        
        author =  self.bot.user.name
        author_img = self.bot.user.avatar.url
        if ctx:
            if get_user_auth(get_author(ctx)) <= get_user_auth(dcuser) - 1:
                await wreply(ctx, "No tienes el rango suficiente")
                return

            if 'interaction' in vars(ctx):
                author = ctx.user.nick if ctx.user.nick else ctx.user.name
                author_img = ctx.user.avatar.url
            elif 'prefix' in vars(ctx):
                author = ctx.author.nick if ctx.author.nick else ctx.author.name
                author_img = ctx.author.avatar.url
        elif issuer:
            issuer_user, issuer_gld, issuer_mc = get_user(mcname=issuer, guild=self.bot.get_guild(guild_id))
            if issuer_user:
                author = issuer_user.nick if issuer_user.nick else issuer_user.name
                author_img = issuer_user.avatar.url
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        if 'tickets' not in record:
            record['tickets'] = []

        record['tickets'].append(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}:${cantidad}:{razon}')

        db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'] = str(b64encode(bytes(json.dumps(record), 'utf8')), 'utf8')
        db.save()

        embed = embed_builder(**{
            "title":"**MULTA**",
            "description":f"{dcuser.mention} Ha recibido una multa.",
            "fields":[
                {'name':'Multa', 'value':cantidad, 'inline':False},
                {'name':'Razon', 'value':razon, 'inline':False}
            ],
            "color":color("blue"),
            "author":author,
            "author_img":author_img,
            "thumb":"https://media.discordapp.net/attachments/1068739926503465000/1068854653535653888/CPD_logo.png?width=434&height=453",
            "footer":"Podras pagar la multa en..."
        })

        await self.bot.get_channel(db['bots'][str(guild.id)]['chs']["ban_channel"]).send(embed=embed)

    async def warn(self, razon, ctx=None, member=None, mcname=None, guild_id=None, issuer=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=self.bot.get_guild(guild_id) if guild_id else None)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        if not "ban_channel" in db['bots'][str(guild.id)]['chs']:
            return
        
        author =  self.bot.user.name
        author_img = self.bot.user.avatar.url
        if ctx:
            if get_user_auth(get_author(ctx)) < get_user_auth(dcuser) - 1:
                await wreply(ctx, "No tienes el rango suficiente")
                return

            if 'interaction' in vars(ctx):
                author = ctx.user.nick if ctx.user.nick else ctx.user.name
                author_img = ctx.user.avatar.url
            elif 'prefix' in vars(ctx):
                author = ctx.author.nick if ctx.author.nick else ctx.author.name
                author_img = ctx.author.avatar.url
        elif issuer:
            issuer_user, issuer_gld, issuer_mc = get_user(mcname=issuer, guild=self.bot.get_guild(guild_id))
            if issuer_user:
                author = issuer_user.nick if issuer_user.nick else issuer_user.name
                author_img = issuer_user.avatar.url
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        if 'warnings' not in record:
            record['warnings'] = []
        
        if record['counter']['warnings'] < 4:
            wlbl = ['primera', 'segunda', 'tercera', 'cuarta']
            warn_num = wlbl[len(record['warnings'])]
            record['counter']['warnings'] += 1
        elif record['counter']['warnings'] >= 4:
            warn_num = 'quinta'
            record['counter']['warnings'] = record['counter']['warnings'] - 4
            asyncio.run_coroutine_threadsafe(self.multa(db['bots'][str(guild.id)]['extra']['defaultticket'], "Acumular 5 advertencias", ctx=ctx, member=member, mcname=mcname, guild_id=guild_id, issuer=issuer), self.bot.loop)
        
        record['warnings'].append(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}:{razon}')

        db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'] = str(b64encode(bytes(json.dumps(record), 'utf8')), 'utf8')
        db.save()
        
        footers = {
            'primera':'Esta es tu primer advertencia, si acumulas 5 advertencias reciviras una multa.',
            'segunda':'Esta es tu segunda advertencia, si acumulas 5 advertencias reciviras una multa.',
            'tercera':'Esta es tu tercera advertencia, si acumulas 5 advertencias reciviras una multa.',
            'cuarta':'Esta es tu cuarta advertencia, si acumulas 5 advertencias reciviras una multa.',
            'quinta':'Esta es tu quinta advertencia, recibiras una multa por desacato a la justicia.'
        }

        embed = embed_builder(**{
            "title":"**ADVERTENCIA**",
            "description":f"{dcuser.mention} Ha recibido su {warn_num} advertencia.",
            "fields":[
                {'name':'Razon', 'value':razon, 'inline':False}
            ],
            "color":color("teal"),
            "author":author,
            "author_img":author_img,
            "thumb":"https://media.discordapp.net/attachments/1068739926503465000/1068854653535653888/CPD_logo.png?width=434&height=453",
            "footer":footers[warn_num]
        })

        await self.bot.get_channel(db['bots'][str(guild.id)]['chs']["ban_channel"]).send(embed=embed)


    async def usr_info(self, ctx, member=None, mcname=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=ctx.guild)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        txtequal = {'strikes':'strikes','bans':'bans','warnings':'advertencias','tickets':'multas'}

        active_txt = ', '.join([f"{record['counter'][k]} {txtequal[k]} {'activas' if k == 'warnings' else 'activos'}" if record['counter'][k] > 0 else '' for k in record['counter']])

        recieved_txt = ', '.join([f"{len(record[k])} {txtequal[k]}" if k != 'counter' else '' for k in record])
        
        record_txt = f"El ciudadano {' tiene: ' + active_txt if ''.join(active_txt.split(', ')) != '' else 'no tiene eventos activos'}\nEl ciudadano {'ha recibido' + recieved_txt if recieved_txt != '' else 'no ha recibido sanciones'}"
        
        files = None
        if 'passport' in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            passport = discord.File(await render_passport(member=dcuser), filename="passport.png")
            rankbanner = discord.File(await rank_banner(dcuser), filename="rankbanner.png")
            files = [rankbanner, passport]

        pssinfo = db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport'] if 'passport' in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra'] else None

        getprofession = lambda x: db['bots'][str(guild.id)]['extra']['professions'].get(x, "DESMPL")

        embed = embed_builder(**{
            "title":"**Informacion del ciudadano**",
            "description":f"{dcuser.mention}",
            "fields":[
                {'name':'Discord', 'value':dcuser.name, 'inline':False},
                {'name':'Minecraft', 'value':mcnick if mcnick else "no registrado", 'inline':False},
                {'name':'Profesiones', 'value':'\n'.join(map(getprofession, pssinfo['profession'])) if pssinfo else "no registrado", 'inline':False},
                {'name':'Historial', 'value':record_txt, 'inline':False},
            ],
            "color":dcuser.color,
            "thumb":dcuser.avatar.url,
            'img':"attachment://rankbanner.png",
            "footer":f"Ciudadano #{db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['number']} {dcuser.nick if dcuser.nick else dcuser.name} {'registrado el ' + str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issued'][2]) + '/' + str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issued'][1]) + '/' + str(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['passport']['issued'][0]) if 'passport' in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra'] else 'no registrado'}"
        })

        await wreply(ctx, files=files, embed=embed)

    async def usr_record(self, ctx, member=None, mcname=None):
        dcuser, guild, mcnick = get_user(ctx=None, member=member, mcname=mcname, guild=ctx.guild)
        if not dcuser:
            if ctx:
                await wreply(ctx, "No se encontro el usuario")
            return None
        
        if 'record' not in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            record = {}
        else:
            record = json.loads(b64decode(bytes(db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']['record'], 'utf8')))
        
        if 'counter' not in record:
            record['counter'] = {'strikes':0, 'bans':0, 'warnings':0, 'tickets':0}

        file = None
        if 'passport' in db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['extra']:
            rankbanner = discord.File(await rank_banner(dcuser), filename="rankbanner.png")
            file = rankbanner

        embed = embed_builder(**{
            "title":"**Historial del ciudadano**",
            "description":f"{dcuser.mention}",
            "fields":[
                {'name':f"Advertencias ({len(record['warnings'])if 'warnings' in record else 0})", 'value':'\n'.join(record['warnings']) if 'warnings' in record else 'Ninguna', 'inline':False},
                {'name':f"Multas ({len(record['tickets']) if 'tickets' in record else 0})", 'value':'\n'.join(record['tickets']) if 'tickets' in record else 'Ninguna', 'inline':False},
                {'name':f"Strikes ({len(record['strikes']) if 'strikes' in record else 0})", 'value':'\n'.join(record['strikes']) if 'strikes' in record else 'Ninguno', 'inline':False},
                {'name':f"Baneos ({len(record['bans']) if 'bans' in record else 0})", 'value':'\n'.join(record['bans']) if 'bans' in record else 'Ninguno', 'inline':False},
            ],
            "color":dcuser.color,
            'img':"attachment://rankbanner.png",
            "footer":f"Ciudadano #{db['bots'][str(guild.id)]['memberbase'][str(dcuser.id)]['number']} {dcuser.nick if dcuser.nick else dcuser.name} {mcname}"
        })

        await wreply(ctx, file=file, embed=embed)



    @slash_command(name='ban', description='Banea a un jugador')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def app_ban(self, ctx, mention, tiempo, razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.ban(tiempo, razon, ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido baneado {tiempo} por {razon}')
    @command(name='ban')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def cmd_ban(self, ctx, mention, tiempo, *razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.ban(tiempo, ' '.join(map(str, razon)), ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido baneado {tiempo} por {" ".join(map(str, razon))}')

    @slash_command(name='strike', description='Da un strike a un jugador')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def app_strk(self, ctx, mention, razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.strike(razon, ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha recibido un strike por {razon}')
    @command(name='strike')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def cmd_strk(self, ctx, mention, *razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.strike(' '.join(map(str, razon)), ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha recibido un strike por {" ".join(map(str, razon))}')

    @slash_command(name='multa', description='Multa a un jugador')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def app_mult(self, ctx, mention, cantidad, razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.multa(cantidad, razon, ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido multado {cantidad} por {razon}')
    @command(name='multa')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def cmd_mult(self, ctx, mention, cantidad, *razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.multa(cantidad, ' '.join(map(str, razon)), ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido multado {cantidad} por {" ".join(map(str, razon))}')

    @slash_command(name='warn', description='Da una davertencia a un jugador')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def app_warn(self, ctx, mention, razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.warn(razon, ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido advertido: {razon}')
    @command(name='warn')
    @on_guild(1068420065692766308)
    @user_auth(4)
    async def app_warn(self, ctx, mention, *razon):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.warn(' '.join(map(str, razon)), ctx=ctx, member=user, mcname=mcname, guild_id=ctx.guild.id)
        await wreply(ctx, f'{user.mention if user else mcname} Ha sido advertido: {" ".join(map(str, razon))}')

    @slash_command(name='info', description='Mira la informacion de un ciudadano')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def app_info(self, ctx, mention):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.usr_info(ctx, member=user, mcname=mcname)
    @command(name='info')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def cmd_info(self, ctx, mention):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.usr_info(ctx, member=user, mcname=mcname)

    @slash_command(name='record', description='Mira el historial de un ciudadano')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def app_record(self, ctx, mention):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention

        await self.usr_record(ctx, member=user, mcname=mcname)
    @command(name='record')
    @on_guild(1068420065692766308)
    @user_auth(1)
    async def cmd_record(self, ctx, mention):
        user = None
        mcname = None
        if '<@' in str(mention):
            user = get_mention(ctx.guild, str(mention))
        else:
            mcname = mention
        
        await self.usr_record(ctx, member=user, mcname=mcname)

    @slash_command(name='passport', description='Mira tu pasaporte o el de otros ciudadanos')
    @on_guild(1068420065692766308)
    async def app_passport(self, ctx, mention=None):
        user = None
        mcname = None
        eph = False if get_user_auth(ctx.user) > 0 else True
        if mention:
            if eph:
                await wreply(ctx, 'No puedes ver los pasaportes de otros ciudadanos')
                return

            eph = False
            if '<@' in str(mention):
                user = get_mention(ctx.guild, str(mention))
            else:
                mcname = mention

        passport = discord.File(await render_passport(ctx, member=user, mcname=mcname))
        if passport:
            await wreply(ctx, file=passport)
        else:
            await wreply(ctx, 'no esta registrado')
    @command(name='passport')
    @on_guild(1068420065692766308)
    async def cmd_passport(self, ctx, mention=None):
        user = None
        mcname = None
        eph = False if get_user_auth(ctx.author) > 0 else True
        if mention:
            if eph:
                await wreply(ctx, 'No puedes ver los pasaportes de otros ciudadanos')
                return

            eph = False
            if '<@' in str(mention):
                user = get_mention(ctx.guild, str(mention))
            else:
                mcname = mention

        passport = discord.File(await render_passport(ctx, member=user, mcname=mcname))
        if passport:
            await wreply(ctx, file=passport)
        else:
            await wreply(ctx, 'no esta registrado')

    @slash_command()
    @on_guild(1068420065692766308)
    @user_auth(7)
    async def registrer(self, ctx):

        embed = embed_builder(**{
            "title":"**Registro**",
            "description":"Para poder entrar al servidor deberas registrarte primero, una vez registrado obtendras tu pasaporte, acceso al servidor y a diversas funciones",
            "color":color("orange"),
            "img":"https://media.discordapp.net/attachments/1068739926503465000/1070387198949605548/ere.png",
            "footer":"El registro solo funciona cuando el servidor esta encendido"
        })

        view = Register_button()
        await ctx.respond("", embed=embed, view=view)
    
    @slash_command(name='ip', description='Mira tu pasaporte o el de otros ciudadanos')
    @on_guild(1068420065692766308)
    async def app_ip(self, ctx):
        await wreply("La ip es <ip>")
    @command(name='ip')
    @on_guild(1068420065692766308)
    async def cmd_ip(self, ctx):
        await wreply("La ip es <ip>")

    @Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Register_button())
        self.regs_view = Register_button()
        self.bot.log.info(f'{self.__name__}: started!')

#   ROLCITY
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒


#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#*   Dynamite

class Dynamite(Cog, guild_ids=[1094736534076412036]):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[Dynamite]'
        self.bot.log.info(f'starting {self.__name__}...')

    async def redes(self, ctx):
        emb = embed_builder(**{
            "title":"Sigueme en mis redes :D",
            "color":color("teal")
        })
        await ctx.reply(embed=emb)
        emb = embed_builder(**{
            "author":"Twitch",
            "author_img":"https://media.discordapp.net/attachments/1095222311231168542/1096327850048630844/tvtv.png?width=453&height=453",
            "title":"APKxDynamite en Twitch",
            "thumb":"https://images-ext-2.discordapp.net/external/Tqq5ILk87Ib8HzUhaEy21i3wfUWI7ScfALuGy8eYSyY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/393144304027041804/69e83cfde8fd7b69190d4ad97bef1aa1.png",
            "url":"https://www.twitch.tv/apkxdynamite",
            "color":color("#9146ff")
        })
        await ctx.send(embed=emb)
        emb = embed_builder(**{
            "author":"YouTube",
            "author_img":"https://media.discordapp.net/attachments/1095222311231168542/1096327849813737532/ytyt.png?width=453&height=453",
            "title":"APKxDynamite en Youtube",
            "thumb":"https://images-ext-2.discordapp.net/external/Tqq5ILk87Ib8HzUhaEy21i3wfUWI7ScfALuGy8eYSyY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/393144304027041804/69e83cfde8fd7b69190d4ad97bef1aa1.png",
            "url":"https://www.youtube.com/@APKxDynamite",
            "color":color("#c3352e")
        })
        await ctx.send(embed=emb)
        emb = embed_builder(**{
            "author":"TikTok",
            "author_img":"https://media.discordapp.net/attachments/1095222311231168542/1096327849608232980/tktk.png?width=453&height=453",
            "title":"apkxdynamite en Tiktok",
            "thumb":"https://images-ext-2.discordapp.net/external/Tqq5ILk87Ib8HzUhaEy21i3wfUWI7ScfALuGy8eYSyY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/393144304027041804/69e83cfde8fd7b69190d4ad97bef1aa1.png",
            "url":"https://www.tiktok.com/@apkxdynamite",
            "color":color("#ffffff")
        })
        await ctx.send(embed=emb)
        emb = embed_builder(**{
            "author":"Instagram",
            "author_img":"https://media.discordapp.net/attachments/1095222311231168542/1096327849360764969/2048px-Instagram_logo_2016.png?width=453&height=453",
            "title":"apkxdynamite en Instagram",
            "thumb":"https://images-ext-2.discordapp.net/external/Tqq5ILk87Ib8HzUhaEy21i3wfUWI7ScfALuGy8eYSyY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/393144304027041804/69e83cfde8fd7b69190d4ad97bef1aa1.png",
            "url":"https://www.instagram.com/apkxdynamite",
            "color":color("#d62976")
        })
        await ctx.send(embed=emb)
        
    @slash_command(name='redes', description='sigueme en mis redes :D')
    #@on_guild(1094736534076412036)
    async def app_redes(self, ctx):
        await self.redes(ctx)
    @command(name='redes')
    @on_guild(1094736534076412036)
    async def cmd_redes(self, ctx, mention=None):
        await self.redes(ctx)
    
    @Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Register_button())
        self.regs_view = Register_button()
        self.bot.log.info(f'{self.__name__}: started!')

#   Dynamite
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

"""
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#*   E621

esix_api = E621()

with codecs.open("parameters.txt", 'r', 'utf-8') as file:
    _parameters = file.read()

class WoxE621(Cog, guild_ids=[997679468996993105]):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[WoxE621]'
        self.bot.log.info(f'starting {self.__name__}...')

    async def e6setwl(self, ctx, *parameters):
        global _parameters

        _parameters = ' '.join(parameters)

        with codecs.open("parameters.txt", 'w', 'utf-8') as file:
            file.write(_parameters)
            
        await wreply(ctx, "***Whitelist cambiada a:***\n ```\n" + "\n".join(_parameters.split(' ')) + "```")

    async def e6wl(self, ctx):
        await wreply(ctx, "***Whitelist actual:***\n ```\n" + "\n".join(_parameters.split(' ')) + "```")

    async def esix(self, ctx, *query):
        
        query = list(query)
        num_of_posts = abs(int(query.pop())) if query[-1].isdigit() else 1
        if num_of_posts > 20:
            num_of_posts = 20
        
        posts = []
        for i in range(round((num_of_posts/2) + 0.1)):
            posts += esix_api.posts.search(' '.join(query) + ' ' + _parameters, page=i+1)

        if len(posts) <= 0: 
            await wreply(ctx, 'Escribiste algun tag mal ;)')
        
        if len(posts) < num_of_posts:
            num_of_posts = round(2 * (len(posts) / 3))
    
        for i in range(num_of_posts):
            
            post = posts[randint(0, len(posts)) - 1]

            if post.file.url: extension = post.file.url[-3:] 
            else: raise Exception("got a null url")

            if extension in ['png', 'jpg', 'jpeg', 'webp']:
                emb = embed_builder(**{
                    "title":f"Post {post.id}",
                    "description":post.description,
                    "img":post.file.url,
                    "url":f"https://e621.net/posts/{post.id}",
                    "color":color("#9146ff"),
                    "footer":', '.join(post.tags.artist)
                })
                await wreply(ctx, embed=emb)
            else:
                await wreply(ctx, f"**Post {post.id}**\nBy *{', '.join(post.tags.artist)}*\n*https://e621.net/posts/{post.id}*")

        
    @slash_command(name='e6setwl', description='cambia la whitelist de e621')
    @on_guild(997679468996993105)
    @user_auth(5)
    @is_nsfw()
    async def app_e6setwl(self, ctx, parameters):
        parameters = parameters.split(' ')
        await self.e6setwl(ctx, *parameters)
    @command(name='e6setwl')
    @on_guild(997679468996993105)
    @user_auth(5)
    @is_nsfw()
    async def cmd_e6setwl(self, ctx, *parameters):
        await self.e6setwl(ctx, *parameters)
    
    @slash_command(name='e6wl', description='muestra la whitelist de e621')
    @on_guild(997679468996993105)
    @is_nsfw()
    async def app_e6wl(self, ctx):
        await self.e6wl(ctx)
    @command(name='e6wl')
    @on_guild(997679468996993105)
    @is_nsfw()
    async def cmd_e6wl(self, ctx):
        await self.e6wl(ctx)
    
    @slash_command(name='esix', description='busca posts en e621')
    @on_guild(997679468996993105)
    @is_nsfw()
    async def app_esix(self, ctx, query):
        query = query.split(' ')
        await self.esix(ctx, *query)
    @command(name='esix')
    @on_guild(997679468996993105)
    @is_nsfw()
    async def cmd_esix(self, ctx, *query):
        await self.esix(ctx, *query)
    
    @Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Register_button())
        self.regs_view = Register_button()
        self.bot.log.info(f'{self.__name__}: started!')

#   E621
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
"""


doc_log.info('ready')
