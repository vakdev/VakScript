#ext
from json import load, dump

#own
from data import Info, VK_CODES

class jsonSetter:

    def __init__(self):
        self.file_name = Info.settings_file_name
        self.file = open(self.file_name, "r+")
        self.settings = load(self.file)

    def _json_update(self):
        self.file.seek(0)
        dump(self.settings, self.file, indent=4)
        self.file.truncate()
        self.file.close()

    def is_valid_data(self, data):
        return data.lower() in VK_CODES.keys()
    
    def set_spaceglider_data(self, key, data):
        if isinstance(data, str):
            if self.is_valid_data(data):
                self.settings['Spaceglider'][key] = data.lower()
            elif key.endswith(('mode', 'prio')):
                self.settings['Spaceglider'][key] = data
        else:
            self.settings['Spaceglider'][key] = data
        self._json_update()

    def set_drawings_data(self, key, data):
        self.settings['Drawings'][key] = data
        self._json_update()

    def set_autosmite_data(self, key, data):
        if isinstance(data, str):
            if self.is_valid_data(data):
                self.settings['AutoSmite'][key] = data.lower()
        else:
            self.settings['AutoSmite'][key] = data
        self._json_update()
    
    def set_scripts_data(self, key, data):
        self.settings['Scripts'][key] = data
        self._json_update()

class jsonGetter(jsonSetter):

    def __init__(self):
        super().__init__()

    def get_data(self, key):
        for sk, sv in self.settings.items():
            if key in sv:
                return self.settings[sk][key]