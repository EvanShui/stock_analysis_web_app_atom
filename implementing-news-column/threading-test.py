import threading
import time

i = [0]
lock = threading.Lock()

def foo(j):
    while True:
        with lock:
            print(j[0])
        time.sleep(5)

t = threading.Thread(target=foo, args=(i,))
t.start()

while True:
    with lock:
        i[0] = i[0]+1
