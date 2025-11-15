#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord
from functools import lru_cache as cache
from multiprocessing import Process
from wox_sdb import db
from Gaia import *
from discord.ext.commands import *
import traceback

dc_log = wox_log('discord', stdout_warn_handler)

er_log = wox_log('Eris')


class WoxBot(Bot):
    def __init__(self, command_prefix, guild, name='WoxBot', description=None, **options):
        super().__init__(command_prefix, description=description, **options)
        self.guild_id = guild
        self.__name__ = name
        self.on_message_threads = {}
        self.ready = False
        er_log.info(f'iniciando [{self.__name__}]...')
    
    def on_guild():
        async def predicate(self, ctx):
            if ctx.guild is None:
                raise NoPrivateMessage() 
            return ctx.guild.id == self.guild_id
        return check(predicate)
    
    @on_guild()
    async def on_member_join(member):
        if False: #db['maintenance']:
            if user_auth(ctx) < 3:
                if ctx.valid:
                    await message.channel.send("El bot esta en mantenimiento, intenta mas tarde")
                    return
        else:
            pass

    @on_guild()
    async def on_message(self, message):
        try:
            ctx = await self.get_context(message)
        except Exception as ex:
            er_log.error(
                error_form(
                    ex,
                    f"[{self.__name__}] Ignoring exception while processing command",
                    f"An error ocurred while processing {ctx.message}"
                )
            )
        
        if False: #db['maintenance']:
            if user_auth(ctx) < 3:
                if ctx.valid:
                    await message.channel.send("El bot esta en mantenimiento, intenta mas tarde")
                    return
        else:
            return

    async def on_ready(self):
        self.guild = self.get_guild(self.guild_id)
        self.ready = True
        er_log.info(f'[{self.__name__}]: Sesion iniciada como: {self.user}')
        er_log.info(f'[{self.__name__}]: Corriendo :D !!!')
    
    async def on_error(self, error):
        er_log.error(f'Ignoring exception: {type(error).__name__} {type(error).__name__} Error:\n{"".join(map(str, traceback.format_exception(type(error), error, error.__traceback__)))}\n detalles: \n{"".join(map(str,error.args))}')

dis_log = wox_log('Disnomia')

version = 1.3

intents = discord.Intents.all()
client = WoxBot("p.", 604593971829800990, name='Disnomia', intents=intents)

def run_process():
    client.run(dc_token)

disnomia_process = Process(target=run_process)

def Disnomia_Start():
    dis_log.info('starting...')
    disnomia_process.start()

def Disnomia_Stop():
    disnomia_process.terminate()

dis_log.info('ready')



    

    


    
