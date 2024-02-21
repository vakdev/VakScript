#built-in
from collections import namedtuple
from math import hypot

#ext
from pyMeow import r_string, r_float, r_bool, r_int, r_ints64, r_uint64

#own
from data import Offsets
from stats import Stats

"""
TODO:
    - Remove name reading from read_minion. (bugs)
    - Add read_ward
    - Optimize buffs and items reading.
    - Add lasthit function in target selector.

"""


class AttributesReader(Offsets):
    def __init__(self, process, base_address):
        self.process = process
        self.base_address = base_address
        self.spell_keys = ['Q', 'W', 'E', 'R', 'D', 'F']
        self.PlayerNamedtuple = namedtuple('Player', 'name lvl basic_attack bonus_attack magic_damage x y z attack_range items buffs')
        self.EnemyNamedtuple = namedtuple('Enemy', 'name health max_health gold armor magic_resist basic_attack bonus_attack magic_damage x y z alive targetable visible attack_range pointer items')
        self.MinionNamedtuple = namedtuple('Minion', 'name health armor magic_resist x y z alive targetable visible')
        self.TurretNamedTuple = namedtuple('Turret', 'attack_range x y z alive targetable visible')
        self.BuffNamedTuple = namedtuple('Buff', 'name count count2 alive')
        self.zombies = ["Sion", "KogMaw", "Karthus"]
    
    def read_items(self, pointer):
        process = self.process
        items_ids = []
        for i in range(7):
            try:
                item = r_uint64(process, pointer + Offsets.obj_item_list + 0x50 + 0x8 * i)
                item_slot = r_uint64(process, item + 0x10)
                item_info = r_uint64(process, item_slot + Offsets.item_info)
                item_info_id = r_int(process, item_info + Offsets.item_info_id)
                items_ids.append(item_info_id)
            except:
                items_ids.append(0)
        return items_ids

    def read_buffs(self, pointer):
        process = self.process
        buffs = []
        for i in range(200):
            buff_manager = r_uint64(process, pointer + Offsets.buff_manager)
            try:
                buff = r_uint64(process, buff_manager + 0x10 + 0x8 * i)
                buff_count = r_int(process, buff + Offsets.buff_count)
                buff_count2 = r_int(process, buff + Offsets.buff_count2)
            except:
                continue
            
            gametime = r_float(process, self.base_address + Offsets.game_time)
            buff_alive = False
            try:
                buff_start = r_float(process, buff + Offsets.buff_start)
                buff_end = r_float(process, buff + Offsets.buff_end)
                if buff_start <= gametime <= buff_end:
                    buff_alive = True
            except:
                buff_alive = True

            buff_info = r_uint64(process, buff + Offsets.buff_info)
            try:
                buff_name_ptr = r_uint64(process, buff_info + Offsets.buff_name)
                buff_name = r_string(process, buff_name_ptr, 100)
            except:
                continue

            attributes = self.BuffNamedTuple(
                name = buff_name,
                count = buff_count,
                count2 = buff_count2,
                alive = buff_alive
            )
            buffs.append(attributes)
        return buffs
    
    def read_player(self, local_player):
        process = self.process

        items_ids = self.read_items(local_player)
        buffs = self.read_buffs(local_player)

        attributes = self.PlayerNamedtuple(
            name =         r_string(process, local_player + self.obj_name),
            lvl =          r_int(process, local_player + self.obj_lvl),
            basic_attack = r_float(process, local_player + self.obj_base_attack),
            bonus_attack = r_float(process, local_player + self.obj_bonus_attack),
            magic_damage = r_float(process, local_player + self.obj_magic_damage),
            x =            r_float(process, local_player + self.obj_x),
            y =            r_float(process, local_player + self.obj_y),
            z =            r_float(process, local_player + self.obj_z),
            attack_range = r_float(process, local_player + self.obj_attack_range),
            items =        items_ids,
            buffs =        buffs
        )

        return attributes
    
    def read_enemy(self, pointer):
        process = self.process

        items_ids = self.read_items(pointer)

        # Currently cause huge lags, because we read alot of enemies for some reason
        # buffs = self.read_buffs(pointer)
        
        name =         r_string(process, pointer + self.obj_name)
        health =       r_float(process, pointer + self.obj_health)

        attributes = self.EnemyNamedtuple(
            name =         name,
            health =       health,
            max_health =   r_float(process, pointer + self.obj_max_health),
            gold =         r_int(process, pointer + self.obj_gold),
            armor =        r_float(process, pointer + self.obj_armor),
            magic_resist = r_float(process, pointer + self.obj_magic_resist),
            basic_attack = r_float(process, pointer + self.obj_base_attack),
            bonus_attack = r_float(process, pointer + self.obj_bonus_attack),
            magic_damage = r_float(process, pointer + self.obj_magic_damage),
            x =            r_float(process, pointer + self.obj_x),
            y =            r_float(process, pointer + self.obj_y),
            z =            r_float(process, pointer + self.obj_z),
            alive =        health > 0 if name in self.zombies else r_int(process, pointer + self.obj_spawn_count) % 2 == 0,
            targetable =   r_bool(process, pointer + self.obj_targetable),
            visible =      r_bool(process, pointer + self.obj_visible),
            attack_range = r_float(process, pointer + self.obj_attack_range),
            pointer =      pointer,
            items =        items_ids,
            # buffs =        buffs
        )
    
        return attributes
    
    def read_minion(self, pointer):
        process = self.process
        attributes = self.MinionNamedtuple(
            name =         r_string(process, pointer + self.obj_name),
            health =       r_float(process, pointer + self.obj_health),
            armor =        r_float(process, pointer + self.obj_armor),
            magic_resist = r_float(process, pointer + self.obj_magic_resist),
            x =            r_float(process, pointer + self.obj_x),
            y =            r_float(process, pointer + self.obj_y),
            z =            r_float(process, pointer + self.obj_z),
            alive =        r_int(process, pointer + self.obj_spawn_count) % 2 == 0,
            targetable =   r_bool(process, pointer + self.obj_targetable),
            visible =      r_bool(process, pointer + self.obj_visible),
        )

        return attributes
    
    def read_turret(self, pointer):
        process = self.process
        attributes = self.TurretNamedTuple(
            attack_range = r_float(process, pointer + self.obj_attack_range),
            x =            r_float(process, pointer + self.obj_x),
            y =            r_float(process, pointer + self.obj_y),
            z =            r_float(process, pointer + self.obj_z),
            alive =        r_int(process, pointer + self.obj_spawn_count) % 2 == 0,
            targetable =   r_bool(process, pointer + self.obj_targetable),
            visible =      r_bool(process, pointer + self.obj_visible),
        )

        return attributes

    def read_spells(self, pointer):
        spells, process = [], self.process
        spell_book = r_ints64(process, pointer + self.obj_spell_book, 0x6)
        for spell_slot in spell_book:
            spell_info_ptr = r_uint64(process, spell_slot + self.spell_info)
            spell_data_ptr = r_uint64(process, spell_info_ptr + self.spell_data)
            spell_name_ptr = r_uint64(process, spell_data_ptr + self.spell_name)
            name = r_string(process, spell_name_ptr, 50)
            charges = r_int(process, spell_slot + self.spell_charges)

            level = r_int(process, spell_slot + self.spell_level)
            cooldown = r_float(process, spell_slot + self.spell_cooldown)
            spell = dict(name=name, charges=charges, level=level, cooldown=cooldown)
            spells.append(spell)
        # to use spells: spells[0]['level'] or spells[0]['cooldown']
        # where 0 is Q, 3 is R, 4 and 5 are summoner spells
        return spells
    

    
