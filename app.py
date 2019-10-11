from multiprocessing import Pool, Manager
from getabbflow import GetAbbFlow

sites = [
    {"address": '192.168.30.146', "site": '01L'},
    {"address": '192.168.30.130', "site": '01RA'},

    {"address": '13l.recorder.wwd.local', "site": '13L'},
    {"address": '12l.recorder.wwd.local', "site": '12L'},

    {"address": '11l.recorder.wwd.local', "site": '11L'},
    {"address": '10l.recorder.wwd.local', "site": '10L'},
    {"address": '14l.recorder.wwd.local', "site": '14L'},
    {"address": '15l.recorder.wwd.local', "site": '15L'},
    {"address": '16l.recorder.wwd.local', "site": '16L'},
]

results = {}


def my_process(inp_param):
    address = inp_param['address']
    site = inp_param['site']
    print('Start Address = %s' % address)
    result = GetAbbFlow(address=address, site=site)
    print('finish address = %s' % address)
    data = result.data
    inp_param['q'].put(data)
    return


manager = Manager()
output_queue = manager.Queue()
params = list()
for s in sites:
    p = {'address': s['address'], 'site': s['site'], 'q': output_queue}
    params.append(p)

print(params)

# pool = Pool(processes=5)
pool = Pool()
print('x')
pool.map(my_process, params)
print('y')
# with Pool() as pool:
#
#     pool.map(my_process, params)
#
print('Ending program')
while not output_queue.empty():
    item = output_queue.get()
    for row in item:
        print(row)

print('******** app finished *******')

# for site in sites:
#     results[site['site']] = GetAbbFlow(address=site['address'], site=site['site'])

# url = 'http://13l.recorder.wwd.local/isapiext.dll/?100000101'
# address = '13l.recorder.wwd.local'
# abb = GetAbbFlow(address=address, site='13L')
# data = abb.data


# def print_results(data):
#     for r in data:
#         _s_ = data[r].timestamp_local + ' - ' + data[r].site
#         print(_s_)
#         for row in data[r].data:
#             _s_ = f'%s %10.3f' % (row['tag'], row['value'])
#             print(_s_)
#
#
# print_results(results)
