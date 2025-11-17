#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord
from wox_sdb import db
from Chia import wreply, get_mention
from discord.ext.commands import *
from discord import Embed, Colour
from Gaia import *
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops, ImageColor
from math import sqrt
from functools import lru_cache as cache
from colorama import Fore
from random import randint
from time import time

hat_log = Wox_log('Hati', color=Fore.LIGHTGREEN_EX)
hat_log.info('loading...')

@cache
def color(color_like, default='dark_grey'):
    colors = {
        'blue':Colour.blue(),
        'blurple':Colour.blurple(),
        'dark_blue':Colour.dark_blue(),
        'dark_gold':Colour.dark_gold(),
        'dark_gray':Colour.dark_gray(),
        'dark_green':Colour.dark_green(),
        'dark_grey':Colour.dark_grey(),
        'dark_magenta':Colour.dark_magenta(),
        'dark_orange':Colour.dark_orange(),
        'dark_purple':Colour.dark_purple(),
        'dark_red':Colour.dark_red(),
        'dark_teal':Colour.dark_teal(),
        'dark_theme':Colour.dark_theme(),
        'darker_gray':Colour.darker_gray(),
        'darker_grey':Colour.darker_grey(),
        'default':Colour.default(),
        'gold':Colour.gold(),
        'green':Colour.green(),
        'greyple':Colour.greyple(),
        'light_gray':Colour.light_gray(),
        'light_grey':Colour.light_grey(),
        'lighter_gray':Colour.lighter_gray(),
        'lighter_grey':Colour.lighter_grey(),
        'magenta':Colour.magenta(),
        'orange':Colour.orange(),
        'purple':Colour.purple(),
        'random':Colour.random(),
        'red':Colour.red(),
        'teal':Colour.teal()
    }

    if color_like.startswith('#'):
        return discord.Color(value=int(color_like[1:], 16))
    elif type(color_like) in (list, tuple):
        return discord.Color.from_rgb(*color_like)
    else:
        return colors.get(color_like, default)


@cache
def get_exp(xp:int)->str:
    if xp > 1000000:
        res = f'{round(xp/1000000, 3)}m'
    elif xp > 1000:
        res = f'{round(xp/1000, 1)}K'
    else:
        res = str(xp)
    return res

def update_ranking(guild_id, rerank=True):
    hat_log.info('Updating ranking...')

    if rerank:
        rank_func = lambda x: (db['bots'][str(guild_id)]['memberbase'][x]["level"], db['bots'][str(guild_id)]['memberbase'][x]["xp"], db['bots'][str(guild_id)]['memberbase'][x]["number"])
        db['bots'][str(guild_id)]['extra']['ranking'] = sorted(db['bots'][str(guild_id)]['memberbase'], key=rank_func)
        db['bots'][str(guild_id)]['extra']['ranking'].reverse()

    for position, member in enumerate(db['bots'][str(guild_id)]['extra']['ranking']):
        db['bots'][str(guild_id)]['memberbase'][member].update({"ranking":position + 1})
    
    db.save()

    hat_log.info('Rank updated')

async def add_xp(guild, user, exp):
        if not "lvl_channel" in db['bots'][str(guild.id)]['chs']:
            return
        member = get_mention(guild, f"<@{user.id}>")

        current_xp = db['bots'][str(guild.id)]['memberbase'][str(user.id)]['xp']
        next_lvl = db['bots'][str(guild.id)]['memberbase'][str(user.id)]['nxtlvl']
        lvl = db['bots'][str(guild.id)]['memberbase'][str(user.id)]['level']
        xp = current_xp + exp

        if xp < next_lvl:
            db['bots'][str(guild.id)]['memberbase'][str(user.id)].update({"xp":xp})
            return

        while xp >= next_lvl:
            xp = xp - next_lvl
            lvl += 1
            next_lvl += round((lvl / 0.31) ** 2.0)
              
        db['bots'][str(guild.id)]['memberbase'][str(user.id)].update({"level":lvl, 'nxtlvl':next_lvl, "xp":xp})
        
        db.save()

        update_ranking(guild.id)

        banner = discord.File(await user_banner(member=member), filename="banner.png")

        embed = embed_builder(
            **{
                'title':f'Felicidades {(member.nick if member.nick else member.name)}!!!',
                'description':f"{member.mention} Has subido al nivel {lvl}",
                'color':member.color,
                'img':"attachment://banner.png"
            }
        )

        await guild.get_channel(db['bots'][str(guild.id)]['chs']["lvl_channel"]).send(file=banner, embed=embed)

