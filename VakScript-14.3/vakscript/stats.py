#built-in
from urllib.request import urlopen
from functools import lru_cache
from time import sleep

#ext
from orjson import loads
from requests import get

#own
from data import Info
from utils import debug_info

"""
TODO:
    - Update default windup modifier.
    - Add stats if its needed.
"""

class Stats:
    def __init__(self):
        while True:
            try:
                stats = loads(urlopen(Info.url_allgamedata).read())
                self.names = [champion['rawChampionName'].removeprefix('game_character_displayname_').lower() for champion in stats['allPlayers']]
                self.champion_data = dict()
                for name in self.names:
                    champion_response = get(Info.url_comunitydragon.format(name=name)).json()
                    self.champion_data[name] = {k.lower(): v for k, v in champion_response.items()}
                break
            except Exception as stats_loop:
                debug_info(stats_loop, True)
                sleep(0.1)

    @lru_cache(maxsize=None)
    def get_attack_speed(self, name):
        name = name.lower()
        root_key = 'characters/{}/characterrecords/root'.format(name)
        base_as = self.champion_data[name][root_key]['attackSpeed']
        return base_as
    
    @lru_cache(maxsize=None)
    def get_radius(self, name):
        name = name.lower()
        try:
            root_key = 'characters/{}/characterrecords/root'.format(name)
            return self.champion_data[name][root_key].get('overrideGameplayCollisionRadius', 65.0)
        except:
            return 65.0
    
    @lru_cache(maxsize=None)
    def get_windup(self, name):
        name = name.lower()
        root_key = 'characters/{}/characterrecords/root'.format(name)
        basic_attack = self.champion_data[name][root_key]['basicAttack']
        windup = 0.3
        windup_mod = 0.
        if 'mAttackDelayCastOffsetPercent' in basic_attack:
            windup = basic_attack['mAttackDelayCastOffsetPercent'] + 0.3
        if 'mAttackDelayCastOffsetPercentAttackSpeedRatio' in basic_attack:
            windup_mod = basic_attack['mAttackDelayCastOffsetPercentAttackSpeedRatio']
        return windup, windup_mod
    
    def get_targets_radius(self):
        champions_radius = dict()
        for name in self.names:
            radius = self.get_radius(name)
            champions_radius[name.capitalize()] = radius
        return champions_radius
    
