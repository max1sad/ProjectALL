from threading import Thread
import itertools
import time
stop = True
def wiat():
    
        print('Execution', end='')
        it = itertools.cycle(['.'] * 3 + ['\b \b'] * 3)
        #for x in range(100):
        while stop:
            time.sleep(.3)  # выполнение функции
            print(next(it), end='', flush=True)
def startEx():
    t = Thread(target=wiat).start()
def stopEx():
    global stop
    stop = False
#startEx()
#time.sleep(5)
#stopEx()