#ext
from pyMeow import r_string, r_int, r_int64, r_uint64, r_ints64

#own
from data import Offsets

"""
TODO:
    - Optimize search_mode 3
"""

class ListReader:
    def __init__(self, process, base_address, local_team):
        self.process = process
        self.base_address = base_address
        self.local_team = local_team
        self.name_offset = Offsets.obj_name
        self.team_offset = Offsets.obj_team

    @staticmethod
    def _is_valid_name(name, entities_list, search_mode):
        if isinstance(name, str):
            name = name.lower()
            if search_mode == 0:
                return name in entities_list or name.startswith('practicetool')
            elif search_mode == 1:
                return name.startswith(('sru', 'ha'))
            elif search_mode == 2:
                return name == 'turret'
            elif search_mode == 3:
                wards = ['sightward', 'visionward', 'yellowtrinket', 'yellowtrinketupgrade', 'bluetrinket', 'jammerdevice', 
                         'perkszombieward']
                return name in wards
        
        return False
    

    def is_valid_pointer(self, pointer, entities_list, search_mode):
        process = self.process

        try:
            name = r_string(process, r_int64(process, pointer + self.name_offset), 50)
            if self._is_valid_name(name, entities_list, search_mode):
                team = r_int(process, pointer + self.team_offset)
                if team != self.local_team:
                    return True
        except:
            pass

        try:
            name = r_string(process, pointer + self.name_offset, 50)
            if self._is_valid_name(name, entities_list, search_mode):
                team = r_int(process, pointer + self.team_offset)
                if team != self.local_team:
                    return True
        except:
            pass
        
        return False
    
    def get_pointers(self, type_list: int, entities_list: list = [], size: int = 512, search_mode: int = 0):
        process = self.process
        pointers_mng = r_uint64(process, self.base_address + type_list)
        pointers = r_ints64(process, r_int64(process, pointers_mng + 0x8), size)
        return {pointer for pointer in pointers if self.is_valid_pointer(pointer, entities_list, search_mode)}