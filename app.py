from getabbflow import GetAbbFlow

sites = [
    {"address": '13l.recorder.wwd.local', "site": '13L'},
    {"address": '12l.recorder.wwd.local', "site": '12L'}
]

results = {}


for site in sites:
    results[site['site']] = GetAbbFlow(address=site['address'], site=site['site'])

# url = 'http://13l.recorder.wwd.local/isapiext.dll/?100000101'
# address = '13l.recorder.wwd.local'
# abb = GetAbbFlow(address=address, site='13L')
# data = abb.data


def print_results(data):
    for r in data:
        _s_ = data[r].timestamp_local + ' - ' + data[r].site
        print(_s_)
        for row in data[r].data:
            _s_ = f'%s %10.3f' % (row['tag'], row['value'])
            print(_s_)


print_results(results)
