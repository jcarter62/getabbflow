from multiprocessing import Pool, Manager
import time
import random

print('Starting program')
datalist = list()


def my_process(inp_param):
    print(inp_param)
    num = inp_param['num']
    seconds = randomSeconds()
    text = 'this is a text field for id: %d' % num
    text = text + ', and %d seconds' % seconds
    print(text)
    data = {'seconds': seconds, 'text': text}
    time.sleep(seconds)
    print('End process %d' % num)
    inp_param['q'].put(data)
    #    output_queue.put(data)
    return


def randomSeconds():
    return random.randint(2, 5)


items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
params = list()

with Pool(processes=5) as pool:
    manager = Manager()
    output_queue = manager.Queue()
    for i in items:
        param = {'num': i, 'site': 'site #%d' % i, 'q': output_queue}
        params.append(param)

    pool.map(my_process, params)

    print('Ending program')
    while not output_queue.empty():
        item = output_queue.get()
        print(item)

print('******** app finished *******')
