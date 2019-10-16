from abbdata import AbbData
import os, json


class AbbAPI:

    def __init__(self, site='') -> None:
        self.address = ''
        self.site = site
        self.lookup_ip_address(site)
        self.data = {}
        if self.address > '':
            self.load_data()

    def lookup_ip_address(self, site):
        filename = os.path.join(os.path.abspath('.'), 'data.json')
        with open(filename, 'r') as f:
            data = json.load(f)

        self.address = ''
        for s in data['sites']:
            if s['name'] == site:
                self.address = s['abb']['address'].replace('http://', '')
        return

    def load_data(self):
        self.data = AbbData(address=self.address, site=self.site).data
