#              Felix Blu Wox (c) All Rights Reserved 2023
from flask import Flask, request, render_template
from discord.ext.commands import *
from wox_sdb import db
import discord
from Chia import *
from random import randint
from requests import post

mc_colors = {
    'black':'§0',
    'dark_blue':'§1',
    'dark_green':'§2',
    'dark_aqua':'§3',
    'dark_red':'§4',
    'dark_purple':'§5',
    'gold':'§6',
    'gray':'§7',
    'dark_gray':'§8',
    'blue':'§9',
    'green':'§a',
    'aqua':'§b',
    'red':'§c',
    'light_purple':'§d',
    'yellow':'§e',
    'white':'§f',
    'o':'§k',
    'b':'§l',
    's':'§m',
    'u':'§n',
    'i':'§o',
    'r':'§r'
}
mcc = lambda x: mc_colors.get(x, '§r')

adv_especial = {
    "mine_diamond",
    "obtain_ancient_debris",
    "enter_the_end",
    "enter_end_gateway",
    "tame_an_animal",
    "enter_the_nether",
    "return_to_sender"
}

adv_epic = {
    "summon_iron_golem",
    "bullseye",
    "sniper_duel",
    "two_birds_one_arrow",
    "find_end_city",
    "cure_zombie_villager",
    "netherite_armor",
    "honey_block_slide",
    "use_lodestone",
    "get_wither_skull",
    "dragon_breath",
    "elytra",
    "silk_touch_nest",
    "create_beacon",
    "very_very_frightening",
    "levitate",
    "hero_of_the_village",
    "find_fortress",
    "explore_nether"
}

adv_ultimate = {
    "fast_travel",
    "arbalistic",
    "respawn_dragon",
    "adventuring_time",
    "uneasy_alliance",
    "kill_dragon",
    "totem_of_undying",
    "balanced_diet",
    "kill_all_mobs",
    "all_potions",
    "complete_catalogue",
    "summon_wither",
    "all_effects",
    "create_full_beacon",
    "dragon_egg",
    "bred_all_animals",
    "obtain_netherite_hoe"
}


class web_server(Cog, Flask):
    def __init__(self, bot, *args, **kwargs) -> None:
        super(web_server, self).__init__(*args, **kwargs)
        self.bot = bot
        print("Web server cog starting...")

        self.panel = lambda: render_template("temp.html")
        self.players = lambda: render_template("temp.html")
        self.estadis = lambda: render_template("temp.html")
        self.botstate = lambda: render_template("botstate.html")

        self.add_url_rule('/home', 'home', self.home)
        self.add_url_rule('/', '', self.home)
        self.add_url_rule('/controlpanel', 'controlpanel', self.panel)
        self.add_url_rule('/players', 'players', self.players)
        self.add_url_rule('/statistics', 'statistics', self.estadis)
        self.add_url_rule('/discordbot', 'discordbot', self.botstate)

        self.add_url_rule('/send', 'send', self.send_post, methods=["POST"])

        self.add_url_rule('/mc_port/mc_test', 'mc_port/mc_test', self.mc_test, methods=["GET"])
        self.add_url_rule('/mc_port/mc_strike', 'mc_port/mc_strike', self.mc_strike, methods=["POST"])
        self.add_url_rule('/mc_port/mc_ban', 'mc_port/mc_ban', self.mc_ban, methods=["POST"])

        #self.add_url_rule('/mc_port/mc_new_player', 'mc_port/mc_new_player', self.mc_new_player, methods=["POST"])
        self.add_url_rule('/mc_port/mc_player_achievement', 'mc_port/mc_player_achievement', self.mc_player_achievement, methods=["POST"])

        setattr(self.bot, 'run_wsv', self.run)
        
        self.__name__ = '[web_server]'

    

    def home(self):
        print('Pinged')
        return render_template("index.html")


    def send_post(self):
        data = request.get_json()
        pass

    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    # MINECRAFT COMMANDS
    def mc_test(self):
        return mcc('blue') + mcc('b') + 'Echo desde el bot de ghostland :D'

    def mc_strike(self):
        return 'echo desde ghostald discord'

    def mc_ban(self):
        #savejson(request.__dict__, 'post.json')
        data = request.get_json()
        print (request.headers)
        print(data)

        return f'El bot de ghostland te dice hola {data["name"]}'
        pass
    
    # MINECRAFT COMMANDS
    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    # MINECRAFT EVENTS

        
        return 'Bienvenido al servidor, espero te diviertas'

    def mc_player_achievement(self):
        data = request.get_json()
        advancement_info = data['advancement'].split('/')
        logro = False
        if advancement_info[0] == 'recipes':
            exp = randint(30, 50)
        elif advancement_info[0] in adv_especial:
            exp = randint(2800, 3000)
            logro = '&6&lespecial :D&r'
        elif advancement_info[0] in adv_epic:
            exp = randint(7800, 8000)
            logro = '&d&lepico B)&r'
        elif advancement_info[0] in adv_ultimate:
            exp = randint(17000, 20000)
            logro = '&b&lincreible :O&r'
        else:
            exp = randint(700, 800)
            logro = ':)'
        
        if logro:
            return f'{data["display"]}&r has recibido &a&l{exp}&r de experiencia por completar un logro {logro}'
        else:
            return "None"
        pass
    
    # MINECRAFT EVENTS
    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    


    def serve(self):
        from waitress import serve
        serve(self ,host='0.0.0.0',port=8080, _quiet=True, threads=6)

    def run(self):
        thread_run(self.serve)

    @Cog.listener()
    async def on_ready(self):
        print('Web server cog started')
