#For making different functions to run parallely follow this procedure.

import threading
from threading import Thread
import time

def time1():    
    while True:
        #Code here
        print("Function1")
        time.sleep(5) # pass time delay in seconds
    
def time2():
    #Code here
    while True:
        #Code here
        print("Function2")
        time.sleep(7) # pass time delay in seconds
    
if __name__ == '__main__':
    p1=Thread(target = time1)
    p2=Thread(target = time2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
