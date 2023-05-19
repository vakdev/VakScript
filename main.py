#ext
from multiprocessing import Process, Value, freeze_support

#own
from AutoKite import auto_kite
from Drawings import drawings
from GUI import gui


if __name__ == '__main__':
    freeze_support()
    terminate = Value('b', False)
    procs = [
        Process(target=auto_kite, args=(terminate,)),
        Process(target=drawings, args=(terminate,)),
        Process(target=gui, args=(terminate,))
    ]

    for process in procs:
        process.start()
    
    for process in procs:
        process.join()

