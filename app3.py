from abbapi import AbbAPI


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
results = list()

#
# Setup list of sites to request data.
#
for s in sites:
    result = AbbAPI(site=s['site']).data
    # result = AbbData(address=s['address'], site=s['site']).data
    results.append(result)

for r in results:
    print(r)

print('******** app finished *******')
