from multiprocessing import Process
import time
import random


def my_process(seconds=5):
    print('Start process ')
    time.sleep(seconds)
    print('End process')
    return


def randomSeconds():
    i = random.randint(2, 10)
    return i


if __name__ == "__main__":
    procs = []
    proc = Process(target=my_process(randomSeconds()))
    procs.append(proc)
    proc = Process(target=my_process(randomSeconds()))
    procs.append(proc)

    for p in procs:
        p.start()

    for p in procs:
        p.join()
