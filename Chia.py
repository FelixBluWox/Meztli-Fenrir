#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord, os, sys
from functools import lru_cache as cache
from functools import wraps
from wox_sdb import db
from discord.ext.commands import *
from Gaia import *
from discord.ext.commands import *
from threading import Thread
from colorama import init, Fore
import asyncio, traceback
import logging
import inspect
import pickle
init()

dc_log = Wox_log('discord', stdout_warn_handler)

qi_log = Wox_log('Chia', color=Fore.LIGHTMAGENTA_EX)

def run_async(func, *args, **kwargs):
    new_thread = Thread(target=asyncio.run, args=(func(*args, **kwargs),))
    new_thread.start()

def thread_run(func, *args, **kwargs):
    new_thread = Thread(target=func, args=args, kwargs=kwargs)
    new_thread.start()

async def wsend(ctx, *args, **kwargs):
    if 'interaction' in vars(ctx):
        await ctx.interaction.channel.send(*args, **kwargs)
    elif 'prefix' in vars(ctx):
        await ctx.send(*args, **kwargs)
    else:
        raise TypeError("Invalid context object")
    pass

async def wreply(ctx, *args, **kwargs):
    if 'interaction' in vars(ctx):
        await ctx.respond(*args, **kwargs)
    elif 'prefix' in vars(ctx):
        await ctx.reply(*args, **kwargs)
    else:
        raise TypeError("Invalid context object")
    pass

def get_userid(ctx):
    if 'interaction' in vars(ctx):
        return ctx.user.id
    elif 'prefix' in vars(ctx):
        return ctx.author.id
    else:
        raise TypeError("Invalid context object")
    pass

@cache
def get_mention(guild, mention):
    if '<@!' == mention[:3]:
        return guild.get_member(int(mention[3:-1]))
    elif '<@&' == mention[:3]:
        return guild.get_role(int(mention[3:-1]))
    elif '<@' == mention[:2]:
        return guild.get_member(int(mention[2:-1]))
    elif '<#' == mention[:2]:
        return guild.get_channel(int(mention[2:-1]))
    else:
        return None
    
def get_interaction_name(interaction):
    interaction_types = {
        0:"Unknown",
        1:"Action Row",
        2:"Button",
        3:"String Select",
        4:"Text Input",
        5:"User Select",
        6:"Role Select",
        7:"Mentionable Select",
        8:"Channel Select"
    }
    if 'name' in interaction.data:
        name = interaction.data['name']
    elif 'component_type' in interaction.data:
        name = interaction_types.get(interaction.data['component_type'], 0)
    elif 'components' in interaction.data:
        name = ' & '.join(map(str, [f"{interaction_types.get(comp['type'], 0)}:{comp['value'] if 'value' in comp else ' & '.join(map(str, ['{}:{}'.format(interaction_types.get(compx['type'], 0), compx['value']) for compx in comp['components']]))}" for comp in interaction.data['components']]))
    else:
        name = json.dumps(interaction.data, ensure_ascii=False, indent=4, sort_keys=True)
    return name

def get_author(ctx):
    if 'interaction' in vars(ctx):
        return ctx.user
    elif 'prefix' in vars(ctx):
        return ctx.author

@cache
def get_user_auth(member)->int:
    if type(member) != discord.Member:
        raise TypeError(f"Invalid user")

    if member.id == root_usr:
        return 100
    elif str(member.id) in db['bots'][str(member.guild.id)]["modmins"]:
        return db['bots'][str(member.guild.id)]["modmins"][str(member.id)]
    else:
        user_creds = [db['bots'][str(member.guild.id)]["modmins"][str(k)] for k in [r.id for r in member.roles] if str(k) in db['bots'][str(member.guild.id)]["modmins"]]
        user_creds.append(-1)
        return max(user_creds)
    
def user_auth(lvl_required):
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return get_user_auth(get_author(ctx)) >= lvl_required
    return check(predicate)

def on_channel(channel):
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return channel.id == ctx.channel.id
    return check(predicate)

def on_guild(guild_id):
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return guild_id == ctx.guild.id
    return check(predicate)

