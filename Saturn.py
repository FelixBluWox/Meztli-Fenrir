#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
import sys
import io

# Fuerza UTF-8 para la salida estándar
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from discord.ext.commands import *
from discord.ext import tasks
from Gaia import *
import discord
from Chia import WoxBot, user_auth, get_mention, get_user_auth
from random import randint
import io, requests, platform
import aiohttp, codecs, json, asyncio
from Hati import prettier, embed_builder, color
from threading import Thread, Event
from multiprocessing import Process
#from Ixchel import y2_voice_chat
from wox_sdb import db
from random import randint
import io, requests
from web_integrations import web_server
from Tsukuyomi import twitch_integration
from Chandra import web_cog
import argparse
import time
from colorama import Fore
from WoxDocs import RolCity, Dynamite, WoxE621
from gtts import gTTS

parser = argparse.ArgumentParser()
parser.add_argument('-b', dest='bot_type', default='DevFenrir', type=str)
#parser.add_argument('-n', dest='number', default=0, type=int)

parameters = parser.parse_args()
bot_type = parameters.bot_type

sat_log = Wox_log('Saturn', color=Fore.LIGHTBLUE_EX)
sat_log.info('loading...')

version = 1.3

modules = [
    "Main - Entry point",
    "Saturn - b1.8 - Main",
    "Quilla - b1.6 - Discord integration",
    #"Ixchel - t1.1 - Discord Voice integration",
    "Gaia - a1.2 - Utilities",
    "Hati - a1.3 - Design utilitie",
    "DisMusic - 1.2.2b0 - external",
    #"Eris - t1.0 - Running process",
    #"Tsukuyomi - b1.5 - Twitch.tv",
    #"Chandra - t1.4 - web server"
]

formats=['png', 'jpg', 'gif' , 'webp', 'jpeg', 'jpg' , 'jpeg' ,'jfif' ,'pjpeg' , 'pjp', 'svg', 'bmp']

