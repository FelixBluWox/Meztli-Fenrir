#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import discord
from wox_sdb import db
from Chia import wreply, thread_run, get_userid, get_mention
from Hati import embed_builder, user_banner
from discord.ext.commands import *
from discord import Embed, Colour
from Gaia import *
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops, ImageColor
from math import sqrt
from functools import lru_cache as cache
from colorama import Fore

sko_log = Wox_log('Skoll', color=Fore.LIGHTGREEN_EX)
sko_log.info('loading...')


from datetime import date
from threading import Thread



class user_manager(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        print("User_manager cog starting...")
        sc = Scheduler()
        sc.every().day.at("02:00").do(self.update_ranks)
        self.__name__ = '[user_manager]'
        wh_sm_console.send(f'inicializando{self.__name__}...')


    async def update_ranks(self):
        await self.bot.sm_console.send("updating user ranks...")
        
        for index, rank in enumerate(db["security"]["given_ranks"]):
            if rank['elapsed'] > rank['time']:
                expired = db["security"]["given_ranks"].pop(index)
                user = self.bot.guild.get_member(expired['userid'])
                if expired['section'] == 'report':
                    if expired['rank'] == 'strike1':
                        await user.remove_roles(self.bot.strike1_role)
                    elif expired['rank'] == 'strik2':
                        await user.remove_roles(self.bot.strike2_role)
                    elif expired['rank'] == 'ban1':
                        await user.remove_roles(self.bot.ban1_role)
                    elif expired['rank'] == 'ban2':
                        await user.remove_roles(self.bot.ban2_role)

                elif expired['section'] == 'rank':
                    if expired['rank'] == 'alpha':
                        await user.remove_roles(self.bot.rol_alpha)
                    elif expired['rank'] == 'beta':
                        await user.remove_roles(self.bot.rol_beta)
                    elif expired['rank'] == 'gamma':
                        await user.remove_roles(self.bot.rol_gama)
                    #elif expired['rank'] == 'vip':
                    #    user.remove_roles(self.bot.rol_vip)
            else:
                rank['elapsed'] += 1
                    
    @command()
    async def derank(self, ctx, to_rank, *args):
        if user_auth(ctx) >= 3:
            key = get_user(ctx, to_rank)
            if key:
                mem = ctx.guild.get_member(key['dcid'])
                demoted_from = []

                if self.bot.rol_alpha in mem.roles:
                    await mem.remove_roles(self.bot.rol_alpha)
                    demoted_from.append(self.bot.rol_alpha.name)
                if self.bot.rol_alpha in mem.roles:
                    await mem.remove_roles(self.bot.rol_beta)
                    demoted_from.append(self.bot.rol_beta.name)
                if self.bot.rol_alpha in mem.roles:
                    await mem.remove_roles(self.bot.rol_gama)
                    demoted_from.append(self.bot.rol_gama.name)
                if self.bot.rol_alpha in mem.roles:
                    await mem.remove_roles(self.bot.rol_vip)
                    demoted_from.append(self.bot.rol_vip.name)

                db["player_base"][key["number"]]['rank'] = 'Jugador'

                banner = discord.File(await user_banner(ctx, mem.id), filename="banner.png")
                embed = embed_builder(
                    **{
                        'title':f'{mem.nick} Has sido degradad@ de tu rango',
                        'description':f'{mem.mention} Se te quitaron los rangos de: {" ".join(map(str,demoted_from))}, Razon: {" ".join(map(str, args))}',
                        'color':mem.color,
                        'footer':'Ya no eres digno de tu titulo uwu',
                        'img':"attachment://banner.png"
                    }
                )
                await self.bot.ch_levels.send(file=banner, embed=embed)
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
    

    @command()
    async def alpha(self, ctx, to_rank):
        if user_auth(ctx) >= 3:
            key = get_user(ctx, to_rank)
            if key:
                
                mem = ctx.guild.get_member(key['dcid'])
                await mem.add_roles(self.bot.rol_alpha)
                db["player_base"][key["number"]]['rank'] = 'Alpha'

                banner = discord.File(await user_banner(ctx, mem.id), filename="banner.png")
                embed = embed_builder(
                    **{
                        'title':f'Felicidades {mem.nick}!!!',
                        'description':f'{mem.mention} Ahora eres alpha :D',
                        'color':mem.color,
                        'footer':'El principe Alí, Amas así, Alíaba búa...',
                        'img':"attachment://banner.png"
                    }
                )
                await self.bot.ch_levels.send(file=banner, embed=embed)
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
    
    @command()
    async def beta(self, ctx, to_rank):
        if user_auth(ctx) >= 3:
            key = get_user(ctx, to_rank)
            if key:
                
                mem = ctx.guild.get_member(key['dcid'])
                await mem.add_roles(self.bot.rol_beta)
                db["player_base"][key["number"]]['rank'] = 'Beta'

                banner = discord.File(await user_banner(ctx, mem.id), filename="banner.png")
                embed = embed_builder(
                    **{
                        'title':f'Felicidades {mem.nick}!!!',
                        'description':f'{mem.mention} Ahora eres beta :D',
                        'color':mem.color,
                        'footer':'Que elegancia la de francia 7w7',
                        'img':"attachment://banner.png"
                    }
                )
                await self.bot.ch_levels.send(file=banner, embed=embed)
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
    
    @command()
    async def gamma(self, ctx, to_rank):
        if user_auth(ctx) >= 3:
            key = get_user(ctx, to_rank)
            if key:
                
                mem = ctx.guild.get_member(key['dcid'])
                await mem.add_roles(self.bot.rol_gama)
                db["player_base"][key["number"]]['rank'] = 'Gamma'

                banner = discord.File(await user_banner(ctx, mem.id), filename="banner.png")
                embed = embed_builder(
                    **{
                        'title':f'Felicidades {mem.nick}!!!',
                        'description':f'{mem.mention} Ahora eres Gamma :D',
                        'color':mem.color,
                        'footer':'Bienvenido al distrito 1 y que la suerte este siempre de tu lado...',
                        'img':"attachment://banner.png"
                    }
                )
                await self.bot.ch_levels.send(file=banner, embed=embed)
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
    
    @command()
    async def vip(self, ctx, to_rank):
        if user_auth(ctx) >= 3:
            key = get_user(ctx, to_rank)
            if key:
                
                mem = ctx.guild.get_member(key['dcid'])
                await mem.add_roles(self.bot.rol_vip)
                db["player_base"][key["number"]]['rank'] = 'VIP'

                banner = discord.File(await user_banner(ctx, mem.id), filename="banner.png")
                embed = embed_builder(
                    **{
                        'title':f'Felicidades {mem.nick}!!!',
                        'description':f'{mem.mention} Ahora eres VIP :D',
                        'color':mem.color,
                        'footer':'Abran pasoo, persona importante pasandoo B)',
                        'img':"attachment://banner.png"
                    }
                )
                await self.bot.ch_levels.send(file=banner, embed=embed)
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
    
    async def _wl(self, ctx, mode, nick, dc):
        print('witelist', mode, nick, dc.name + '#' + dc.discriminator)
        if mode == 'update':
            print('updating')
            player = get_user(ctx, dc.id)
            await self.bot.mc_console.send(f"whitelist add {nick}")
            await self.bot.mc_console.send(f'discord link {nick} {dc.id}')
            await self.bot.wf_console.send(f"whitelist add {nick}")
            await self.bot.wf_console.send(f'discord link {nick} {dc.id}')
            temp_alt = dict(player["alts"])
            temp_alt.update({
                        f'{player["name"]}-{player["dcid"]}':player
            })
            db["player_base"][player["number"]].update(
                {
                    "uuid":None,
                    "name":nick,
                    "dcid":dc.id,
                    "dcname":dc.nick,
                    "alts":temp_alt
                }
            )
            await ctx.message.add_reaction(em_check)
            await ctx.reply(f"Has sido añadido como \"{nick}\" a la whitelist")
        elif mode == 'add':
            await ctx.author.add_roles(self.bot.rol_ghost)
            await self.bot.mc_console.send(f"whitelist add {nick}")
            await self.bot.mc_console.send(f'discord link {nick} {dc.id}')
            await self.bot.wf_console.send(f"whitelist add {nick}")
            await self.bot.wf_console.send(f'discord link {nick} {dc.id}')
            db["ranking"].append(len(db["player_base"]))
            db["player_base"].append(
                {
                    "uuid":None,
                    "name":nick,
                    "number":len(db["player_base"]),
                    "dcid":dc.id,
                    "dcname":dc.nick,
                    "rank":'Jugador',
                    "level":1,
                    "xp":0,
                    "nxtlvl":200,
                    "job":None,
                    "ranking":0,
                    "alts":{}
                }
            )
            update_ranking()
            await ctx.message.add_reaction(em_check)
            await ctx.reply(f"Has sido añadido como \"{nick}\" a la whitelist")
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.channel.send("Hmmm no funciono...")
            raise TypeError(f'mode must be "update" or "add" got {mode} instead')

    @command()
    async def wlremove(self, ctx, search):
        if user_auth(ctx) >= 3:
            player = get_user(ctx, search)
            if player:
                db["ranking"].pop(db["ranking"].index(player["number"]))
                removed = db["player_base"].pop(player['number'])
                for index, player in enumerate(db["player_base"]):
                    db["player_base"][index].update[{'number':index}]
                update_ranking()
                await ctx.message.add_reaction(em_check)
                await ctx.reply(f"{removed['dcname']}, {removed['name']} ha sido eliminado de la whitelist")
            else:
                await ctx.message.add_reaction(em_cross)
                await ctx.reply('No pude encontrar ese usuario en la base de datos UwU')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply('No tienes permisos para usar ese comando')
            

    @command()
    async def wl(self, ctx, nick):
        if ctx.channel.id == self.bot.ch_whitelist.id:
            if nick == 'help':
                await ctx.reply('Es asi:\n!wl <tu nick>\nSi es para ti, o:\n!wl <nick del jugador> <@mension del jugador>\n si es para otro jugador')
                return
            if user_auth(ctx) >= 3:
                if ctx.message.mentions:
                    player = get_user(ctx)
                    if player:
                        await self._wl(ctx, 'update', nick, ctx.message.mentions[0])
                    else:
                        await self._wl(ctx, "add", nick, ctx.message.mentions[0])

                else:
                    idplayer = get_user(ctx, ctx.author.id)
                    nmplayer = get_user(ctx, nick)
                    if idplayer and nmplayer:
                        await ctx.reply("Ya estas registrado...")
                    if idplayer:
                        await self._wl(ctx, 'update', nick, ctx.author)
                    if nmplayer:
                        await self._wl(ctx, 'update', nick, ctx.author)
                    else:
                        await self._wl(ctx, 'add', nick, ctx.author)
            else:
                if get_user(ctx, nick):
                    await ctx.reply('Ya te has registrado :D, solo puedes hacerlo una vez...')
                    return
                else:
                    await self._wl(ctx, 'add', nick, ctx.author)
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply("Este comando solo sirve en el canal de whitelist.")


    @wl.error
    async def wl_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.message.add_reaction(em_cross)
            if error.param.name == 'nick':
                if user_auth(ctx):
                    await ctx.reply('Es asi:\n!wl <tu nick>\nSi es para ti, o:\n!wl <nick del jugador> <@mension del jugador>\n si es para otro jugador')
                else:
                    await ctx.reply('Es asi: "!wl <tu nombre en minecraft>"')
        else:
            await ctx.message.add_reaction(em_cross)
            await ctx.reply("Algo salio mal con el comando UwU")
            wh_sm_console.send(f'{self.__name__}: algo salio mal con el comando WL')
            await self.bot.sm_console.send(f'Ignoring exception in command {ctx.command}:\n{type(error), error, error.__traceback__}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            



    @Cog.listener()
    async def on_ready(self):
        print('User_Manager cog started')
        wh_sm_console.send(f'{self.__name__}: listo!')

   