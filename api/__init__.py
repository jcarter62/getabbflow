import os
import requests


class Api:

    def __init__(self) -> None:
        super().__init__()

    def _load_settings(self):
        filename = os.path.join(os.path.abspath('.'), 'data.json')
        with open(filename, 'r') as f:
            self.sites = json.load(f)


'''
        filename = os.path.join(os.path.abspath('.'), 'data.json')
        with open(filename, 'r') as f:
            self.sites = json.load(f)

        self.names = list()
        for s in self.sites['sites']:
            if s['abb']['urlname'] > '':
                this_name = s['name']
                self.names.append(this_name)
        return
'''

# def get_orders_summary():
#     import requests
#     result = []
#     filename = os.path.join(os.path.abspath('.'), 'abborders_url.json')
#
#     url = abb_orders_url() + 'orders_summary'
#     request_completed = False
#     try:
#         content = requests.get(url, timeout=10)
#         request_completed = True
#         result = content.json()['data']
#     except requests.exceptions.RequestException as e:
#         # https://stackoverflow.com/a/16511493
#         print('abbflow Request exception: %s ' % e.__str__())
#
#     return result
