from multiprocessing import Pool, Manager
import signal

from abbsites import AbbSites
from abbapi import AbbAPI
import arrow
import time

sites = list()

abbsites = AbbSites()
sites = abbsites.names

pause = 120  # seconds
show_progress = True


def sighandler(a, b):
    pass


def my_process(inp_param):
    result = AbbAPI(site=inp_param['site'])
    inp_param['q'].put(result)
    return


#
# Setup list of sites to request data.
#
params = []
i = 0
iEnd = len(sites)
while i < iEnd:
    one = sites[i]
    p = {'site': one, 'q': object}
    params.append(p)
    i += 1

manager = Manager()
q = manager.Queue()
i = 0
while i < iEnd:
    sites[i]['q'] = q
    i += 1

#
# Perform work.
#
signal.signal(signal.SIGINT, sighandler)

while True:
    start_time = arrow.utcnow().timestamp

    pool = Pool()
    pool.map(my_process, params)

    items = list()
    while not output_queue.empty():
        item = output_queue.get()
        items.append(item)

    still_waiting = True
    while still_waiting:
        try:
            time_remaining = arrow.utcnow().timestamp - start_time
            still_waiting = (time_remaining < pause)
            print('Waiting %d' % time_remaining)
        finally:
            time.sleep(5)
