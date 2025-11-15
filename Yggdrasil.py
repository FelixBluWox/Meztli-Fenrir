  #                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots
from Gaia import *
import discord, asyncio
from threading import Thread, Event
from discord.ui import Button, Select, View
from discord.ext import tasks
from discord.ext.commands import *
from Chia import WoxBot, user_auth, wreply
from Hati import embed_builder, color
from wox_sdb import db
import subprocess, argparse, platform, time
from Saturn import Bot_worker
from multiprocessing import JoinableQueue
from Chandra import web_cog
from colorama import Fore

parser = argparse.ArgumentParser()
parser.add_argument('-g', dest='guild_id', default=604593971829800990, type=int)

parameters = parser.parse_args()

patobot_bot_queue = JoinableQueue()
fenrir_bot_queue = JoinableQueue()
marcelo_bot_queue = JoinableQueue()

Patobot = Bot_worker(patobot_bot_queue)
Fenrir = Bot_worker(fenrir_bot_queue)
Marcelo = Bot_worker(marcelo_bot_queue)

ygg_log = Wox_log('Yggdrasil', color=Fore.LIGHTBLUE_EX)
ygg_log.info('loading...')
version = 1.0

bot_prossecees = []

modules = [
    "Self - Entry point",
    "Yggdrasil - t1.2 - Main",
    "Gaia - a1.2 - Utilities",
    "Hati - a1.3 - Design utilitie",
]

class cancel_button(Button):
    def __init__(self, msg):
        super().__init__(label="Cancelar", style=discord.ButtonStyle.red)
        self.msg = msg

    async def callback(self, interaction):
        await interaction.response.defer()
        await self.msg.delete()

class Bot_Button(Button):

    def __init__(self, gld, usr, bot, msg):
        super().__init__(label="Encender", style=discord.ButtonStyle.green)
        self.gld = gld
        self.usr = usr
        self.bot = bot
        self.msg = msg
        self.spent = False

    async def callback(self, interaction):
        if self.spent:
            return
        self.spent = True

        embed = embed_builder(**{
            "title":"Listo :D",
            "description":"Ya puedes usar el bot en tu servidor :D",
            "color":color("green"),
            "thumb":"https://i.postimg.cc/cCJ55VBw/check.png"
        })

        view = View()
        view.add_item(Button(label="Cancelar", style=discord.ButtonStyle.red, disabled=True))
        view.add_item(Button(label="Encender", style=discord.ButtonStyle.green, disabled=True))
        view.add_item(Button(label="Añadir", url=urls.get(self.bot)))

        await self.msg.edit(f"***Listo! :D, {self.bot} esta listo.***", embed=embed, view=view)
        await interaction.response.defer()

        entry = {
            "chs": {
            },
            "documents": {},
            "memberbase":{},
            "modmins": {
                str(self.usr.id):7
            },
            "setups": {
            },
            "streamers": {
            }
        }

        if str(self.gld.id) not in db['bots']:
            db['bots'][str(self.gld.id)] = entry
        
        db['bots'][str(self.gld.id)]['setups'][self.bot] = {
                    "config": {
                        "leveling": False,
                        "ttvnotif": False
                    },
                    "guild_id": self.gld.id,
                    "prefix": f"{self.bot.lower()[0]}."
                }

        db.save()
        
        if 'Fenrir' == self.bot:
            ygg_log.info('Starting new Fenrir instance')
            fenrir_bot_queue.put(('Fenrir', str(self.gld.id), i))
        if 'Patobot' == self.bot:
            ygg_log.info('Starting new Patobot instance')
            patobot_bot_queue.put(('Patobot', str(self.gld.id), i))
        if 'Marcelo' == self.bot:
            ygg_log.info('Starting new Patobot instance')
            marcelo_bot_queue.put(('Marcelo', str(self.gld.id), i))
        
        embed2 = embed_builder(**{
            "title":f"{self.bot} añadido a un nuevo servidor",
            "description":f"{self.bot} ha sido añadido al servidor {self.gld.name} por {self.usr.name}",
            "color":color(db['clients'][self.bot]['color']),
            "thumb":db['clients'][self.bot]['pfp']
        })

        await asyncio.sleep(10)
        await self.msg.edit('', embed=embed2, view=View())
        return

class Bot_Select(Select):

    def __init__(self, gld, usr) -> None:
        self.gld = gld
        self.usr = usr
        options = [discord.SelectOption(label=k, description=db['clients'][k]['description']) for k in db['clients']]
        super().__init__( 
            placeholder = "Elige un bot para añadir", 
            min_values = 1,
            max_values = 1,
            options = options
        )

    async def callback(self, interaction):
        if (str(self.gld.id) in db['bots']) and (self.values[0] in db['bots'][str(self.gld.id)]['setups']):
            await self.view.message.edit(
                "***Ese bot ya esta añadido a tu server!***", 
                embed=embed_builder(**{
                    "title":"Ese bot ya esta añadido!",
                    "description":'***El bot que seleccionaste ya esta en tu server, si no lo encuentras avisale a <@312807184927031306>, o selecciona otro bot para añadir',
                    "color":color("red"),
                    "footer":"Entra a la pagina y dale los permisos al bot, posteriormente ennciende el bot.",
                    "thumb":db['clients'][self.values[0]]['pfp']
                }))
            await interaction.response.defer()
            return

        embed = embed_builder(**{
            "title":"Añade y enciende el bot",
            "description":'Da click en el boton "Añadir" para añadir al bot al servidor, despues de añadirlo dale al boton "Encender" para iniciarl el bot',
            "color":color(db['clients'][self.values[0]]['color']),
            "footer":"Entra a la pagina y dale los permisos al bot, posteriormente ennciende el bot.",
            "thumb":db['clients'][self.values[0]]['pfp']
        })

        view = View()
        view.add_item(cancel_button(self.view.message))
        view.add_item(Bot_Button(self.gld, self.usr, self.values[0], self.view.message))
        view.add_item(Button(label="Añadir", url=urls.get(self.values[0])))

        await self.view.message.edit(f"***Añade a {self.values[0]}***", embed=embed, view=view)
        await interaction.response.defer()
        return



