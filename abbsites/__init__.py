import os
import json
from typing import List, Any


class AbbSites:
    names: List[Any]
    sites: object

    def __init__(self):
        filename = os.path.join(os.path.abspath('.'), 'data.json')
        with open(filename, 'r') as f:
            self.sites = json.load(f)

        self.names = list()
        for s in self.sites['sites']:
            if s['abb']['urlname'] > '':
                this_name = s['name']
                self.names.append(this_name)
        return

    def find_by_name(self, name) -> str:
        address = ''
        for s in self.sites['sites']:
            if s['name'] == name:
                address = s['abb']['address'].replace('http://', '')
        return address

    def find_by_ip(self, address) -> str:
        name = ''
        url = 'http://' + address
        for s in self.sites['sites']:
            if s['address'] == url:
                name = s['name']
        return name

    def find_sort_name(self, name=''):
        result = name
        for s in self.sites['sites']:
            if name == s['abb']['urlname']:
                result = s['name']
                return result
        return result

    def find_user_name(self, name=''):
        result = name
        for s in self.sites['sites']:
            if name == s['name']:
                result = s['abb']['urlname']
                return result
        return result
