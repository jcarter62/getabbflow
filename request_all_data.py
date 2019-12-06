from multiprocessing import Pool, Manager, freeze_support
import signal

from abbsites import AbbSites
from abbapi import AbbAPI
from abbsavedata import AbbSaveData
import arrow
import time

pause = 120  # seconds
show_progress = True
show_log = True

sites = list()

def sighandler(a, b):
    pass


def log_file() -> str:
    import os
    import tempfile
    f = tempfile.TemporaryDirectory().name
    today_name = arrow.now().strftime("%Y%m%d.txt")
    result = os.path.join(f, today_name)
    return result


def log_it(message):
    if show_log:
        file = log_file()
        ts = arrow.now()
        f = open(file, "w+")
        s = f"%s %s" % (ts, message)
        f.writelines(s)
        f.close()


def my_process(inp_param):
    log_it(inp_param['site'] + ' start ')
    result = AbbAPI(site=inp_param['site'])
    inp_param['q'].put(result)
    log_it(inp_param['site'] + ' finished ')
    return




if __name__ == '__main__':
    # freeze_support()

    #
    # Setup list of sites to request data.
    #
    params = []
    manager = Manager()
    q = manager.Queue()

    abb_sites = AbbSites()
    sites = abb_sites.names

    log_it('start setting up params')

    i = 0
    iEnd = len(sites)
    while i < iEnd:
        one = sites[i]
        p = {'site': one, 'q': q}
        params.append(p)
        i += 1

    print(sites)
    print(params)

    log_it('finished setting up params')


    #
    # Perform work.
    #
    # signal.signal(signal.SIGINT, sighandler)

    while True:
        start_time = arrow.utcnow().timestamp
        time_remaining = 0

        print(params)
        with Pool(processes=20) as pool:
            # pool = Pool(processes=20)
            pool.map(my_process, params)

        msg = 'Starting to wait for finished processes'
        log_it(msg)

        db = AbbSaveData()
        while not q.empty():
            item = q.get()
            msg = 'process finished for %s' % item.data['site']
            log_it(msg)
            key = f'%-15s - %d' % (item.data['site'], item.data['t0'])
            try:
                db.save_record(key=key, data=item.data)
            finally:
                msg = 'save record for %s' % item.data['site']
                log_it(msg)

        db.client.close()

        still_waiting = True
        while still_waiting:
            try:
                time_remaining = arrow.utcnow().timestamp - start_time
                still_waiting = (time_remaining < pause)
                msg = 'Elapsed time: %s, Target time: %s, State: %s' % (time_remaining, pause, still_waiting.__str__())
                log_it(msg)
                if still_waiting:
                    time.sleep(5)
            finally:
                pass

        msg = 'The waiting is over !'
        log_it(msg)
        pool.close()
