from multiprocessing import Pool, Manager
from getabbflow import GetAbbFlow

show_progress = True


# sites = [
#     {"address": '192.168.30.146', "site": '01L'},
#     {"address": '192.168.30.130', "site": '01RA'},
#     {"address": '13l.recorder.wwd.local', "site": '13L'},
#     {"address": '12l.recorder.wwd.local', "site": '12L'},
# ]


def my_process(inp_param):
    address = inp_param['address']
    site = inp_param['site']
    if show_progress:
        print('Start %s, with address = %s' % (site, address))
    result = GetAbbFlow(address=address, site=site)
    if show_progress:
        print('finish %s' % site)
    data = result.data
    inp_param['q'].put(data)
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
pool = Pool(processes=3)
pool.map(my_process, params)

#
# Get Results from output_queue.
#
while not output_queue.empty():
    item = output_queue.get()
    for row in item:
        print(row)

print('******** app finished *******')