class EntityConditions:
    def __init__(self, world=None, stats=None):
        if stats is not None:
            self.radius = stats.get_targets_radius()
        else:
            self.radius = Stats().get_targets_radius()

        if world is not None:
            self.world_to_screen_limited = world.world_to_screen_limited
            self.get_view_proj_matrix = world.get_view_proj_matrix

    @staticmethod
    def hurtable(entity) -> bool:
        return entity.alive and entity.visible and entity.targetable

    @staticmethod
    def effective_damage(damage, armor) -> float:
        if armor >= 0:
            return damage * 100. / (100. + armor)
        return damage * (2. - (100. / (100. - armor)))

    @staticmethod
    def max_damage(entity) -> float:
        return max(entity.basic_attack + entity.bonus_attack, entity.magic_damage)

    def distance(self, player, target) -> float:
        return hypot(player.x - target.x, player.y - target.y)
    
    def in_distance(self, player, target):
        return self.distance(player, target) - self.radius.get(target.name, 65.) <= player.attack_range + self.radius.get(player.name, 65.)
    
    def in_distance_minion(self, player, target):
        return self.distance(player, target) - 65.0 <= player.attack_range + self.radius.get(player.name, 65.)

    def min_attacks(self, player, entity) -> float:
        return entity.health / self.effective_damage(player.basic_attack + player.bonus_attack, entity.armor)

class TargetSelector(EntityConditions):
    def __init__(self, world=None, stats=None):
        super().__init__(world, stats)

    def select_by_health(self, player, targets):
        # Enemy with less hits to kill him will be focused.
        target, min_autos = None, None
        for entity in targets:
            if self.hurtable(entity) and self.in_distance(player, entity):
                autos = self.min_attacks(player, entity)
                if target is None or 0 < autos < min_autos:
                    target, min_autos = entity, autos
        return target
    
    def select_by_damage(self, player, targets):
        # Enemy with most damage will be focused.
        target, max_damage = None, None
        for entity in targets:
            if self.hurtable(entity) and self.in_distance(player, entity):
                damage = max(entity.basic_attack + entity.bonus_attack + entity.attack_range, entity.magic_damage)
                if target is None or damage > max_damage:
                    target, max_damage = entity, damage
        return target
    
    def select_by_distance(self, player, targets):
        # Nearest enemy will be focused.
        target, min_distance = None, None
        for entity in targets:
            if self.hurtable(entity) and self.in_distance(player, entity):
                d = self.distance(player, entity)
                if target is None or d < min_distance:
                    target, min_distance = entity, d
        return target
        
    def select_by_lasthit(self, player, entities):
        # Select minion to lasthit
        valid_targets = filter(lambda entity: self.hurtable(entity) and self.in_distance_minion(player, entity) and self.effective_damage(player.basic_attack + player.bonus_attack, entity.armor) > entity.health + entity.armor, entities)
        return min(valid_targets, key=lambda target: hypot(player.x - target.x, player.y - target.y), default=None)