class general_commands(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[general_commands cog]'
        self.bot.log.info(f'starting {self.__name__}...')
        
    @command()
    @user_auth(7)
    async def leave(self, ctx):
        await ctx.guild.leave()
    
    @command()
    @user_auth(2)
    async def echo(self, ctx, *args):
        
        att = None
        files = []
        if ctx.message.attachments:
            for i, attatchment in enumerate(ctx.message.attachments):
                att = await ctx.message.attachments[i].to_file()
                print(att.filename.split(".")[-1], att.filename, f'attached_{i}.{att.filename.split(".")[-1]}')
                att.filename = f'attached_{i}.{att.filename.split(".")[-1]}'
                files.append(att)
        
        text=None
        if len(args) > 0:
            text = ' '.join(map(str, args))
        
        await ctx.channel.send(text, files=files)
        await ctx.message.delete()
    
    
    @command()
    async def mp3(self, ctx, *args):
        if len(args) < 1:
            return
        if args[0] == 'stop':
            await discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild).disconnect()
            print('arg stop')
            return
            
        if not ctx.message.attachments:
            print('no atach')
            return
        
        file = await ctx.message.attachments[0].to_file()
        if file.filename[-3:] != 'mp3':
            print('no mp3')
            return
            
        await file.save('temp.mp3')

        voice_channel=ctx.author.voice.channel
        bot_voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_voice_client and bot_voice_client.is_connected():
            if bot_voice_client.channel.id != voice_channel.id:
                await ctx.reply('El bot ya esta siendo usado en otro canal de voz UwU')
                return

        elif voice_channel!= None:
            bot_voice_client = await voice_channel.connect()
        else:
            await ctx.reply('No estas en ningun canal de voz.')
            return
        
        bot_voice_client.play(discord.FFmpegPCMAudio("temp.mp3"))
        
        #await discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild).disconnect()
        
        
        
    @command()
    async def ts(self, ctx, *args):
        if len(args) < 1:
            return
        if args[0] == 'stop':
            await discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild).disconnect()
            return
        
        author_name = ctx.author.nick if ctx.author.nick else ctx.author.name
        text = ' '.join(map(str, args))
        #text = anti_utf8(author_name) + " dice: " + text
        
        voice = gTTS(text=text, lang='es', slow=False)
        voice.save("test.mp3")

        voice_channel=ctx.author.voice.channel
        bot_voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_voice_client and bot_voice_client.is_connected():
            if bot_voice_client.channel.id != voice_channel.id:
                await ctx.reply('El bot ya esta siendo usado en otro canal de voz UwU')
                return

        elif voice_channel!= None:
            bot_voice_client = await voice_channel.connect()
        else:
            await ctx.reply('No estas en ningun canal de voz.')
            return
        
        bot_voice_client.play(discord.FFmpegPCMAudio("test.mp3"))

    @command()
    async def avatar(self, ctx, mention):
        mem = get_mention(ctx.guild, str(mention))

        if not mem:
            await ctx.reply(f"No pude encontrar a {mention} UwU")

        await ctx.reply(embed=embed_builder(**{
            "title":mem.nick if mem.nick else mem.name,
            "description":f"Imagen de perfil de {mention}",
            "img":mem.avatar.url,
            "color":mem.color
        }))

    @command()
    @user_auth(7)
    async def sendmsg(self, ctx, mention, *args):
        mem = get_mention(ctx.guild, str(mention))

        if '```' in ctx.message.content:
            json_txt = "".join(map(str, ctx.message.content.split("```")[1:]))[4:]
            print('\n\n\n\n\n\n\n\n\n')
            print(json_txt)
            print('\n\n\n\n\n\n\n\n\n')
            
            if json_txt[-1] == ',':
                json_txt[-1] == ' '

            if json_txt:

                print(json_txt)

                ops = json.loads(json_txt)

                ops['color'] = color(ops['color']) if 'color' in ops else color('random')

                embed = embed_builder(**ops)

                text = None
                if 'text' in ops:
                    text = ops['text']

                await mem.send(text, embed=embed)
                await ctx.message.delete()
            else:
                await ctx.reply("""mira los mensajes pineados del canal de staff para ver el funcionamiento del commando""")
        else:
            if not mem:
                await ctx.reply(f"No pude encontrar a {mention} UwU")

            await mem.send(' '.join(map(str, args)))
            await ctx.message.delete()

        await ctx.send('mensaje enviado ;)', delete_after=5) 





    @command()
    @user_auth(5)
    async def sendemb(self, ctx):

        emb = {
            "text":"@ /everyone",
            "title":"**BIENVENIDO A INCA RP - ORIGINAL**",
            "color":'#131c47',
            "fields":[
                {"name":"***Normas generales de comportamiento:***", "value":"", "inline":"false"},
                {"name":"**1.**", "value":"No usar lenguaje ofensivo, calumnias u ofensas hacia los otros usuarios de este servicio.", "inline":"false"},
                {"name":"**2.**", "value":"Mantener una conducta decente y de respeto mutuo cuando utiliza este servicio.", "inline":"false"},
                {"name":"**3.**", "value":"No publicar mensajes comerciales (SPAM masivo de otros canales).", "inline":"false"},
                {"name":"**4.**", "value":"No enviar repetida e indiscriminadamente mensajes en el chat (SPAM).", "inline":"false"},
                {"name":"**5.**", "value":"No mayúsculas.", "inline":"false"},
                {"name":"**6.**", "value":"Esta totalmente prohibido hablar acerca de la vida privada de cualquier miembro del staff y/o usuario. El incumplimiento de esta norma lleva a baneo inmediato del server.", "inline":"false"},
                {"name":"**7.**", "value":"Mantener el respeto a todas las personas en el server, cualquier acoso físico, ideológico, religioso, etc.", "inline":"false"},
                {"name":"**8.**", "value":"Esta prohibido tagear al cuerpo administrativo, si necesitas asistencia existe un canal respectivo <#1342322908449607812> .", "inline":"false"},
                {"name":"**9.**", "value":"Prohibido hacer cualquier tipo de spam (símbolos, frases o palabras) y/o flood (FLOOD: realizar repetidamente el enviado de mensaje en un corto periodo de tiempo).", "inline":"false"},
                {"name":"**10.**", "value":"Es necesario el uso correcto de los topics.", "inline":"false"},
                {"name":"**11.**", "value":"Prohibido el contenido NSFW(+18). ", "inline":"false"},
                {"name":"**12.**", "value":"Está completamente prohibido hacerse pasar por cualquier tipo de persona en el servidor.", "inline":"false"},
                {"name":"**13.**", "value":"Esta prohibido escribir al privado de algún miembro del cuerpo administrativo para apelar algún tipo de sanción.", "inline":"false"},
                {"name":"**14.**", "value":"Esta prohibido la toxicidad en todo sentido.", "inline":"false"}
            ],
            "footer":"Att. El equipo de INCA RP.",
            "thumb":"https://media.discordapp.net/attachments/1342338440607301663/1342360213831024640/imagen.png?ex=67b959de&is=67b8085e&hm=a768e12cf99265ea042f17bb86a05b0539e5948aee4ef0e85a0e7f75bd856ce1&=&format=webp&quality=lossless&width=621&height=621",
            "img":"https://media.discordapp.net/attachments/1342338440607301663/1342360296374665216/imagen.png?ex=67b959f2&is=67b80872&hm=72861801aeec953d36f490ae1980eb0f85c57002ae824a5b67905d23351b26c6&=&format=webp&quality=lossless&width=1104&height=621"
        }

        ops = emb

        ops['color'] = color(ops['color'])

        embed = embed_builder(**ops)

        text = None
        if 'text' in ops:
            text = ops['text']

        await ctx.channel.send(text, embed=embed)
        await ctx.message.delete()
    
    @command()
    @user_auth(1)
    async def authlvl(self, ctx):
        await ctx.reply(f"Tu nivel de autorizacion es: {get_user_auth(ctx.author)}")

    @command()
    @user_auth(5)
    async def test(self, ctx):
        await ctx.reply("a")

    @slash_command()
    @user_auth(5)
    async def stest(self, ctx):
        await ctx.respond("a")
    
    @command()
    @user_auth(5)
    async def testex(self, ctx):
        raise Exception('esto es una prueba')

    @slash_command()
    @user_auth(5)
    async def stestex(self, ctx):
        raise Exception('esto es una prueba')

    @command()
    @user_auth(5)
    async def adstream(self, ctx, streamer, c="teal"):
        msg = ctx.message.content.split(' ')
        msg = ''.join(msg[3:])
        new = {
            "color":c,
            "islive":False,
            "game":None,
            "message":msg
        }
        if streamer in db['bots'][str(ctx.guild.id)]['streamers']:
            await ctx.reply("El stremer ya esta enlistado")
        else:
            db['bots'][str(ctx.guild.id)]['streamers'][streamer] = new
            db.save()
            await ctx.reply(f"{streamer} añadido a la lista de notificaciones :D")
    
    @command()
    @user_auth(7)
    async def auth(self, ctx, level, mention):

        role = get_mention(ctx.guild, str(mention))
        
        if type(role) not in (discord.member.Member, discord.role.Role):
            await ctx.reply("usuario invalido")
            return
        
        db['bots'][str(ctx.guild.id)]["modmins"][str(role.id)] = int(level)
        db.save()

        await ctx.reply(f"{role.mention} ahora tiene permisos de Moderacion de nivel {level} :D")
    
    @command()
    @user_auth(7)
    async def deauth(self, ctx, mention):

        role = get_mention(ctx.guild, str(mention))
        
        if type(role) not in (discord.member.Member, discord.role.Role):
            await ctx.reply("usuario invalido")
            return
        
        if str(role.id) not in db['bots'][str(ctx.guild_id)]["modmins"]:
            await ctx.reply(f"{role.mention} no tiene permisos que revocar")
            return
        
        db['bots'][str(ctx.guild.id)]["modmins"].pop(str(role.id))
        db.save()

        await ctx.reply(f"{role.mention} ya no tiene permisos")
    
    @command()
    @user_auth(2)
    async def img(self, ctx):
        if ctx.message.attachments:
            file = await ctx.message.attachments[0].to_file()
            file.filename = 'attached.png'
        else:
            await ctx.message.delete()
            await ctx.send(f'{ctx.author.mention} no enviaste un archivo valido')
            return
            
        await ctx.channel.send(file=file)
        await ctx.message.delete()
    
    @command()
    @user_auth(5)
    async def rem(self, ctx, id:int):
        msg = await ctx.fetch_message(int(id))
        mention, nick, name = msg.author.mention, msg.author.nick, msg.author.name
        
        await msg.delete()
        await ctx.message.delete()
        
        embed = embed_builder(**{
            "title":f"eliminado un mensaje de {name}",
            "color":ctx.author.color,
            "author":ctx.author.nick if ctx.author.nick else ctx.author.name,
            "author_img":ctx.author.avatar.url
        })
        
        await ctx.send(embed=embed, delete_after=120) 
        

    @command()
    @user_auth(2)
    async def emb(self, ctx):
        json_txt = "".join(map(str, ctx.message.content.split("```")[1:]))[4:]
        if json_txt[-1] == ',':
            json_txt[-1] == ' '

        if json_txt:

            print(json_txt)

            ops = json.loads(json_txt)

            ops['color'] = color(ops['color']) if 'color' in ops else color('random')

            embed = embed_builder(**ops)

            text = None
            if 'text' in ops:
                text = ops['text']

            att = None
            files = []
            if ctx.message.attachments:
                for i, attatchment in enumerate(ctx.message.attachments):
                    att = await ctx.message.attachments[i].to_file()
                    print(att.filename.split(".")[-1], att.filename, f'file_{i}.{att.filename.split(".")[-1]}')
                    att.filename = f'file_{i}.{att.filename.split(".")[-1]}'
                    files.append(att)
            else:
                file = None
            
            await ctx.channel.send(text, embed=embed, files=files)
            await ctx.message.delete()
        else:
            await ctx.reply("""mira los mensajes pineados del canal de staff para ver el funcionamiento del commando""")
        

    @Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f'{self.__name__}: started!')



