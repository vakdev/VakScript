#ext
from json import load, dump

#own
from Data import Data, VK_CODES

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
            self.settings['AutoKite']['Keys'][id] = key
            self._jsonUpdate()

    def setMode(self, id, mode):
        self.settings['AutoKite']['Modes'][id] = mode
        self._jsonUpdate()

    def setSetting(self, id, setting):
        self.settings['AutoKite']['Settings'][id] = setting
        self._jsonUpdate()

    def setSmiteKey(self, id, key):
        if self.isValidKey(key):
            self.settings['AutoSmite']['Keys'][id] = key
            self._jsonUpdate()

class jsonGetter:

    def __init__(self):
        self.file_name = Data.settings_file_name
        self.file = open(self.file_name, "r+")
        self.settings = load(self.file)

    def getKey(self, id):
        data = self.settings['AutoKite']['Keys'][id]
        self.file.close()
        return data
    
    def getMode(self, id):
        data = self.settings['AutoKite']['Modes'][id]
        self.file.close()
        return data
    
    def getSetting(self, id):
        data = self.settings['AutoKite']['Settings'][id]
        self.file.close()
        return data
    
    def getSmiteKey(self, id):
        data = self.settings['AutoSmite']['Keys'][id]
        self.file.close()
        return data
