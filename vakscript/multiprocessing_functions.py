#built-in
import ssl
from multiprocessing import Process, Value
from time import sleep
from json import load
from gc import collect as del_mem

#ext
import requests
from pyMeow import open_process, get_module, r_uint64, r_int

#own
from spaceglider import spaceglider
from drawings import drawings
from autosmite import autosmite
from data import Info, Offsets
from read_manager import ListReader
from stats import Stats
from utils import is_active_window, debug_info
from scripts_manager import execute_scripts

"""
TODO:
    - Optimize wards reading.
"""

requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context


MINION_NAMES = [
    'ha_orderminionsuper', 'ha_orderminionranged', 'ha_chaosminionsuper', 'sru_orderminionsuper', 
    'ha_orderminionsiege', 'ha_chaosminionmelee', 'sru_chaosminionmelee', 'sru_chaosminionsiege', 
    'sru_orderminionranged', 'sru_orderminionsiege', 'ha_chaosminionsiege', 'ha_chaosminionranged', 
    'ha_orderminionmelee', 'sru_chaosminionsuper', 'sru_chaosminionranged', 'sru_orderminionmelee'
]

JUNGLE_NAMES = [
        'sru_dragon_air', 'sru_dragon_chemtech', 'sru_dragon_earth', 'sru_dragon_elder',
        'sru_dragon_fire', 'sru_dragon_hextech', 'sru_dragon_water', 'sru_riftherald',
        'sru_baron', 'sru_riftherald_mercenary_tx_cm', 'sru_red', 'sru_blue', 'sru_crab'
]

class MultiprocessingFunctions:
    
    def __init__(self, manager):
        #pointers
        self.champion_pointers = manager.list()
        self.minion_pointers = manager.list()
        self.jungle_pointers = manager.list()
        self.ward_pointers = manager.list()
        self.turret_pointers = manager.list()

        #json settings
        self.spaceglider_settings = manager.dict()
        self.autosmite_settings = manager.dict()
        self.drawings_settings = manager.dict()

        #terminate
        self.updater_terminate = Value('i', 0)
        self.spaceglider_terminate = Value('i', 0)
        self.autosmite_terminate = Value('i', 0)
        self.drawings_terminate = Value('i', 0)
        self.scripts_terminate = Value('i', 0)
        self.on_window = Value('i', 0)

        #entities names
        self.minion_names = MINION_NAMES
        self.jungle_names = JUNGLE_NAMES
    

    def updater(self) -> None:
        """
        This function will continuosly update and share all the pointers and settings that each process needs.
        """


        while not self.updater_terminate.value:
            del_mem()
            try:
                name_exec = Info.game_name_executable
                process = open_process(process=name_exec)
                base_address = get_module(process, name_exec)['base']
                local_player = r_uint64(process, base_address + Offsets.local_player)
                local_team = r_int(process, local_player + Offsets.obj_team)
                read_pointers = ListReader(process, base_address, local_team)
                stats = Stats()
            except Exception as updater_proc_loop:
                debug_info(updater_proc_loop, True)
                sleep(0.1)
            else:
                try:
                    while True:
                        
                        if is_active_window():
                            self.on_window.value = 1
                            self.update_settings()

                            if not self.spaceglider_terminate.value or not self.drawings_terminate.value:
                                self.champion_pointers[:] = read_pointers.get_pointers(Offsets.champion_list, stats.names, size=128, search_mode=0)
                                self.minion_pointers[:] = read_pointers.get_pointers(Offsets.minion_list, size=512, search_mode=1)
                                self.ward_pointers[:] = read_pointers.get_pointers(Offsets.minion_list, size=512, search_mode=3)
                                self.turret_pointers[:] = read_pointers.get_pointers(Offsets.turret_list, size=64, search_mode=2)

                            if not self.autosmite_terminate.value:
                                if not self.autosmite_settings['randb']:
                                    jg_names = self.jungle_names[:-3]
                                else:
                                    jg_names = self.jungle_names
                                self.jungle_pointers[:] = read_pointers.get_pointers(Offsets.minion_list, jg_names, size=512, search_mode=0)
                        else:
                            self.on_window.value = 0

                        sleep(0.1)

                except Exception as updater_loop:
                    debug_info(updater_loop, True)
                    self.on_window.value = 0

    def update_settings(self) -> None:
        with open(Info.settings_file_name, 'r+') as json_file:
            settings = load(json_file)

            if not self.spaceglider_terminate.value:
                for k, v in settings['Spaceglider'].items():
                    self.spaceglider_settings[k] = v

            if not self.drawings_terminate.value:
                for k, v in settings['Drawings'].items():
                    self.drawings_settings[k] = v
                    
            if not self.autosmite_terminate.value:
                for k, v in settings['AutoSmite'].items():
                    self.autosmite_settings[k] = v


    def start_spaceglider_process(self, _, state) -> None:
        if state:
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


    def start_autosmite_process(self, _, state) -> None:
        if state:
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


    def start_drawings_process(self, _, state) -> None:
        if state:
            self.drawings_terminate.value = 0
            process = Process(target=drawings, args=(
                self.drawings_terminate,
                self.drawings_settings,
                self.champion_pointers,
                self.ward_pointers,
                self.turret_pointers,
                self.on_window
            ))
            process.start()
        else:
            self.drawings_terminate.value = 1
    

    def start_scripts_process(self, _, state, user_data) -> None:
        if state:
            self.scripts_terminate.value = 0
            process = Process(target=execute_scripts, args=(
                self.scripts_terminate,
                user_data,
                self.champion_pointers,
                self.ward_pointers,
                self.minion_pointers,
                self.turret_pointers,
                self.on_window
            ))
            process.start()
        else:
            self.scripts_terminate.value = 1