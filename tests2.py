



class Persona():
    def __init__(self, nombre, edad) -> None:
        self.nombre = nombre
        self.edad = edad
        pass

    def saludar(self):
        print(f'hola mi nombre es {self.nombre}')


class Trabajador(Persona):
    def __init__(self, nombre, edad, trabajo) -> None:
        super().__init__(nombre, edad)
        self.trabajo = trabajo

    def trabajos(self):
        print(f'Hola, soy {self.nombre} y trabajo en {self.trabajo}')


raul = Persona('raul', '21')
poncho = Persona('poncho', '13')

laura = Trabajador('laura', '24', 'florista')

laura.saludar()
laura.trabajos()


@client.command()
@user_auth(100)
async def dbcharge(ctx):
    if ctx.author.id in {312807184927031306}:

        members = client.guild.members

        embed = embed_builder(
            **{
                'title':'Recreando base de datos',
                'description':'fabricando base de datos desde 0 a partir de los miembros de la guild',
                'color':ctx.author.color,
                'footer':"",
                #'img':"attachment://banner.png",
                'thumb':ctx.author.avatar.url,
                'fields':[
                    {'name':'miembros', 'value':len(members), 'inline':True},
                    {'name':'solicitante', 'value':ctx.author.name, 'inline':True}
                ]
            }
        )

        await ctx.reply(embed=embed)

        temp = {}

        for i, mem in enumerate(members):
            
            if mem.id not in db['bots'][parameters.guild_id]['memberbase']:

                temp[mem.id] = {
                        "number":i,
                        "level":1,
                        "xp":0,
                        "nxtlvl":200,
                        "ranking":0
                }
            
            else:
                temp[mem.id] = db['bots'][parameters.guild_id]['memberbase'][mem.id]
        
        db['bots'][parameters.guild_id]["memberbase"] = temp

        db.save()
        
        await ctx.reply(file=discord.File('./database.json'))
    
    else:
        await ctx.reply("No tienes permiso para usar el comando! :)")






    @slash_command()
    async def getinfo(self, ctx, *args):
        print(args)
        search = None
        if args:
            search = args[0]
        if user_auth(ctx) < 1:
            await ctx.reply('No tienes permiso para usar ese comando')
            return

        await ctx.message.add_reaction(em_check)
        print(search)
        #mcuser = get_user(ctx, search)
        mcuser = False
        print(mcuser)
        if not mcuser:
            await ctx.reply('No pude encontrar al usuario .-.')
            return

        dcmem = ctx.guild.get_member(mcuser['dcid'])

        incid = ['El jugador', '', '']

        if dcmem:
            if self.bot.rol_strike1 in dcmem.roles:
                incid[1] = 'tiene 2 strikes y'
            elif self.bot.rol_strike2 in dcmem.roles:
                incid[1] = 'tiene 1 strike y'
            else:
                incid[1] = 'no tiene strikes,'

            if self.bot.rol_ban1 in dcmem.roles:
                incid[2] = 'tiene 2 bans'
            elif self.bot.rol_ban2 in dcmem.roles:
                incid[2] = 'tiene 1 ban'
            else:
                incid[2] = 'no tiene bans'
            incidents = ' '.join(map(str, incid))
        else:
            incidents = 'No se pudo acceder a la informacion del miembro'
        
        banner = discord.File(await user_banner(ctx, dcmem.id), filename="banner.png")
        embed = embed_builder(
            **{
                'title':'Informacion del jugador',
                'description':f'{dcmem.mention}',
                'color':dcmem.color,
                'footer':f"Jugador numero{mcuser['number']}: {dcmem.name}{dcmem.discriminator}, {mcuser['name']}",
                'img':"attachment://banner.png",
                'thumb':dcmem.avatar_url,
                'fields':[
                    {'name':'Nick', 'value':mcuser['name'], 'inline':True},
                    {'name':'Nombre', 'value':(dcmem.name if dcmem.name else mcuser['dcname']), 'inline':True},
                    {'name':'Discord', 'value':(dcmem.mention if dcmem.mention else None), 'inline':True},
                    {'name':'MC UUID', 'value':mcuser['uuid'], 'inline':True},
                    {'name':'Apodo', 'value':(dcmem.name if dcmem.name else "No tiene"), 'inline':True},
                    {'name':'DC ID', 'value':dcmem.id, 'inline':True},

                    {'name':'Incidentes', 'value':incidents, 'inline':True}
                ]
            }
        )
        await ctx.reply(file=banner, embed=embed)


