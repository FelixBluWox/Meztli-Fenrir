#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
from apscheduler.schedulers.background import BackgroundScheduler
import discord
from wox_sdb import db
from discord.ext.commands import *
from Gaia import *
from Chia import user_auth
import requests
from functools import lru_cache as cache
from Hati import color, embed_builder
import asyncio
from phobos import *
from colorama import Fore

tky_log = Wox_log('Tsukuyomi', color=Fore.LIGHTGREEN_EX)
tky_log.info('loading...')

class Stream:
    def __init__(self, title, streamer, game, thumb, link, pfp):
        self.title = title
        self.streamer = streamer
        self.game = game
        self.thumb = thumb
        self.link = link
        self.pfp = pfp
        
def getOAuthToken():
    body = {
        'client_id': twitch_id,
        'client_secret': twitch_secret,
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
 
    keys = r.json()
    return keys['access_token']

HEADERS = {
        'Client-ID': twitch_id,
        'Authorization': 'Bearer ' + getOAuthToken()
}

@cache
def getpfp(id):
    url = "https://api.twitch.tv/helix/users?id=" + id
        
    req = requests.get(url, headers=HEADERS)
        
    res = req.json()

    if 'error' in res:
        try:
            raise HttpResponseError(res)
        except Exception as ex:
            tky_log.ferr(
                ex,
                f"{ex}: {ex.message}",
                f"Request returned HTTP error code {ex}"
            )
    elif len(res['data']) > 0:
            data = res['data'][0]
            pfp = data['profile_image_url']
            return pfp
    else:
            return None

@cache
def geticon(id):
    url = f"https://api.twitch.tv/helix/games?id={id}"
        
    req = requests.get(url, headers=HEADERS)
        
    res = req.json()

    if 'error' in res:
        try:
            raise HttpResponseError(res)
        except Exception as ex:
            tky_log.ferr(
                ex,
                f"{ex}: {ex.message}",
                f"Request returned HTTP error code {ex}"
            )
    elif len(res['data']) > 0:
            data = res['data'][0]
            icon = data['box_art_url']
            return icon
    else:
            return None  

def checkIfLive(channel):
    url = "https://api.twitch.tv/helix/streams?user_login=" + channel

    req = requests.get(url, headers=HEADERS)
        
    res = req.json()

    if 'error' in res:
        raise HttpResponseError(res)
    elif len(res['data']) > 0:
        return res['data'][0]
    else:
        return None

class twitch_integration(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[twitch_integration cog]'
        self.task = BackgroundScheduler()
        self.task.add_job(self.live_checker, 'interval', minutes=1)
        self.task.start()
        self.bot.log.info(f'starting {self.__name__}...')
    
    @cache
    def scolor(self, guild, streamer):
        if streamer in db['bots'][str(guild.id)]['streamers']:
            return color(db['bots'][str(guild.id)]['streamers'][streamer]['color'], 'teal')
        else:
            return color('teal')
            
    @command()
    @user_auth(5)
    async def so(self, ctx, twitch_name):
        data = checkIfLive(twitch_name)
        embed = embed_builder(
        **{
            "title":f"{data['user_name']} esta en vivo!",
            "description":f"[{data['title']}](https://www.twitch.tv/{data['user_name']})",
            "color":self.scolor(ctx.guild, data['user_name']),
            "thumb":getpfp(data['user_id']),
            "footer":data['game_name'],
            "ficon":geticon(data['game_id']).format(width=400,height=400),
            "img":data['thumbnail_url'].format(width=1280,height=720)
            }
        )
        await ctx.channel.send('@everyone', embed=embed)
        await ctx.message.delete()
    
    def live_checker(self):
        try:
            for guild in self.bot.active_guilds:
                if not db['bots'][str(guild.id)]['setups'][self.bot.__name__]['config']['ttvnotif']:
                    continue
                if not "ttv_channel" in db['bots'][str(guild.id)]['chs']:
                    continue
                for channel in db['bots'][str(guild.id)]['streamers']:
                    
                    data = checkIfLive(channel)

                    if data:
                        if (not db['bots'][str(guild.id)]['streamers'][channel]['islive']) or (db['bots'][guild.id]['streamers'][channel]['game'] != data['game_name']):
                            embed = embed_builder(
                                **{
                                    "title":f"{data['user_name']} esta en vivo!",
                                    "description":f"[{data['title']}](https://www.twitch.tv/{data['user_name']})",
                                    "color":self.scolor(guild, data['user_name']),
                                    "thumb":getpfp(data['user_id']),
                                    "footer":data['game_name'],
                                    "ficon":geticon(data['game_id']).format(width=400,height=400),
                                    "img":data['thumbnail_url'].format(width=1280,height=720)
                                }
                            )
                            asyncio.run_coroutine_threadsafe(self.bot.get_channel(db['bots'][str(guild.id)]['chs']["ttv_channel"]).send(db['bots'][str(guild.id)]['streamers'][channel]['message'], embed=embed), self.bot.loop)
                            db['bots'][str(guild.id)]['streamers'][channel]['islive'] = True
                            db['bots'][str(guild.id)]['streamers'][channel]['game'] = data['game_name']
                            db.save()

                    elif db['bots'][str(guild.id)]['streamers'][channel]['islive']:
                        db['bots'][str(guild.id)]['streamers'][channel]['islive'] = False
                        db.save()
            
        except Exception as ex:
            self.bot.log.ferr(
                ex,
                f"[{self.__name__}]: Error while checking for streams",
                f"An error ocurred while looking for live streams"
            )
    
    def islive(self, ctx, channel, col="blurple"):
        pass

    



    @Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f'{self.__name__}: started!')

tky_log.info('ready')
