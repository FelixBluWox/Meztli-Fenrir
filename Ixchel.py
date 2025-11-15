#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord
from wox_sdb import db
from discord.ext.commands import *
from discord import Embed, Colour
from Gaia import *
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops, ImageColor
from math import sqrt
from Chia import user_auth
from functools import lru_cache as cache
import os
import youtube_dl

ixc_log = Wox_log('Ixchel')
ixc_log.info('loading...')

playlist = []


class y2_voice_chat(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[y2_voice_chat cog]'
        ixc_log.info(f'starting {self.__name__}...')
    

    
    @Cog.listener()
    async def on_ready(self):
        ixc_log.info(f'{self.__name__}: started!')

ixc_log.info('ready')