class A :
    def Decorators(func) :
        def inner(self) :
            print('Decoration started.')
            func(self)
            print('Decoration of function completed.\n')
        return inner
  
    @Decorators
    def fun1(self) :
        print('Decorating - Class A methods.')
  
# creating class B
class B(A) :
    @A.Decorators
    def fun2(self) :
        print('Decoration - Class B methods.')



class WoxCog(Cog):
    def cog_auth(lvl_required):
        """user_auth method for use inside subclass"""
        async def predicate(self, ctx):
            print(lvl_required)
            if ctx.guild is None:
                raise NoPrivateMessage()
            return self.bot.get_user_auth(ctx) >= lvl_required
        return check(predicate)

class general_commands(WoxCog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__name__ = '[general_commands cog]'
        sat_log.info(f'starting {self.__name__}...')
    
    @command()
    @WoxCog.cog_auth(5)
    async def test(self, ctx):
        await ctx.reply("a")
    
    @slash_command()
    @WoxCog.cog_auth(5)
    async def stest(self, ctx):
        await ctx.respond("a")


@command()
    @user_auth(10)
    async def test(self, ctx):
        user_list = [
            365717450404134914
        ]
        for id in user_list:
            user = self.bot.get_user(id)
            print(type(user), id)
            try:
                await user.send(";)")
            except Exception as ex:
                print(type(user), id, type(ex).__name__)
    
    @command()
    @user_auth(10)
    async def send(self, ctx):
        user_list = [
            365717450404134914
        ]
        for id in user_list:
            user = self.bot.get_user(id)
            embed = embed_builder(**{
                "title":"**Herramientas** y **Estrategias** para **Plataformas Digitales**",
                "description":"[El dia de hoy es nuestra conferencia sobre Estrategias y metodos de expansion donde hablaremos sobre como aprobechar las distintas plataformas y las herramientas que estas nos aportan al maximo.](https://discord.com/events/604593971829800990/1040605828991946793)",
                "color":color("dark_purple"),
                "footer":"***Evento para streamers y moderadores***",
                "ficon":"https://i.postimg.cc/2SM9kp2W/mugn1-bg.png",
                "img":"https://media.discordapp.net/attachments/1040863983483236433/1041110928294424756/Sin_titulo-1.png",
                "thumb":"https://media.discordapp.net/attachments/1013311080350629928/1027385804168904804/Sin_titulo-1.jpg?width=453&height=453",
                "fields":[
                    {"name":"Temas", "value":"*Configuracion de Twitch\nDrops y Recompenzas\nExtensiones e Integraciones de Twitch\nIntegracion de Twitch a Discord\nConfiguracion de Discord\nConexiones e Integraciones de Discord\n Y mas...*", "inline":False},
                    {"name":"Presentadores","value":"*AlejandroGMusic\nFelixBluWox*", "inline":True},
                    {"name":"Fecha","value":"***Domingo 13\nde noviembre (HOY)***", "inline":True},
                    {"name":"Servidor","value":"[**AlejandroGMusic**](https://discord.gg/YjMDKdE5)", "inline":True},
                    {"name":"Hora","value":"Horarios en las diferentes regiones", "inline":False},
                    {"name":"CDMX", "value":"***9:00 PM***", "inline":True},
                    {"name":"Cancun", "value":"***10:00 PM***", "inline":True},
                    {"name":"Sonora", "value":"***8:00 PM***", "inline":True},
                    {"name":"Chile", "value":"***12:00 PM***", "inline":True},
                    {"name":"Colombia", "value":"***10:00 PM***", "inline":True},
                    {"name":"Argentina", "value":"***12:00 PM***", "inline":True}
                ]
            })
            await user.send("**Mu Games** ***Presenta...***", embed=embed)
            await user.send("*nota: la conferencia es offline, solo se dara en el server de discord, no hace falta iniciar stream <3\n\nsi no estas en el server de discord, entra (dandole click a donde dice \"servidor\") para que te demos el rol y puedas entrar :D\n\natt: FelixBluWox :D*")
        enviados = ','.join(map(str, [f'<@{i}>' for i in user_list]))
        await ctx.reply(f"se enviaron los mensajes :D a {enviados}")