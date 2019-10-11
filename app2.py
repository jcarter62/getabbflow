from multiprocessing import Pool
import time
import random


def my_process(num):
    seconds = randomSeconds()
    print('Start process %d for %d seconds' % (num, seconds))
    time.sleep(seconds)
    print('End process %d' % num)
    return


def randomSeconds():
    return random.randint(2, 5)


print('Starting program')
with Pool(5) as p:
    p.map(my_process, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

# time.sleep(10)
print('Ending program')