class font_str():
    def __init__(self, text:str, font:ImageFont.FreeTypeFont) -> None:
        self.text = anti_utf8(text)
        self.font = font
        self.x = font.getbbox(self.text)[2]
        self.y = font.getbbox(self.text)[3]
        
        
    def __repr__(self) -> str:
        return self.text

def embed_builder(**ops):
    'title:any | description:any | color:dc_color | footer:any | img:url/none | thumb:url/none | fields:List[Dict]:{name:any, value:any, inline:bool}'

    embd = Embed(
            title = ops['title'] if 'title' in ops else None,
            description = ops['description'] if 'description' in ops else None,
            colour = ops['color']  if 'color' in ops else None,
            url = ops['url']  if 'url' in ops else None
        )
    if 'footer' in ops:
        if 'ficon' in ops:
            embd.set_footer(text=ops['footer'], icon_url=ops['ficon'])
        else:
            embd.set_footer(text=ops['footer'])
    if 'thumb' in ops:
        embd.set_thumbnail(url=ops['thumb'])
    if 'img' in ops:
        embd.set_image(url=ops['img'])
    if 'author' in ops:
        if 'author_img' in ops:
            embd.set_author(name=ops['author'], icon_url=ops['author_img'])
        else:
            embd.set_author(name=ops['author'])
    if 'fields' in ops:
        for field in ops['fields']:
            embd.add_field(name=field['name'], value=field['value'], inline=field['inline'])

    return embd

@cache
async def user_banner(ctx=False, member=False):

    if member:
            dcuser = member
    else:
            dcuser = ctx.author

    rank = font_str(dcuser.roles[-1].name , ImageFont.truetype("./images/Comfortaa-Bold.ttf", 32))

    name = font_str(dcuser.name, ImageFont.truetype("./images/Comfortaa-Regular.ttf", 32))

    nick = font_str((dcuser.nick if dcuser.nick else dcuser.name), ImageFont.truetype("./images/Comfortaa-Bold.ttf", 62))

    disc = font_str(f'#{dcuser.discriminator}', ImageFont.truetype("./images/Comfortaa-Light.ttf", 32))

    smal = lambda x: font_str(x, ImageFont.truetype("./images/Comfortaa-Regular.ttf", 28))

    dc_str = smal('DC: ')

    lvl = db['bots'][str(dcuser.guild.id)]['memberbase'][str(dcuser.id)]['level']
    xp = db['bots'][str(dcuser.guild.id)]['memberbase'][str(dcuser.id)]['xp']
    nextlvl = db['bots'][str(dcuser.guild.id)]['memberbase'][str(dcuser.id)]['nxtlvl']
    ranking = db['bots'][str(dcuser.guild.id)]['memberbase'][str(dcuser.id)]['ranking']

    exp = font_str(f'{get_exp(xp)}/{get_exp(nextlvl)} xp', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 32))
    lvl_str = font_str('nivel:  ', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 40))
    pos_str = font_str('ranking:  #', ImageFont.truetype("./images/Comfortaa-Regular.ttf", 40))
    level = font_str(str(lvl), ImageFont.truetype("./images/Comfortaa-Bold.ttf", 96))
    pos_rank = font_str(str(ranking), ImageFont.truetype("./images/Comfortaa-Bold.ttf", 96))

    await dcuser.avatar.save(fp = "./images/tempimage.webp")

    template = Image.open("./images/gltemplatebg.png")
    mask = Image.open("./images/cicularmask.png").convert('L')
    pfp = Image.open("./images/tempimage.webp").convert("RGBA")

    finalpfp = ImageOps.fit(pfp, (mask.size), centering=(0.5, 0.5))
    finalpfp.putalpha(mask)

    urs_color = ImageColor.getrgb(str(dcuser.color))

    decal = Image.new('RGBA', (1300, 350), urs_color)

    decalmask = Image.open("./images/templatedecalmask.png").convert('L')

    decal.putalpha(decalmask)
    bar = int((818 / nextlvl) * xp)

    xp_bar_placeholder = Image.new('RGBA', (818, 61), (45, 56, 50))
    xp_bar_full = Image.new('RGBA', (bar, 61), urs_color)
    xp_bar_full = ImageChops.invert(xp_bar_full)
    xp_bar_placeholder.paste(xp_bar_full, (0,0))
    xp_bar_mask = Image.open("./images/xpbar.png").convert('L')
    xp_bar_placeholder.putalpha(xp_bar_mask)


    template = Image.alpha_composite(template, decal)
    template.paste(finalpfp, (10,10), finalpfp)
    template.paste(xp_bar_placeholder, (401,251), xp_bar_placeholder)
    draw = ImageDraw.Draw(template)

    white = (255,255,255)
    gray = (170, 170, 170)

    mid = lambda text1, text2: (text1.y/2) - (text2.y/2)
    xpos = lambda text, vert: int(sqrt(abs((220 ** 2) - ((200 - (vert + (text.y * 2))) ** 2))))

    vertical = 15
    horizontal = 165 + xpos(rank, vertical)
    draw.text((horizontal, vertical), rank.text, urs_color, font=rank.font)
    horizontal += rank.x + 10
    draw.text((horizontal, vertical), name.text, gray, font=name.font)
    horizontal += name.x + 2
    draw.text((horizontal, vertical), disc.text, gray, font=disc.font)
    vertical += rank.y + 10
    horizontal = 165 + xpos(dc_str, vertical)
    draw.text((horizontal, vertical + mid(nick, dc_str)), dc_str.text, gray, font=dc_str.font)
    horizontal += dc_str.x + 5
    draw.text((horizontal, vertical), nick.text, white, font=nick.font)
    vertical += nick.y + 10
    horizontal = 165 + xpos(lvl_str, vertical)
    draw.text((horizontal, vertical + mid(level, lvl_str)), lvl_str.text, gray, font=lvl_str.font)
    horizontal += lvl_str.x + 6
    draw.text((horizontal, vertical), level.text, white, font=level.font)
    horizontal += level.x + 6
    draw.text((horizontal, vertical + mid(pos_rank, pos_str)), pos_str.text, gray, font=pos_str.font)
    horizontal += pos_str.x + 6
    draw.text((horizontal, vertical), pos_rank.text, white, font=pos_rank.font)
    horizontal = 582 - (exp.x / 2)
    vertical = 280.5 - (exp.y /2)
    draw.text((horizontal, vertical), exp.text, white, font=exp.font)

    template.save('./images/tempimage.png')
    return './images/tempimage.png'

