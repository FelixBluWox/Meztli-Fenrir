#                        Felix Blu Wox (c) 2022
#  This file is part of the WoxFenrir framework for creating Discord bots

from os import getenv
from dotenv import load_dotenv
from traceback import format_exception
from colorama import Style, Fore, Back, init
import logging, sys, codecs, json, requests
from functools import lru_cache as cache
init()


#loading important files...
load_dotenv("./secret.env")

with codecs.open('./wxsdb/gnrl_setups.json', 'r', encoding='utf8') as f:
    setups = json.loads(f.read())



#getting bot tokens
qztl_token = getenv("quetzalcoatl_token")
bots = {k:getenv(f"{k.lower()}_token") for k in setups["clients"]}

#getting bot join urls
urls = {k:getenv(f"{k.lower()}_url") for k in setups["clients"]}

#the root users discord id (returns auth level 100 in every @user_auth call)
root_usr = int(getenv("wox_devel"))

#CREDENTIALS
#spotify
spotify_id = getenv("spotify_id")
spotify_secret = getenv("spotify_secret")

#twitch
twitch_id = getenv("twitch_id")
twitch_secret = getenv("twitch_secret")

#discord
discord_id = getenv("discord_id")
discord_secret = getenv("discord_secret")

#OAuth2 stuff
ttv_oidc_cfg = requests.get("https://id.twitch.tv/oauth2/.well-known/openid-configuration").json()
dcr_oidc_cfg = {   
    "authorization_endpoint":"https://discord.com/api/oauth2/authorize",
    "token_endpoint":"https://discord.com/api/oauth2/token",
    "userinfo_endpoint":"https://discord.com/api/users/@me"
}



