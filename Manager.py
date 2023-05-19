#ext
from pyMeow import r_string, r_int, r_int64, r_uint64, r_ints64

#own
from Data import Offsets

class ReadManager:
    
    def __init__(self, process, base_address):
        self.process = process
        self.base_address = base_address
        self.champion_list = Offsets.oChampionList
        self.minion_list = Offsets.oMinionList
        self.name = Offsets.objName
        self.team = Offsets.objTeam

    def isValidPointer(self, pointer, champions, team):
        #Get 5 pointers only.
        try:
            pointer_name = r_string(self.process, pointer + self.name, 50).lower()
            pointer_team = r_int(self.process, pointer + self.team)
            if pointer_name in champions and pointer_team != team:
                return pointer
        except:
            return None
        
        #If there's a custom target in practice mode.
        try:
            pointer_name = r_string(self.process, r_int64(self.process, pointer + self.name), 50).lower()
            pointer_team = r_int(self.process, pointer + self.team)
            if pointer_name.startswith('practicetool') and pointer_team != team: 
                return pointer
        except:
            return None

    def isValidMinionPointer(self, pointer, minions, team):
        try:
            pointer_name = r_string(self.process, r_int64(self.process, pointer + self.name), 50)
            pointer_team = r_int(self.process, pointer + self.team)
            if pointer_name in minions and pointer_team != team:
                return pointer
        except:
            return None
        
    def getChampionPointers(self, champions, team):
        champion_manager = r_uint64(self.process, self.base_address + self.champion_list)
        pointers = r_ints64(self.process, r_int64(self.process, champion_manager + 0x8), 200)
        return {pointer for pointer in pointers if self.isValidPointer(pointer, champions, team)}
    
    def getMinionPointers(self, minions, team):
        minion_manager = r_uint64(self.process, self.base_address + self.minion_list)
        pointers = r_ints64(self.process, r_int64(self.process, minion_manager + 0x8), 200)
        return [pointer for pointer in pointers if self.isValidMinionPointer(pointer, minions, team)]
    
