from multiprocessing import Pool, Manager
import signal
# from getabbflow import GetAbbFlow
from abbflow import AbbFlow
from abbacft import AbbAcFt

show_progress = True

def my_process(inp_param):
    address = inp_param['address']
    site = inp_param['site']
    if show_progress:
        print('Start %s, with address = %s' % (site, address))
    flow = AbbFlow(address=address, site=site)
    acft = AbbAcFt(address=address, site=site)
    if show_progress:
        print('finish %s' % site)
    result = {
        'site': site,
        'flow': {},
        'acft': {}
    }
    if len(flow.data) > 0:
        result['flow'] = flow.data

    if len(acft.data) > 0:
        result['acft'] = acft.data

    inp_param['q'].put(result)
    return


def load_sites_from_file():
    import os, json
    __filename = os.path.join(os.path.abspath('.'), 'data.json')
    with open(__filename, 'r') as f:
        __data = json.load(f)

    __result = []
    for s in __data['sites']:
        if s['abb']['urlname'] > '':
            site = s['name']
            address = s['abb']['address'].replace('http://', '')
            __result.append({'address': address, 'site': site})
    return __result


def sighandler(a, b):
    pass

sites = load_sites_from_file()

#
# Setup list of sites to request data.
#
manager = Manager()
output_queue = manager.Queue()
params = list()
for s in sites:
    p = {'address': s['address'], 'site': s['site'], 'q': output_queue}
    params.append(p)

# print(params)

#
# Perform work.
#
signal.signal(signal.SIGINT, sighandler)
pool = Pool()
pool.map(my_process, params)

#
# Get Results from output_queue.
#
items = list()
while not output_queue.empty():
    item = output_queue.get()
    items.append(item)

for row in items:
    print(row)

print('******** app finished *******')