class Fenrir(WoxBot):
    def __init__(self, command_prefix, guild, name='WoxBot', **options):
        super().__init__(command_prefix, guild, name, force_guilds=False, intents=discord.Intents.all(), **options)
        self.add_cog(prettier(self))
        self.add_cog(general_commands(self))
        #self.add_cog(web_cog(self, import_name=__name__,template_folder='./webpage', static_folder = './webpage'))
        self.add_cog(twitch_integration(self))

        self.add_cog(RolCity(self))
        self.add_cog(Dynamite(self))
        self.add_cog(WoxE621(self))

        self.lavalink_nodes = [
            {"host": "127.0.0.1", "port": 2333, "password": "plumonenlacola"},
            #{"host": "WoxLavalink.bluwoxdev.repl.co", "port": 433, "password": "WoxDevelLavalink"},
            #{"host": "lavalink.oops.wtf", "port": 2000, "password": "www.freelavalink.ga"},
            #{"host": "connect.freelavalink.ga", "port": 2000, "password": "www.freelavalink.ga"}
        ]
        self.spotify_credentials = {
            "client_id": spotify_id,
            "client_secret": spotify_secret,
        }
        self.log.info('Loading dismusic extension')
        self.load_extension("dismusic")

    async def function_after_ready(self):
        txt_modul = '\n        - '.join(map(str, modules))
        msg = f"""
            **Meztli Fenrir version {version} Running bot {parameters.bot_type}, running on {platform.system()} {platform.release()} {platform.version()} Python {platform.python_version()} **
            Bot_instance
            ***Using the modules:***
                    - {txt_modul}

            *note: t - test, a - alpha, b - beta, r - release*
        """
        self.log.info(msg)