class prettier(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[prettier cog]'
        self.bot.log.info(f'starting {self.__name__}...')

    async def lvl(self, ctx, mention=None):
        if not db['bots'][str(ctx.guild.id)]['setups'][self.bot.__name__]['config']['leveling']:
            return
        if not "lvl_channel" in db['bots'][str(ctx.guild.id)]['chs']:
            return
        if ctx.channel.id != db['bots'][str(ctx.guild.id)]['chs']["lvl_channel"]:
            await wreply(ctx, f"Usa el comando en el canal <#{db['bots'][str(ctx.guild.id)]['chs']['lvl_channel']}>")
            return
        
        user = get_mention(ctx.guild, str(mention))

        if user: 
            if type(user) is not discord.member.Member:
                await wreply(ctx, f"No pude encontrar a {mention} UwU")
                return

        banner = await user_banner(ctx, user)
        banner = discord.File(banner)
        await wreply(ctx, file=banner)

    @slash_command(name='lvl', help='help <placeholder>', brief='brief explanation')
    async def app_lvl(self, ctx, mention=None):
        await self.lvl(ctx, mention)
    
    @command(name='lvl')
    async def cmd_lvl(self, ctx, mention=None):
        await self.lvl(ctx, mention)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in db["ignored_ids"]:
            return
        if not message.guild:
            return
        if (message.guild.id not in self.bot.guild_ids) and self.bot.force_guilds:
            return
        if not db['bots'][str(message.guild.id)]['setups'][self.bot.__name__]['config']['leveling']:
            return
        if int(time()) - db['bots'][str(message.guild.id)]['memberbase'][str(message.author.id)]['xpcooldown'] <= 60:
                return
        await add_xp(message.guild, message.author, randint(30,50))
        db['bots'][str(message.guild.id)]['memberbase'][str(message.author.id)]['xpcooldown'] = int(time())
        
        
    @Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f'{self.__name__}: started!')

hat_log.info('ready')
