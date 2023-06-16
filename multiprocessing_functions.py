#verified context and no warnings.
import requests
import ssl
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

#ext
from multiprocessing import Process, Value
from pyMeow import open_process, get_module
from pyMeow import r_uint64, r_int
from time import sleep
from json import load
from gc import collect as del_mem

#own
from spaceglider import spaceglider
from autosmite import autosmite
from drawings import drawings
from data import Data, Offsets
from manager import ReadManager
from stats import Stats
from utils import is_active_window
from settings import jsonGetter

class MultiprocessingFunctions:

    def __init__(self, manager):

        #pointers
        self.champion_pointers = manager.list()
        self.minion_pointers = manager.list()
        self.jungle_pointers = manager.list()

        #json settings
        self.spaceglider_settings = manager.dict()
        self.autosmite_settings = manager.dict()
        self.drawings_settings = manager.dict()

        #terminate 
        self.updater_terminate = Value('i', 0)
        self.spaceglider_terminate = Value('i', 0)
        self.autosmite_terminate = Value('i', 0)
        self.drawings_terminate = Value('i', 0)
        self.on_window = Value('i', 0)


    def updater(self):
        """
        This will continuously update and share all the pointers and settings that each process needs.
        """

        minion_names = {
            "SRU_OrderMinionRanged", "SRU_ChaosMinionRanged", "SRU_ChaosMinionMelee", "SRU_OrderMinionMelee", 
            "SRU_OrderMinionSuper", "SRU_ChaosMinionSuper", "SRU_ChaosMinionSiege", "SRU_OrderMinionSiege",
            "HA_OrderMinionRanged", "HA_ChaosMinionRanged", "HA_ChaosMinionMelee", "HA_OrderMinionMelee", 
            "HA_OrderMinionSuper", "HA_ChaosMinionSuper", "HA_ChaosMinionSiege", "HA_OrderMinionSiege"}
        
        jungle_names = [
            "sru_dragon_air",
            "sru_dragon_chemtech",
            "sru_dragon_earth",
            "sru_dragon_elder",
            "sru_dragon_fire",
            "sru_dragon_hextech",
            "sru_dragon_water",
            "sru_riftherald",
            "sru_baron",
            "sru_riftherald_mercenary_tx_cm",
            "sru_red",
            "sru_blue",
            "sru_crab"
        ]
        
        while not self.updater_terminate.value:
            del_mem()
            try:
                name_exec = Data.game_name_executable
                process = open_process(process=name_exec)
                base_address = get_module(process, name_exec)['base']
                local_player = r_uint64(process, base_address + Offsets.local_player)
                local_team = r_int(process, local_player + Offsets.obj_team)
                read_pointers = ReadManager(process, base_address)
                stats = Stats()

            except:
                sleep(1)
            else:
                try:
                    while True:
                        if is_active_window():
                            self.on_window.value = 1
                        else:
                            self.on_window.value = 0

                        if not self.autosmite_terminate.value:
                            if not jsonGetter().get_data('randb'):
                                entities = jungle_names[:-3]
                            else:
                                entities = jungle_names
                            self.jungle_pointers[:] = read_pointers.get_jungle_pointers(entities)

                        if not self.spaceglider_terminate.value or not self.drawings_terminate.value:
                            self.champion_pointers[:] = read_pointers.get_pointers(stats.names, local_team)
                            self.minion_pointers[:] = read_pointers.get_minion_pointers(minion_names, local_team)

                        self.update_settings()

                        sleep(.1)
                except:
                    self.on_window.value = 0

    def update_settings(self):
        with open(Data.settings_file_name, 'r+') as json_file:
            settings = load(json_file)

            for k, v in settings['Spaceglider'].items():
                self.spaceglider_settings[k] = v

            for k, v in settings['Drawings'].items():
                self.drawings_settings[k] = v

            for k, v in settings['AutoSmite'].items():
                self.autosmite_settings[k] = v

    def start_spaceglider_process(self, _, data):
        if data:
            self.spaceglider_terminate.value = 0
            process = Process(target=spaceglider, args=(
                self.spaceglider_terminate,
                self.spaceglider_settings,
                self.champion_pointers,
                self.minion_pointers,
                self.on_window
            ))
            process.start()
        else:
            self.spaceglider_terminate.value = 1

    def start_autosmite_process(self, _, data):
        if data:
            self.autosmite_terminate.value = 0
            process = Process(target=autosmite, args=(
                self.autosmite_terminate,
                self.autosmite_settings,
                self.jungle_pointers,
                self.on_window
            ))
            process.start()
        else:
            self.autosmite_terminate.value = 1

    def start_drawings_process(self, _, data):
        if data:
            self.drawings_terminate.value = 0
            process = Process(target=drawings, args=(
                self.drawings_terminate,
                self.drawings_settings,
                self.champion_pointers,
                self.on_window
            ))
            process.start()
        else:
            self.drawings_terminate.value = 1

