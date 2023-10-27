#built-in
from ctypes import wintypes, Structure, Union, WinDLL, POINTER, byref, sizeof
from random import choice
from string import printable
from traceback import print_exc
from time import sleep

#ext
from win32gui import GetWindowText, GetForegroundWindow

#own
from data import Info

DEBUG = True

#
user32 = WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(Structure):
    class _INPUT(Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

def press_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, byref(x), sizeof(x))
    
def release_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, byref(x), sizeof(x))

def send_key(hexKeyCode):
    press_key(hexKeyCode)
    release_key(hexKeyCode)

def is_active_window():
    return GetWindowText(GetForegroundWindow()) == Info.game_name_window

def safe_title():
    return "".join(choice(printable) for i in range(11))

def debug_info(exception=None, ex_info=False, info=None):
    if DEBUG:    
        if info is not None:
            print(f'info > {info}')
        elif exception:
            print(f's > {exception}')
            if ex_info:
                print('d >',end=' ')
                print_exc()
    sleep(0.1)