class general_commands(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[general_commands cog]'
        self.bot.log.info(f'starting {self.__name__}...')
    
    @command()
    @user_auth(5)
    async def test(self, ctx):
        await ctx.reply("a")
    
    @slash_command()
    @user_auth(5)
    async def stest(self, ctx):
        await ctx.respond("a")
    
    async def send_creator(self, ctx, link):
        if 'prefix' in vars(ctx):
            await ctx.message.delete()

        invite = await self.bot.fetch_invite(link)

        embed = embed_builder(**{
            "title":"Selecciona un Bot",
            "description":"Elige un bot de discord para añadir",
            "color":color("orange"),
            "footer":"una vez seleccionado, dale click al boton de añadir y enciende el bot :D",
            "thumb":"https://i.postimg.cc/44vvHLZQ/bot.png"
        })

        view = View()
        view.add_item(Bot_Select(invite.guild, ctx.author))

        if 'interaction' in vars(ctx):
            await ctx.respond("***Oye amigo... quieres un bot 7w7***",  )
        else:
            await ctx.send("***Oye amigo... quieres un bot 7w7***", embed=embed, view=view)
    
    @slash_command(name='bot', help='help <placeholder>', brief='brief explanation')
    @user_auth(2)
    async def cmd_bot(self, ctx, link):
        await self.send_creator(ctx, link)
    
    @command(name='bot')
    @user_auth(2)
    async def app_bot(self, ctx, link):
        await self.send_creator(ctx, link)

    @command()
    @user_auth(2)
    async def emb(self, ctx):
        json_txt = "".join(map(str, ctx.message.content.split("```")[1:]))[4:]
        if json_txt[-1] == ',':
            json_txt[-1] == ' '

        if json_txt:

            ops = json.loads(json_txt)

            ops['color'] = color(ops['color'])

            embed = embed_builder(**ops)

            text = None
            if 'text' in ops:
                text = ops['text']

            await ctx.channel.send(text, embed=embed)
            await ctx.message.delete()
        else:
            await ctx.reply("""mira los mensajes pineados del canal de staff para ver el funcionamiento del commando""")
        

    @Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f'{self.__name__}: started!')


class Quetzalcoatl(WoxBot):
    def __init__(self, command_prefix, guild, name='WoxBot', **options):
        super().__init__(command_prefix, guild, name, force_guilds=True, intents=discord.Intents.all(), **options)
        self.add_cog(general_commands(self))
        self.add_cog(web_cog(self, import_name=__name__,template_folder='./webpage', static_folder = './webpage'))
        self.log.info('Loading dismusic extension')

    async def function_after_ready(self):
        txt_modul = '\n        - '.join(map(str, modules))
        msg = f"""
            **Wox Yggdrasil version {version}, running on {platform.system()} {platform.release()} {platform.version()} Python {platform.python_version()} **
            
            ***Using the modules:***
                    - {txt_modul}

            *note: t - test, a - alpha, b - beta, r - release*
        """
        self.log.info(msg)


class Bot_instance():
    bot_instances = []
    stop_event = Event()
    def __init__(self) -> None:
        self.client = Quetzalcoatl("q.", parameters.guild_id, 'Quetzalcoatl')
        self.instance = Thread(target=self.client.run, args=(qztl_token,))
        self.stop_check.start()
        Bot_instance.bot_instances.append(self)
        self.instance.start()
    
    @tasks.loop(seconds=5.0)
    async def stop_check(self):
        if Bot_instance.stop_event.is_set():
            ygg_log.info(f'stopping Quetzalcoatl...')
            await self.client.close()

ygg_log.info('ready')



if __name__ == '__main__':

    #parameters.bot_type, guild, i

    Bot_instance()

    for i, guild in enumerate(db['bots']):
        if 'Fenrir' in db['bots'][guild]['setups']:
            ygg_log.info('Starting new Fenrir instance')
            fenrir_bot_queue.put(('Fenrir', guild, i))
        if 'Patobot' in db['bots'][guild]['setups']:
            ygg_log.info('Starting new Patobot instance')
            patobot_bot_queue.put(('Patobot', guild, i))
        if 'Marcelo' in db['bots'][guild]['setups']:
            ygg_log.info('Starting new Marcelo instance')
            marcelo_bot_queue.put(('Marcelo', guild, i))
    
    Fenrir.start()
    Patobot.start()
    
    while Bot_instance.stop_event.is_set() is False:
        try:
            time.sleep(200)
        except (SystemExit, KeyboardInterrupt) as ex:
            ygg_log.info('terminating program...')
            Bot_instance.stop_event.set()
            time.sleep(2)
            Bot_instance.bot_instances[0].instance.join()
            time.sleep(2)
            Patobot.W_stop()
            time.sleep(2)
            Fenrir.W_stop()
            time.sleep(2)
            ygg_log.info(f'Quetzalcoatl stopped')



