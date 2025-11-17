#                        Felix Blu Wox (c) 2023
#  This file is part of the WoxFenrir framework for creating Discord bots
from flask import Flask, request, render_template, jsonify, redirect, url_for
from discord.ext.commands import *
from wox_sdb import db
import discord
from Chia import *
from random import randint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

chn_log = Wox_log('Chandra', color=Fore.LIGHTGREEN_EX)
chn_log.info('loading...')




login_manager = LoginManager()

class dummy_bot():
    def __init__(self, *args, **kwargs) -> None:
        self.log = Wox_log('DummyBot', color=Fore.LIGHTCYAN_EX)

class web_cog(Cog, Flask):
    def __init__(self, bot, *args, **kwargs) -> None:
        super(web_cog, self).__init__(*args, **kwargs)
        self.bot = bot
        self.__name__ = '[web_server]'
        self.bot.log.info(f'starting {self.__name__}...')
        self.secret_key = os.urandom(24)

        login_manager.init_app(self)

        self.client = WebApplicationClient(twitch_id)

        self.dashboard = lambda: render_template("temp.html")
        self.streams = lambda: render_template("temp.html")
        self.statistics = lambda: render_template("temp.html")
        self.activity = lambda: render_template("botstate.html")

        self.add_url_rule('/home', 'home', self.home)
        self.add_url_rule('/', '', self.home)
        self.add_url_rule('/dashboard', 'dashboard', self.dashboard)
        self.add_url_rule('/streams', 'streams', self.streams)
        self.add_url_rule('/statistics', 'statistics', self.statistics)
        self.add_url_rule('/activity', 'activity', self.activity)

        self.add_url_rule('/login', 'login', self.login)
        self.add_url_rule('/oauth', 'oauth', self.oauth, methods=["POST"])

        self.add_url_rule('/send', 'send', self.send_post, methods=["POST"])

        self.add_url_rule('/webhooks/ttk', 'webhooks/ttk', self.wh_tiktok, methods=["POST"])

        self.add_url_rule('/webhooks/ttv', 'webhooks/ttv', self.wh_twitch, methods=["POST"])
        setattr(self.bot, 'wsv', self)
        setattr(self.bot, 'run_wsv', self.run)
        

    @login_manager.user_loader
    def load_user(self, user_id):
        print(user_id)
        return None

    def login(self):
        auth_endpoint = ttv_oidc_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            auth_endpoint,
            redirect_uri="https://cd39-201-121-236-162.ngrok.io/oauth",
            scope=["channel:read:vips"],
        )
        return redirect(request_uri)
    
    def home(self):
        self.bot.log.info(f'{self.__name__}: pinged')
        return render_template("home_user.html")

        if current_user.is_authenticated:
            return render_template("home_user.html")
        else:
            return render_template("home_rando.html")
    
    def oauth(self):
        code = request.args.get("code")

        token_endpoint = ttv_oidc_cfg["token_endpoint"]

        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response='https' + request.url[4:],
            redirect_url='https' + request.base_url[4:],
            code=code
        )

        body = {
            'client_id': twitch_id,
            'client_secret': twitch_secret,
            "grant_type": 'authorization_code',
            'code':code,
            'redirect_uri':"https://cd39-201-121-236-162.ngrok.io/home"
        }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)
        print(r.json())
    

        # Parse the tokens!
        self.client.parse_request_body_response(json.dumps(r.json()))


        userinfo_endpoint = ttv_oidc_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        print(userinfo_response.json())

        resp = jsonify(success=True)
        return resp

        return redirect('https://cd39-201-121-236-162.ngrok.io')


    def wh_tiktok(self):
        data = request.get_json()
        print(data)
        resp = jsonify(success=True)
        return resp

    def wh_twitch(self):
        data = request.get_json()
        print(data)
        resp = jsonify(success=True)
        return resp

    def send_post(self):
        data = request.get_json()
        print (request.headers)
        print(data)
        pass

    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    
    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    
    #▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    


    def serve(self):
        from waitress import serve
        serve(self ,host='0.0.0.0',port=8080, _quiet=True, threads=6)

    def run(self):
        self.bot.log.info(f'{self.__name__}: runninf page!')
        thread_run(self.serve)

    @Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f'{self.__name__}: started!')

chn_log.info('ready')

if __name__ == '__main__':
    bot = dummy_bot()
    web = web_cog(bot, import_name=__name__,template_folder='./webpage', static_folder = './webpage')
    bot.run_wsv()