@cache
def anti_utf8(expected_string):
    if type(expected_string) is not str:
        return expected_string
    true_abc = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    utf8_abc = ('𝐚','𝐛','𝐜','𝐝','𝐞','𝐟','𝐠','𝐡','𝐢','𝐣','𝐤','𝐥','𝐦','𝐧','𝐧̃','𝐨','𝐩','𝐪','𝐫','𝐬','𝐭','𝐮','𝐯','𝐰','𝐱','𝐲','𝐳','𝐀','𝐁','𝐂','𝐃','𝐄','𝐅','𝐆','𝐇','𝐈','𝐉','𝐊','𝐋','𝐌','𝐍','𝐍̃','𝐎','𝐏','𝐐','𝐑','𝐒','𝐓','𝐔','𝐕','𝐖','𝐗','𝐘','𝐙','ɐ','q','ɔ','p','ǝ','ɟ','ƃ','ɥ','ı̣','ɾ̣','ʞ','ן','ɯ','u','ũ','o','d','b','ɹ','s','ʇ','n','ʌ','ʍ','x','ʎ','z','Ɐ','ꓭ','Ɔ','ꓷ','Ǝ','Ⅎ','ꓨ','H','I','ſ','ꓘ','ꓶ','W','N','Ñ','O','Ԁ','Ò','ꓤ','S','ꓕ','ꓵ','ꓥ','M','X','⅄','Z','𝓪','𝓫','𝓬','𝓭','𝓮','𝓯','𝓰','𝓱','𝓲','𝓳','𝓴','𝓵','𝓶','𝓷','𝓷̃','𝓸','𝓹','𝓺','𝓻','𝓼','𝓽','𝓾','𝓿','𝔀','𝔁','𝔂','𝔃','𝓐','𝓑','𝓒','𝓓','𝓔','𝓕','𝓖','𝓗','𝓘','𝓙','𝓚','𝓛','𝓜','𝓝','𝓝̃','𝓞','𝓟','𝓠','𝓡','𝓢','𝓣','𝓤','𝓥','𝓦','𝓧','𝓨','𝓩','𝙖','𝙗','𝙘','𝙙','𝙚','𝙛','𝙜','𝙝','𝙞','𝙟','𝙠','𝙡','𝙢','𝙣','𝙣̃','𝙤','𝙥','𝙦','𝙧','𝙨','𝙩','𝙪','𝙫','𝙬','𝙭','𝙮','𝙯','𝘼','𝘽','𝘾','𝘿','𝙀','𝙁','𝙂','𝙃','𝙄','𝙅','𝙆','𝙇','𝙈','𝙉','𝙉̃','𝙊','𝙋','𝙌','𝙍','𝙎','𝙏','𝙐','𝙑','𝙒','𝙓','𝙔','𝙕','🅐','🅑','🅒','🅓','🅔','🅕','🅖','🅗','🅘','🅙','🅚','🅛','🅜','🅝','🅝̃','🅞','🅟','🅠','🅡','🅢','🅣','🅤','🅥','🅦','🅧','🅨','🅩','🅐','🅑','🅒','🅓','🅔','🅕','🅖','🅗','🅘','🅙','🅚','🅛','🅜','🅝','🅝̃','🅞','🅟','🅠','🅡','🅢','🅣','🅤','🅥','🅦','🅧','🅨','🅩','𝕒','𝕓','𝕔','𝕕','𝕖','𝕗','𝕘','𝕙','𝕚','𝕛','𝕜','𝕝','𝕞','𝕟','𝕟̃','𝕠','𝕡','𝕢','𝕣','𝕤','𝕥','𝕦','𝕧','𝕨','𝕩','𝕪','𝕫','𝔸','𝔹','ℂ','𝔻','𝔼','𝔽','𝔾','ℍ','𝕀','𝕁','𝕂','𝕃','𝕄','ℕ','ℕ̃','𝕆','ℙ','ℚ','ℝ','𝕊','𝕋','𝕌','𝕍','𝕎','𝕏','𝕐','ℤ','ᴀ','ʙ','ᴄ','ᴅ','ᴇ','ғ','ɢ','ʜ','ɪ','ᴊ','ᴋ','ʟ','ᴍ','ɴ','ɴ̃','ᴏ','ᴘ','ǫ','ʀ','s','ᴛ','ᴜ','ᴠ','ᴡ','x','ʏ','ᴢ','ᴀ','ʙ','ᴄ','ᴅ','ᴇ','ғ','ɢ','ʜ','ɪ','ᴊ','ᴋ','ʟ','ᴍ','ɴ','ɴ̃','ᴏ','ᴘ','ǫ','ʀ','s','ᴛ','ᴜ','ᴠ','ᴡ','x','ʏ','ᴢ','𝖆','𝖇','𝖈','𝖉','𝖊','𝖋','𝖌','𝖍','𝖎','𝖏','𝖐','𝖑','𝖒','𝖓','𝖓̃','𝖔','𝖕','𝖖','𝖗','𝖘','𝖙','𝖚','𝖛','𝖜','𝖝','𝖞','𝖟','𝕬','𝕭','𝕮','𝕯','𝕰','𝕱','𝕲','𝕳','𝕴','𝕵','𝕶','𝕷','𝕸','𝕹','𝕹̃','𝕺','𝕻','𝕼','𝕽','𝕾','𝕿','𝖀','𝖁','𝖂','𝖃','𝖄','𝖅','🅰','🅱','🅲','🅳','🅴','🅵','🅶','🅷','🅸','🅹','🅺','🅻','🅼','🅽','🅽̃','🅾','🅿','🆀','🆁','🆂','🆃','🆄','🆅','🆆','🆇','🆈','🆉','🅰','🅱','🅲','🅳','🅴','🅵','🅶','🅷','🅸','🅹','🅺','🅻','🅼','🅽','🅽̃','🅾','🅿','🆀','🆁','🆂','🆃','🆄','🆅','🆆','🆇','🆈','🆉','𝖺','𝖻','𝖼','𝖽','𝖾','𝖿','𝗀','𝗁','𝗂','𝗃','𝗄','𝗅','𝗆','𝗇','𝗇̃','𝗈','𝗉','𝗊','𝗋','𝗌','𝗍','𝗎','𝗏','𝗐','𝗑','𝗒','𝗓','𝖠','𝖡','𝖢','𝖣','𝖤','𝖥','𝖦','𝖧','𝖨','𝖩','𝖪','𝖫','𝖬','𝖭','𝖭̃','𝖮','𝖯','𝖰','𝖱','𝖲','𝖳','𝖴','𝖵','𝖶','𝖷','𝖸','𝖹','𝘢','𝘣','𝘤','𝘥','𝘦','𝘧','𝘨','𝘩','𝘪','𝘫','𝘬','𝘭','𝘮','𝘯','𝘯̃','𝘰','𝘱','𝘲','𝘳','𝘴','𝘵','𝘶','𝘷','𝘸','𝘹','𝘺','𝘻','𝘈','𝘉','𝘊','𝘋','𝘌','𝘍','𝘎','𝘏','𝘐','𝘑','𝘒','𝘓','𝘔','𝘕','𝘕̃','𝘖','𝘗','𝘘','𝘙','𝘚','𝘛','𝘜','𝘝','𝘞','𝘟','𝘠','𝘡','𝑎','𝑏','𝑐','𝑑','𝑒','𝑓','𝑔','ℎ','𝑖','𝑗','𝑘','𝑙','𝑚','𝑛','𝑛̃','𝑜','𝑝','𝑞','𝑟','𝑠','𝑡','𝑢','𝑣','𝑤','𝑥','𝑦','𝑧','𝐴','𝐵','𝐶','𝐷','𝐸','𝐹','𝐺','𝐻','𝐼','𝐽','𝐾','𝐿','𝑀','𝑁','𝑁̃','𝑂','𝑃','𝑄','𝑅','𝑆','𝑇','𝑈','𝑉','𝑊','𝑋','𝑌','𝑍','𝒂','𝒃','𝒄','𝒅','𝒆','𝒇','𝒈','𝒉','𝒊','𝒋','𝒌','𝒍','𝒎','𝒏','𝒏̃','𝒐','𝒑','𝒒','𝒓','𝒔','𝒕','𝒖','𝒗','𝒘','𝒙','𝒚','𝒛','𝑨','𝑩','𝑪','𝑫','𝑬','𝑭','𝑮','𝑯','𝑰','𝑱','𝑲','𝑳','𝑴','𝑵','𝑵̃','𝑶','𝑷','𝑸','𝑹','𝑺','𝑻','𝑼','𝑽','𝑾','𝑿','𝒀','𝒁','𝗮','𝗯','𝗰','𝗱','𝗲','𝗳','𝗴','𝗵','𝗶','𝗷','𝗸','𝗹','𝗺','𝗻','𝗻̃','𝗼','𝗽','𝗾','𝗿','𝘀','𝘁','𝘂','𝘃','𝘄','𝘅','𝘆','𝘇','𝗔','𝗕','𝗖','𝗗','𝗘','𝗙','𝗚','𝗛','𝗜','𝗝','𝗞','𝗟','𝗠','𝗡','𝗡̃','𝗢','𝗣','𝗤','𝗥','𝗦','𝗧','𝗨','𝗩','𝗪','𝗫','𝗬','𝗭','𝚊','𝚋','𝚌','𝚍','𝚎','𝚏','𝚐','𝚑','𝚒','𝚓','𝚔','𝚕','𝚖','𝚗','𝚗̃','𝚘','𝚙','𝚚','𝚛','𝚜','𝚝','𝚞','𝚟','𝚠','𝚡','𝚢','𝚣','𝙰','𝙱','𝙲','𝙳','𝙴','𝙵','𝙶','𝙷','𝙸','F','𝙺','𝙻','𝙼','𝙽','𝙽̃','𝙾','𝙿','𝚀','𝚁','𝚂','𝚃','𝚄','𝚅','𝚆','𝚇','𝚈','𝚉','𝔞','𝔟','𝔠','𝔡','𝔢','𝔣','𝔤','𝔥','𝔦','𝔧','𝔨','𝔩','𝔪','𝔫','𝔫̃','𝔬','𝔭','𝔮','𝔯','𝔰','𝔱','𝔲','𝔳','𝔴','𝔵','𝔶','𝔷','𝔄','𝔅','ℭ','𝔇','𝔈','𝔉','𝔊','ℌ','ℑ','𝔍','𝔎','𝔏','𝔐','𝔑','𝔑̃','𝔒','𝔓','𝔔','ℜ','𝔖','𝔗','𝔘','𝔙','𝔚','𝔛','𝔜','ℨ','𝒶','𝒷','𝒸','𝒹','ℯ','𝒻','ℊ','𝒽','𝒾','𝒿','𝓀','𝓁','𝓂','𝓃','𝓃̃','ℴ','𝓅','𝓆','𝓇','𝓈','𝓉','𝓊','𝓋','𝓌','𝓍','𝓎','𝓏','𝒜','ℬ','𝒞','𝒟','ℰ','ℱ','𝒢','ℋ','ℐ','𝒥','𝒦','ℒ','ℳ','𝒩','𝒩̃','𝒪','𝒫','𝒬','ℛ','𝒮','𝒯','𝒰','𝒱','𝒲','𝒳','𝒴','𝒵')
    diacritics = ('á','é','í','ó','ú','Á','É','Í','Ó','Ú','à','è','ì','ò','ù','À','È','Ì','Ò','Ù','ä','ë','ï','ö','ü','Ä','Ë','Ï','Ö','Ü')
    vocals = ('a','e','i','o','u','A','E','I','O','U')
    str_buffer = ()
    for c in expected_string:
        if c in true_abc:
            str_buffer += (c,)
        elif c in {'0','1','2','3','4','5','6','7','8','9',' ','<','>','!','"','·','#','$','%','&','/','(',')','=','?','¿','¡','\'','{','}','[',']','+','-','_','.',',',':',';','*'}:
            str_buffer += (c,)
        elif c in diacritics:
            n = diacritics.index(c)
            n = n - (10 * int(n/10)) if n >= 10 else n
            str_buffer += (vocals[n],)
        elif c in utf8_abc:
            n = utf8_abc.index(c)
            n = n - (54 * int(n/54)) if n >= 26 else n
            str_buffer += (true_abc[n],)

    return ''.join(str_buffer)


