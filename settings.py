#ext
from json import load, dump

#own
from data import Data, VK_CODES

class jsonSetter:

    def __init__(self):
        self.file_name = Data.settings_file_name
        self.file = open(self.file_name, "r+")
        self.settings = load(self.file)

    def _jsonUpdate(self):
        self.file.seek(0)
        dump(self.settings, self.file, indent=4)
        self.file.truncate()
        self.file.close()

    def isValidKey(self, key):
        return key.lower() in VK_CODES.keys()
    
    def setKey(self, id, key):
        if self.isValidKey(key):
            self.settings['AutoKite']['Keys'][id] = key.lower()
            self._jsonUpdate()

    def setMode(self, id, mode):
        self.settings['AutoKite']['Modes'][id] = mode
        self._jsonUpdate()

    def setSetting(self, id, setting):
        self.settings['AutoKite']['Settings'][id] = setting
        self._jsonUpdate()

    def setSmiteKey(self, id, key):
        if isinstance(key, str):
            if self.isValidKey(key):
                self.settings['AutoSmite']['Keys'][id] = key.lower()
        else:
            self.settings['AutoSmite']['Keys'][id] = key
        self._jsonUpdate()
