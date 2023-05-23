#ext
from multiprocessing import Process, Value, freeze_support
import ctypes
import sys

#own
from AutoKite import auto_kite
from Drawings import drawings
from GUI import gui

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    freeze_support()
    terminate = Value('b', False)

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
        
    procs = [
        Process(target=auto_kite, args=(terminate,)),
        Process(target=drawings, args=(terminate,)),
        Process(target=gui, args=(terminate,))
    ]

    for process in procs:
        process.start()
    
    for process in procs:
        process.join()
