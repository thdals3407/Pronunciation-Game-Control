from multiprocessing import Process, Queue
import time

q = Queue()

def loop1(q):
    i = 1
    while True:
        i+=1
        time.sleep(0.1)
        q.put(i)


def mainloop():
    j = 0
    while True:
        time.sleep(1)
        print(q.get())

audio_process = Process(target=loop1, args=(q,))
audio_process.start()

mainloop()