class Bot_instance():
    bot_instances = []
    stop_event = Event()
    def __init__(self, t, g, n) -> None:
        self.num = n
        db.reload()
        self.client = Fenrir(db['bots'][g]['setups'][t]['prefix'], int(g), f'{t} #{n}', loop=asyncio.new_event_loop())
        #self.client.run_wsv()
        self.instance = Thread(target=self.client.run, args=(bots[t],))
        self.stop_check.start()
        Bot_instance.bot_instances.append(self)
        self.instance.start()
    
    @tasks.loop(seconds=5.0)
    async def stop_check(self):
        if Bot_instance.stop_event.is_set():
            sat_log.info(f'stopping bot #{self.num}...')
            await self.client.close()


class Bot_worker(Process):
    def __init__(self, task_queue):
        Process.__init__(self)
        self.task_queue = task_queue
        self.do_loop = True

    def run(self):
        proc_name = self.name
        while self.do_loop:
            args = self.task_queue.get()
            if args:
                sat_log.info(f'starting bot {args[0]} #{args[2]}')
                Bot_instance(*args)
                self.task_queue.task_done()
            else:
                self.task_queue.task_done()
                time.sleep(200)
        return
    
    def W_stop(self):
        sat_log.info('terminating program...')
        Bot_instance.stop_event.set()
        for botinst in Bot_instance.bot_instances:
            botinst.instance.join()
            sat_log.info(f'bot #{botinst.num} stopped')
        self.do_loop = False
        self.terminate()


