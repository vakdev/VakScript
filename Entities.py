#ext
from collections import namedtuple
from pyMeow import r_string, r_float, r_bool, r_int
from math import hypot
from functools import partial

#own
from Data import Offsets
from WorldToScreen import World

class ReadAttributes:

    def __init__(self, process):
        self.process = process 
        self.PlayerNamedtuple = namedtuple('Player', 'name basic_attack bonus_attack x y z attack_range')
        self.EnemyNamedtuple = namedtuple('Enemy', 'name health max_health armor basic_attack bonus_attack magic_damage x y z alive targetable visible attack_range')
        self.MinionNamedtuple = namedtuple('Minion', 'name health armor x y z alive targetable visible')

    
    def read_player(self, local_player):
        d, process = {}, self.process
        d['name'] = r_string(process, local_player + Offsets.objName)
        d['basic_attack'] = r_float(process, local_player + Offsets.objBaseAttack)
        d['bonus_attack'] = r_float(process, local_player + Offsets.objBonusAttack)
        d['x'] = r_float(process, local_player + Offsets.objPosX)
        d['y'] = r_float(process, local_player + Offsets.objPosY)
        d['z'] = r_float(process, local_player + Offsets.objPosZ)
        d['attack_range'] = r_float(process, local_player + Offsets.objAttackRange)
        return self.PlayerNamedtuple(**d)
    
    def read_enemy(self, pointer):
        d, process = {}, self.process
        d['name'] = r_string(process, pointer + Offsets.objName)
        d['health'] = r_float(process, pointer + Offsets.objHealth)
        d['max_health'] = r_float(process, pointer + Offsets.objMaxHealth)
        d['armor'] = r_float(process, pointer + Offsets.objArmor)
        d['basic_attack'] = r_float(process, pointer + Offsets.objBaseAttack)
        d['bonus_attack'] = r_float(process, pointer + Offsets.objBonusAttack)
        d['magic_damage'] = r_float(process, pointer + Offsets.objMagicDamage)
        d['x'] = r_float(process, pointer + Offsets.objPosX)
        d['y'] = r_float(process, pointer + Offsets.objPosY)
        d['z'] = r_float(process, pointer + Offsets.objPosZ)
        d['alive'] = r_int(process, pointer + Offsets.objSpawnCount) % 2 == 0
        d['targetable'] = r_bool(process, pointer + Offsets.objTargetable)#
        d['visible'] = r_bool(process, pointer + Offsets.objVisible)
        d['attack_range'] = r_float(process, pointer + Offsets.objAttackRange)
        return self.EnemyNamedtuple(**d)
    
    def read_minion(self, pointer):
        d, process = {}, self.process
        d['name'] = r_string(process, pointer + Offsets.objName)
        d['health'] = r_float(process, pointer + Offsets.objHealth)
        d['armor'] = r_float(process, pointer + Offsets.objArmor)
        d['x'] = r_float(process, pointer + Offsets.objPosX)
        d['y'] = r_float(process, pointer + Offsets.objPosY)
        d['z'] = r_float(process, pointer + Offsets.objPosZ)
        d['alive'] = r_int(process, pointer + Offsets.objSpawnCount) % 2 == 0
        d['targetable'] = r_bool(process, pointer + Offsets.objTargetable)
        d['visible'] = r_bool(process, pointer + Offsets.objVisible)
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
        self.radius = self.stats.getTargetsRadius()
    
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
                distance = distance(player, entity)
                if target is None or distance < min_distance:
                    target, min_distance = entity, distance
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
    
    def _has_pos(self, target):
        return self.world.world_to_screen_restricted(self.world.get_view_proj_matrix(), target.x, target.z, target.y) and target.alive and target.targetable and target.visible

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
    
