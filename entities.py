#ext
from collections import namedtuple
from pyMeow import r_string, r_float, r_bool, r_int
from math import hypot
from functools import partial

#own
from data import Offsets
from world_to_screen import World

class ReadAttributes:

    def __init__(self, process):
        self.obj_name = Offsets.obj_name
        self.obj_health = Offsets.obj_health
        self.obj_max_health = Offsets.obj_max_health
        self.obj_team = Offsets.obj_team
        self.obj_base_attack = Offsets.obj_base_attack
        self.obj_bonus_attack = Offsets.obj_bonus_attack
        self.obj_magic_damage = Offsets.obj_magic_damage
        self.obj_armor = Offsets.obj_armor
        self.obj_attack_range = Offsets.obj_attack_range
        self.obj_spawn_count = Offsets.obj_spawn_count
        self.obj_targetable = Offsets.obj_targetable
        self.obj_visible = Offsets.obj_visible
        self.obj_x = Offsets.obj_x
        self.obj_y = Offsets.obj_y
        self.obj_z = Offsets.obj_z
        self.process = process 
        self.PlayerNamedtuple = namedtuple('Player', 'name basic_attack bonus_attack x y z attack_range')
        self.EnemyNamedtuple = namedtuple('Enemy', 'name health max_health armor basic_attack bonus_attack magic_damage x y z alive targetable visible attack_range')
        self.MinionNamedtuple = namedtuple('Minion', 'name health armor x y z alive targetable visible')

    
    def read_player(self, local_player):
        d, process = {}, self.process
        d['name'] = r_string(process, local_player + self.obj_name)
        d['basic_attack'] = r_float(process, local_player + self.obj_base_attack)
        d['bonus_attack'] = r_float(process, local_player + self.obj_bonus_attack)
        d['x'] = r_float(process, local_player + self.obj_x)
        d['y'] = r_float(process, local_player + self.obj_y)
        d['z'] = r_float(process, local_player + self.obj_z)
        d['attack_range'] = r_float(process, local_player + self.obj_attack_range)
        return self.PlayerNamedtuple(**d)
    
    def read_enemy(self, pointer):
        d, process = {}, self.process
        d['name'] = r_string(process, pointer + self.obj_name)
        d['health'] = r_float(process, pointer + self.obj_health)
        d['max_health'] = r_float(process, pointer + self.obj_max_health)
        d['armor'] = r_float(process, pointer + self.obj_armor)
        d['basic_attack'] = r_float(process, pointer + self.obj_base_attack)
        d['bonus_attack'] = r_float(process, pointer + self.obj_bonus_attack)
        d['magic_damage'] = r_float(process, pointer + self.obj_magic_damage)
        d['x'] = r_float(process, pointer + self.obj_x)
        d['y'] = r_float(process, pointer + self.obj_y)
        d['z'] = r_float(process, pointer + self.obj_z)
        d['alive'] = r_int(process, pointer + self.obj_spawn_count) % 2 == 0
        d['targetable'] = r_bool(process, pointer + self.obj_targetable)
        d['visible'] = r_bool(process, pointer + self.obj_visible)
        d['attack_range'] = r_float(process, pointer + self.obj_attack_range)
        return self.EnemyNamedtuple(**d)
    
    def read_minion(self, pointer):
        d, process = {}, self.process
        d['name'] = r_string(process, pointer + self.obj_name)
        d['health'] = r_float(process, pointer + self.obj_health)
        d['armor'] = r_float(process, pointer + self.obj_armor)
        d['x'] = r_float(process, pointer + self.obj_x)
        d['y'] = r_float(process, pointer + self.obj_y)
        d['z'] = r_float(process, pointer + self.obj_z)
        d['alive'] = r_int(process, pointer + self.obj_spawn_count) % 2 == 0
        d['targetable'] = r_bool(process, pointer + self.obj_targetable)
        d['visible'] = r_bool(process, pointer + self.obj_visible)
        return self.MinionNamedtuple(**d)
    

#Entity + EntityDrawings
def distance(player, target):
    return hypot(player.x - target.x, player.y - target.y)

def get_effective_damage(damage, armor):
    if armor >= 0:
        return damage * 100. / (100. + armor)
    return damage * (2. - (100. / (100. - armor)))

def get_min_attacks(player, target):
    effective_damage = get_effective_damage(player.basic_attack + player.bonus_attack, target.armor)
    return target.health / effective_damage


class Entity:

    def __init__(self, stats):
        self.stats = stats
        self.radius = self.stats.get_targets_radius()
    
    def in_distance(self, player, target):
        return distance(player, target) - self.radius.get(target.name, 65.) <= player.attack_range + self.radius.get(player.name, 65.)
    
    def in_distance_minion(self, player, target):
        return distance(player, target) - 65.0 <= player.attack_range + self.radius.get(player.name, 65.)
    
    def is_hurtable(self, target):
        return target.alive and target.visible and target.targetable

    def select_by_health(self, player, targets):
        target, min_autos = None, None
        for entity in targets:
            if self.is_hurtable(entity) and self.in_distance(player, entity):
                autos = get_min_attacks(player, entity)
                if target is None or 0 < autos < min_autos:
                    target, min_autos = entity, autos
        return target
    
    def select_by_damage(self, player, targets):
        target, max_damage = None, None
        for entity in targets:
            if self.is_hurtable(entity) and self.in_distance(player, entity):
                damage = max(entity.basic_attack + entity.bonus_attack + entity.attack_range, entity.magic_damage)
                if target is None or damage > max_damage:
                    target, max_damage = entity, damage
        return target
    
    def select_by_distance(self, player, targets):
        target, min_distance = None, None
        for entity in targets:
            if self.is_hurtable(entity) and self.in_distance(player, entity):
                d = distance(player, entity)
                if target is None or d < min_distance:
                    target, min_distance = entity, d
        return target
    
    def select_lowest_minion(self, player, targets):
        target, min_health = None, None
        for entity in targets:
            if self.is_hurtable(entity) and self.in_distance_minion(player, entity):
                if target is None or entity.health < min_health:
                    target, min_health = entity, entity.health
        return target
    
    def select_lasthit_minion(self, player, targets):
        return [target for target in targets if self.in_distance_minion(player, target) and target.health <= get_effective_damage(player.basic_attack + player.bonus_attack, target.armor) and self.is_hurtable(target)]
    

class EntityDrawings:

    def __init__(self, process, base_address, width, height):
        self.world = World(process, base_address, width, height)
        self.world_to_screen = self.world.world_to_screen_limited
        self.get_view_proj_matrix = self.world.get_view_proj_matrix
    
    def _has_pos(self, target):
        return self.world_to_screen(self.get_view_proj_matrix(), target.x, target.z, target.y) and target.alive and target.targetable and target.visible

    @staticmethod
    def min_attacks(player, target):
        return get_min_attacks(player, target)
    
    @staticmethod
    def max_damage(target):
        return max(target.basic_attack + target.bonus_attack, target.magic_damage)
    
    @staticmethod
    def min_distance(player, target):
        return distance(player, target)
    
    def select_by_health(self, player, targets):
        return min(filter(self._has_pos, targets), key=partial(EntityDrawings.min_attacks, player), default=None)
    
    def select_by_damage(self, player, targets):
        return max(filter(self._has_pos, targets), key=EntityDrawings.max_damage, default=None)
    
    def select_by_distance(self, player, targets):
        return min(filter(self._has_pos, targets), key=partial(EntityDrawings.min_distance, player), default=None)
    