def error_form(error, title="Oh no, something happend", info=None):
    traceback = "Error:\n" + '\n'.join(map(str, format_exception(type(error), error, error.__traceback__)))
    details = '\n'.join(map(str, error.args))
    message = f"""{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT}
    {title} Error: {type(error).__name__}\t{Back.RESET}{Fore.LIGHTYELLOW_EX}

    {info}
    
    {type(error).__name__} Details: \n{details}

    TRACEBACK:{Fore.RESET}{Style.NORMAL}{Fore.YELLOW}
    
    {traceback}{Style.RESET_ALL}
    """
    return message



formatter = logging.Formatter('[%(levelname)s][%(name)s]: %(message)s')

stdout_info_handler = logging.StreamHandler(sys.stdout)
stdout_info_handler.setLevel(logging.INFO)
stdout_info_handler.setFormatter(formatter)

stdout_warn_handler = logging.StreamHandler(sys.stdout)
stdout_warn_handler.setLevel(logging.WARN)
stdout_warn_handler.setFormatter(formatter)

file_debug_handler = logging.FileHandler(filename='./logs/debug.log', encoding='utf-8', mode='w')
file_debug_handler.setLevel(logging.DEBUG)
file_debug_handler.setFormatter(formatter)

file_info_handler = logging.FileHandler(filename='./logs/info.log', encoding='utf-8', mode='w')
file_info_handler.setLevel(logging.INFO)
file_info_handler.setFormatter(formatter)