class WoxBot(Bot):
    def __init__(self, command_prefix, guilds, name='WoxBot', force_guilds=True, **options):
        super().__init__(when_mentioned_or(command_prefix), **options)
        if not ((type(guilds) is int) or hasattr(guilds, '__iter__')): 
            raise TypeError(f"guilds must be int or itreable, got {type(guilds).__name__} {guilds} instead.")
        self.guild_ids = guilds if hasattr(guilds, '__iter__') else (guilds,)
        self.__name__ = name
        self.type = name.split(' ')[0]
        self.configs = {}
        for guild_id in self.guild_ids:
            if self.type in db['bots'][str(guild_id)]['setups']:
                self.configs.update({str(guild_id):db['bots'][str(guild_id)]['setups'][self.type]['config']})
            else:
                self.configs.update({str(guild_id):{"leveling": False, "ttvnotif": False}})
        self.on_message_threads = {}
        self.ready = False
        self.force_guilds = force_guilds
        self.log = Wox_log(self.__name__, color=Fore.LIGHTCYAN_EX)
        qi_log.info(f'iniciando [{self.__name__}]...')
    
    def enforce_guilds():
        async def predicate(self, ctx):
            if ctx.guild is None:
                raise NoPrivateMessage() 
            return ctx.guild.id in self.guild_ids
        return check(predicate)
    
    def after_ready(self, func):
        self.function_after_ready = func

    async def function_after_ready(self):
        pass
    
    def after_message(self, func):
        self.function_after_message = func

    async def function_after_message(self, ctx, message):
        pass
    
    def thread_after_message(self, func):
        self.function_thread_after_message = func

    async def function_thread_after_message(self, ctx, message):
        pass

    @property
    def active_guilds(self):
        guilds = []
        for guild_id in self.guild_ids:
            guild = self.get_guild(guild_id)
            if guild:
                guilds.append(guild)
        return guilds
        
    #!deprecated, must delete
    def getRoles(self):
        self.log.info(f'[{self.__name__}]: obteniendo roles...')
        self.roles = {}

        for guild_id in self.guild_ids:
            self.log.info(guild_id, ' : ', db['bots'][str(guild_id)]['rls'])
            self.channels[str(guild_id)] = {}

            self.channels[str(guild_id)].update({
                role : self.get_channel(db['bots'][str(guild_id)]['rls'][role]) 
                for role in db['bots'][str(guild_id)]['rls']
            })

    def getWebHooks(self):
        self.log.info(f'[{self.__name__}]: obteniendo webhooks...')

        #wh_anuncios = Webhook.partial(int(os.getenv('wh_anuncios_id')), os.getenv('wh_anuncios_token'), adapter=RequestsWebhookAdapter())
        pass

    def addChannel(self, name:str, **kwargs)->None:
        """
        Adds a chanel to the bot

        use
            addChannel(<name>, <id, env or channel>)
        then
            <bot>.<name> 
        to use the channel

        takes
            id: int, discord ID of the channel to add

            env: str, env key if the ID is on a .env file 

            channel: discord.channel.TextChannel, discord channel to 
            
        """
        ## to deprecate!
        self.log.info(f'[{self.__name__}]: añadiendo un nuevo canal de texto...')
        
        if not kwargs:
            raise TypeError('No key argumrnt was provided, must give either "id", "env" or "channel" but None was given')
        elif 'id' in kwargs:
            channel = self.get_channel(kwargs['id'])
        elif 'env' in kwargs:
            channel = self.get_channel(int(os.getenv(kwargs['env'])))
        elif 'channel' in kwargs:
            channel = kwargs['channel'] 
        else:
            raise TypeError(f'The Keywords must be "id", "env" or "channel", got {", ".join(map([f"{key}, {kwargs[key]}" for key in kwargs], str))} instead')
        setattr(self, 'ch_' + name, channel)
    
    async def on_member_join(self, member):
        if member.guild.id not in self.guild_ids:
            return

        self.log.info(f"user {anti_utf8(member.name)}#{anti_utf8(member.discriminator)} joined {anti_utf8(member.guild.name)}")

        if str(member.id) not in db['bots'][str(member.guild.id)]['memberbase']:
            db['bots'][str(member.guild.id)]['memberbase'][str(member.id)] = {
                "level": 1,
                "number": len(db['bots'][str(member.guild.id)]['memberbase']),
                "nxtlvl": 200,
                "ranking": 0,
                "xpcooldown":0,
                "xp": 0,
                "extra":{}
            }
        db.save()
    
    async def on_member_remove(self, member):
        if member.guild.id not in self.guild_ids:
            return

        self.log.info(f"user {anti_utf8(member.name)}#{anti_utf8(member.discriminator)} joined {anti_utf8(member.guild.name)}")

        uid = db['bots'][str(member.guild.id)]['memberbase'].pop(str(member.id), None)
        if not uid:
            self.log.warn(f"user {anti_utf8(member.name)}#{anti_utf8(member.discriminator)} was not in database")
        db.save()

    async def on_interaction(self, interaction):
        if interaction.guild is None:
            raise NoPrivateMessage()
        if (interaction.guild.id not in self.guild_ids) and self.force_guilds:
            return
    
        name = get_interaction_name(interaction)

        self.log.debug(f"{name}#{interaction.id} used by {interaction.user.id} in {interaction.guild.id} @ {interaction.channel.id}")
        self.log.info(f"{name} used by {anti_utf8(interaction.user.name)}#{interaction.user.discriminator} in {anti_utf8(interaction.guild.name)} @ {anti_utf8(interaction.channel.name)}")            
        
        await self.process_application_commands(interaction)

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in db["ignored_ids"]:
            return
        if not message.guild:
            return
        if (message.guild.id not in self.guild_ids) and self.force_guilds:
            return
        try:
            ctx = await self.get_context(message)
        except Exception as ex:
            self.log.fexc(
                    ex,
                    f"[{self.__name__}] Ignoring exception in on_message",
                    f"couldn't get message context"
            )
        if ctx.guild is None:
            self.log.warn(Fore.YELLOW + ctx.message.content + Fore.RESET)
            return
        #! deprecate ?
        if False: #db['bots'][str(self.guild_id)]['maintenance']:
            if user_auth(ctx) < 3:
                if ctx.valid:
                    await message.channel.send("El bot esta en mantenimiento, intenta mas tarde")
                    return
        if ctx.valid:
            self.log.debug(f"{ctx.command} used by {ctx.author.id} in {ctx.guild.id} @ {ctx.channel.id}")
            self.log.info(f"{ctx.command} used by {anti_utf8(ctx.author.name)}#{anti_utf8(ctx.author.discriminator)} in {anti_utf8(ctx.guild.name)} @ {anti_utf8(ctx.channel.name)} as {ctx.message.content}")
            with ctx.channel.typing():
                try:
                    await self.process_commands(message)
                except Exception as ex:
                    self.log.fexc(
                        error_form(
                            ex,
                            f"[{self.__name__}] Ignoring exception while processing command",
                            f"An error ocurred while processing {ctx.message}"
                        )
                    )
        else:
            run_async(self.function_thread_after_message, ctx, message)
            await self.function_after_message(ctx, message)
            return

    async def on_ready(self):
        self.log.info(f'[{self.__name__}]: Actualizando Base de datos')
        for guild in self.active_guilds:
            for number, member in enumerate(guild.members):
                if str(member.id) not in db['bots'][str(guild.id)]['memberbase']:
                    db['bots'][str(guild.id)]['memberbase'][str(member.id)] ={
                                "level": 1,
                                "number": number,
                                "nxtlvl": 200,
                                "ranking": 0,
                                "xpcooldown":0,
                                "xp": 0,
                                "extra":{}
                            }
                if  db['bots'][str(guild.id)]['memberbase'][str(member.id)]['number'] != number:
                    db['bots'][str(guild.id)]['memberbase'][str(member.id)]['number'] = number
        db.save()


        self.ready = True
        await self.function_after_ready()
        self.log.info(f'[{self.__name__}]: Sesion iniciada como: {self.user}')
        self.log.info(f'[{self.__name__}]: Corriendo :D !!!')
    
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (CommandNotFound, )

        if isinstance(error, ignored):
            return
        
        if isinstance(error, MissingRequiredArgument):
            return
        
        if isinstance(error, CheckFailure):
            self.log.info(f'{ctx.command} command bounced')
            return

        if isinstance(error, DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        else:
            await ctx.send("Algo salio mal con el comando UwU")

            self.log.ferr(
                    error,
                    f"[{self.__name__}] Ignoring exception in command {ctx.command}",
                    f"An error ocurred while executing command {ctx.command}: \n\trequester: {ctx.message.author} \n\tprefix: {ctx.prefix} \n\talias used: {ctx.invoked_with} \n\targuments: {ctx.args} \n\tkeywords: {ctx.kwargs} \n\tcurrent: {ctx.current_parameter} \n\tactual message: {ctx.message.content}"
            )


    async def on_application_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (CommandNotFound, )

        if isinstance(error, ignored):
            return
        
        if isinstance(error, MissingRequiredArgument):
            return
        
        if isinstance(error, CheckFailure):
            self.log.info(f'{ctx.command} command bounced')
            return

        if isinstance(error, DisabledCommand):
            await ctx.interaction.response.defer()
            await ctx.channel.send(f'El comando {ctx.command} ha sido desactivado.')

        elif isinstance(error, NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        else:
            try:
                await ctx.interaction.response.send_message("Algo salio mal con el comando UwU")
            except Exception:
                await ctx.channel.send("Algo salio mal con el comando UwU")

            self.log.ferr(
                    error,
                    f"[{self.__name__}] Ignoring exception in application command {ctx.command}"
            )
    
    





