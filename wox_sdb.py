import codecs, json
from Gaia import Wox_log, error_form
from colorama import Fore

wdb_log = Wox_log('WoxSDB', color=Fore.LIGHTGREEN_EX)

database = None

class QuasiDatabase():
    
    def __init__(self) -> None:
        self.__name__ = 'SDB'
        wdb_log.info(f'iniciando [{self.__name__}]...')
        self.reload()
    
    def reload(self):
        wdb_log.info(f'Loading data...')
        try:
            with codecs.open('./wxsdb/gnrl_setups.json', 'r', encoding='utf8') as f:
                self.data = json.loads(f.read())
                self.gnrlstp = dict(self.data)
                self.bots = list(self.data['bots'])
                f.close()
            
            with codecs.open('./wxsdb/userbase.json', 'r', encoding='utf8') as f:
                self.data['users'] = json.loads(f.read())
                f.close()
                
            for entry in self.bots:
                with codecs.open(f'./wxsdb/{entry}_setups.json', 'r', encoding='utf8') as f:
                    self.data['bots'][entry].update(json.loads(f.read()))
                    f.close()

                with codecs.open(f'./wxsdb/{entry}_memberbase.json', 'r', encoding='utf8') as f:
                    self.data['bots'][entry].update({'memberbase':json.loads(f.read())})
                    f.close()
                
                with codecs.open(f'./wxsdb/{entry}_extrabase.json', 'r', encoding='utf8') as f:
                    self.data['bots'][entry].update({'extra':json.loads(f.read())})
                    f.close()

        except Exception as ex:
            wdb_log.error(
                error_form(
                    ex,
                    f"[{self.__name__}] Ignoring exception while loading data",
                    f"An error ocurred while loading WoxPseudoDatabase"
                )
            )
            raise Exception(type(ex).__name__, *ex.args)

    def __setitem__(self, s, i):
        self.data[s] = i
        with codecs.open('./database.json', 'w', encoding='utf8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4, sort_keys=True)
            f.close()

    def __getitem__(self, s):
        if s in self.data:
            return self.data[s]
        else:
            self.data[s] = None
            return None
    
    def save(self):
        wdb_log.info(f'Saving data...')
        try:
            self.bots = list(self.data['bots'])
            with codecs.open('./wxsdb/gnrl_setups.json', 'w', encoding='utf8') as f:
                self.gnrlstp.update({'bots':{b:{} for b in self.bots}})
                json.dump(self.gnrlstp, f, ensure_ascii=False, indent=4, sort_keys=True)
                f.close()
                
            with codecs.open('./wxsdb/userbase.json', 'w', encoding='utf8') as f:
                json.dump(self.data['users'], f, ensure_ascii=False, indent=4, sort_keys=True)
                f.close()

            for entry in self.bots:
                with codecs.open(f'./wxsdb/{entry}_setups.json', 'w', encoding='utf8') as f:
                    json.dump({key:self.data['bots'][entry][key] for key in self.data['bots'][entry] if key not in ('memberbase','extra')}, f, ensure_ascii=False, indent=4, sort_keys=True)
                    f.close()

                with codecs.open(f'./wxsdb/{entry}_memberbase.json', 'w', encoding='utf8') as f:
                    json.dump(self.data['bots'][entry]['memberbase'], f, ensure_ascii=False, indent=4, sort_keys=True)
                    f.close()
                
                with codecs.open(f'./wxsdb/{entry}_extrabase.json', 'w', encoding='utf8') as f:
                    json.dump(self.data['bots'][entry]['extra'], f, ensure_ascii=False, indent=4, sort_keys=True)
                    f.close()

        except Exception as ex:
            wdb_log.error(
                error_form(
                    ex,
                    f"[{self.__name__}] Ignoring exception while loading data",
                    f"An error ocurred while loading WoxPseudoDatabase"
                )
            )
            raise Exception(type(ex).__name__, *ex.args)
        
        with codecs.open('./database.json', 'w', encoding='utf8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4, sort_keys=True)
            f.close()

db = QuasiDatabase()
wdb_log.info('ready')