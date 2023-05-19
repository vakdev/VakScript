#ext
from mousekey import get_active_window
from os import path, system
import fileinput

#own
from Settings import jsonGetter, jsonSetter
from Data import Data

options = {
    'EnableTargetedAttackMove':'1',
    'TargetChampionsOnlyAsToggle':'0',
    'evtCameraSnap':'[Space],[v]',
    'evtChampionOnly':'[Button 3]',
    'evtPlayerAttackMoveClick':'[a]',
    'evtPlayerMoveClick':'[Button 2]',
    'evtShowCharacterMenu':'[o]'
}

class Autoconfig:
    
    def __init__(self):
        self.autoconfig = jsonGetter().getSetting("autoconfig")
        lol_path = get_active_window()[-1]
        self.settings_to_persist = path.join(lol_path, Data.settings_to_persist_path)
        self.persisted_settings = path.join(lol_path, Data.persisted_settings_path)
        system(f'taskkill -f -im "{Data.game_name_executable}"')

    @staticmethod
    def clearName(string):
        return string.strip().removeprefix('"name": "').removesuffix('",')
    
    @staticmethod
    def clearValue(string):
        return string.strip(" \n").removeprefix('"value": "').removesuffix('"')
    
    def removeDuplications(self):
        #Prevent key bugs.
        current_values = self.getPersistedSettings()
        duplications = dict()
        with open(self.persisted_settings) as persisted_settings:
            for index, line in enumerate(persisted_settings, 1):
                line = Autoconfig.clearValue(line)
                if line in current_values.values() and index not in current_values.keys():
                    if len(line) > 1:
                        duplications[index] = line

        for line in fileinput.input(self.persisted_settings, inplace=True):
            current_index = fileinput.lineno()
            for k, v in duplications.items():
                if current_index == k:
                    line = line.replace(v, '[<Unbound>],[<Unbound>]')

            print(line, end="")

    def getPersistedSettings(self):
        if self.autoconfig:
            current_settings = dict()
            is_value = False
            value_pos = None
            with open(self.persisted_settings, "r+") as persisted_settings:
                for index, line in enumerate(persisted_settings, 1):
                    line_name = Autoconfig.clearName(line)
                    if line_name in options.keys():
                        value_pos = index + 1
                        is_value = True
                        continue
                    if is_value:
                        current_settings[value_pos] = Autoconfig.clearValue(line)
                        is_value = False

            return current_settings
        

    def setPersistedSettings(self):
        if self.autoconfig:
            current_settings = self.getPersistedSettings()
            for line in fileinput.input(self.persisted_settings, inplace=True):
                current_index = fileinput.lineno()
                for (value_pos, current_value), new_value in zip(current_settings.items(), options.values()):
                    if value_pos == current_index:
                        line = line.replace(current_value, new_value)
                print(line, end="")

            self.removeDuplications()

    def toggleSettingsToPersist(self, statment):
        for line in fileinput.input(self.settings_to_persist, inplace=True):
            if statment:
                line = line.replace("false", "true")
            else:
                line = line.replace("true", "false")

            print(line, end="")

    def setJsonSettings(self):
        jsonSetter().setKey('orbwalk', 'space')
        jsonSetter().setKey('laneclear', 'v')
        jsonSetter().setKey('lasthit', 'x')
        jsonSetter().setMode('orbwalk', 'Lowest Health')
        jsonSetter().setMode('lasthit', 'auto')
        jsonSetter().setSetting('autoconfig', False)
        jsonSetter().setSetting('ppc', False)
        jsonSetter().setSetting('ext_drawings', True)
        jsonSetter().setSetting('ext_track', True)
        jsonSetter().setSetting('ext_focus', True)
        jsonSetter().setSetting('ext_limited', False)
        jsonSetter().setSetting('freeze', False)


    def start(self):
        self.toggleSettingsToPersist(False)
        self.setPersistedSettings()
        self.toggleSettingsToPersist(True)
        self.setJsonSettings()