file_warn_handler = logging.FileHandler(filename='./logs/warn.log', encoding='utf-8', mode='w')
file_warn_handler.setLevel(logging.WARN)
file_warn_handler.setFormatter(formatter)

class Wox_log(logging.Logger):
    def __init__(self, name, color=None, std_handler=stdout_info_handler, file_handlers=[file_debug_handler, file_info_handler, file_warn_handler]) -> None:
        super().__init__(name)
        self.color = color
        self.setLevel(logging.DEBUG)
        self.addHandler(std_handler)
        for handler in file_handlers:
            self.addHandler(handler)
    
    def debug(self, msg):
        if self.color:
            print(self.color, end ="")
        else:
            print(Fore.MAGENTA, Style.DIM, end ="")
        super().debug(msg)
        print(Style.RESET_ALL, end ="")

    def info(self, msg):
        if self.color:
            print(self.color, end ="")
        super().info(msg)
        print(Style.RESET_ALL, end ="")
    
    def warning(self, msg):
        if self.color:
            print(self.color, end ="")
        else:
            print(Fore.YELLOW, end ="")
        super().warning(msg)
        print(Style.RESET_ALL, end ="")
    
    def critical(self, msg):
        if self.color:
            print(self.color, end ="")
        else:
            print(Fore.LIGHTYELLOW_EX, end ="")
        super().critical(msg)
        print(Style.RESET_ALL, end ="")
    
    def error(self, msg):
        if self.color:
            print(self.color, end ="")
        else:
            print(Fore.LIGHTRED_EX, end ="")
        super().error(msg)
        print(Style.RESET_ALL, end ="")
    
    def exception(self, msg):
        if self.color:
            print(self.color, end ="")
        else:
            print(Fore.LIGHTRED_EX, Style.BRIGHT, end ="")
        super().exception(msg)
        print(Style.RESET_ALL, end ="")
    
    def fwrn(self, error, title="Oh no, something happend", info=None):
        traceback = "Error:\n" + '\n'.join(map(str, format_exception(type(error), error, error.__traceback__)))
        details = '\n'.join(map(str, error.args))
        print(Back.YELLOW, Fore.BLACK, Style.BRIGHT, end ="")
        super().error(f"{title} Error: {type(error).__name__}")
        print(Back.RESET, Fore.LIGHTYELLOW_EX, end ="")
        super().error(f"{info}\n\n{type(error).__name__} Details: \n{details}\n\nTRACEBACK:")
        print(Fore.RESET, Style.NORMAL, Fore.YELLOW, end ="")
        super().error(traceback)
        print(Style.RESET_ALL, end ="")
    
    def ferr(self, error, title="Oh no, something happend", info=None):
        traceback = "Error:\n" + '\n'.join(map(str, format_exception(type(error), error, error.__traceback__)))
        details = '\n'.join(map(str, error.args))
        print(Back.YELLOW, Fore.BLACK, Style.BRIGHT, end ="")
        super().error(f"{title} Error: {type(error).__name__}")
        print(Back.RESET, Fore.YELLOW, end ="")
        super().error(f"{info}\n\n{type(error).__name__} Details: \n{details}\n\nTRACEBACK:")
        print(Fore.RESET, Style.NORMAL, Fore.LIGHTRED_EX, end ="")
        super().error(traceback)
        print(Style.RESET_ALL, end ="")
    
    def fexc(self, error, title="Oh no, something happend", info=None):
        traceback = "Error:\n" + '\n'.join(map(str, format_exception(type(error), error, error.__traceback__)))
        details = '\n'.join(map(str, error.args))
        print(Back.LIGHTRED_EX, Fore.BLACK, Style.BRIGHT, end ="")
        super().critical(f"{title} Error: {type(error).__name__}")
        print(Back.RESET, Fore.LIGHTRED_EX, end ="")
        super().critical(f"{info}\n\n{type(error).__name__} Details: \n{details}\n\nTRACEBACK:")
        print(Fore.RESET, Style.NORMAL, Fore.RED, end ="")
        super().critical(traceback)
        print(Style.RESET_ALL, end ="")


        