sat_log.info('ready')

from time import sleep

if __name__ == '__main__':

    allowed_ids = (
        1275599013957337201, 
        1100990594395942983, 
        1094736534076412036, 
        1078770572516921475, 
        1082415154332967063, 
        972251747198320710, 
        997679468996993105,
        1068420065692766308, 
        436251217073668096, 
        515339969771077643, 
        972251747198320710, 
        795150584096620544, 
        604593971829800990, 
        967225811700695060
    )

    for aid in allowed_ids:

        entry = {
                "chs": {
                },
                "documents": {},
                "memberbase":{},
                "extra":{},
                "modmins": {
                },
                "setups": {
                },
                "streamers": {
                }
        }

        if str(aid) not in db['bots']:
                db['bots'][str(aid)] = entry
            
        db['bots'][str(aid)]['setups']["Fenrir"] = {
                        "config": {
                            "leveling": False,
                            "ttvnotif": False
                        },
                        "guild_id": aid,
                        "prefix": "f."
        }

    db.save()

    #ngrok_instance = Popen('python3 ./lavalinksv/start_lavalink.py', creationflags=CREATE_NEW_CONSOLE)

    #fenrir_client = Fenrir('f.', allowed_ids, 'Fenrir')
    #fenrir_client = Fenrir('m.', 515339969771077643, 'Marcelo')
    #fenrir_client = Fenrir('p.', 604593971829800990, 'Patobot')
    #fenrir_client = Fenrir('m.', 1078770572516921475, 'Fenrir')
    #fenrir_client.run_wsv()


    fenrir_client = Fenrir(bot_type.lower()[0] + '.', allowed_ids, bot_type)


    @fenrir_client.command()
    @user_auth(5)
    async def testout(ctx):
        await ctx.reply("a")

    @fenrir_client.slash_command()
    @user_auth(5)
    async def stestout(ctx):
        await ctx.respond("a")

    def fenrir_run():
        fenrir_client.run(bots[bot_type])

    fenrir_process = Process(target=fenrir_run())

    fenrir_process.start()


    #client = Fenrir(f'{parameters.bot_type.lower()[0]}.', parameters.guild_id, parameters.bot_type)
    #client.run(bots[parameters.bot_type])


