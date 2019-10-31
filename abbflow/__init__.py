import arrow
import requests
from requests.exceptions import Timeout
import os


class AbbFlow:

    def __init__(self, address, site='') -> None:
        ts = arrow.utcnow()
        self.timestamp_float = ts.float_timestamp
        self.timestamp_utc = ts.format('YYYY-MM-DD HH:mm:ss')
        self.timestamp_local = ts.to('local').format('YYYY-MM-DD HH:mm:ss ZZ')

        self.address = address
        self.site = site
        self.url = self.build_url(address)
        self.data = list()

        self.bs = None
        self.driver = None

        self.content = ''

        self.result = {}
        self.barrel = ''
        self.value = 0.0

        self.total = 0.0

        self.load_data()

    def build_url(self, address) -> str:
        # Example url:
        # http://13l.recorder.wwd.local/isapiext.dll/?100000102
        prefix = 'http://'
        postfix = '/isapiext.dll/?100000102'
        self.url = prefix + address + postfix
        return self.url

    def flow_exists(self, c) -> bool:
        if 'ain0.inner' in c:
            return True
        else:
            return False

    def get_first_word(self, s):
        result = ''
        numchars = ['-', '+', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ]
        ptr = 0
        while (ptr < len(s)) and (s[ptr] in numchars):
            result = result + s[ptr]
            ptr += 1

        return result

    def extract_tag_data(self, c, tag) -> str:
        quote = '"'
        result = ''
        tag_pos = c.find(tag)
        if tag_pos > 0:
            c_len = len(c)
            start = tag_pos + len(tag)
            while start < c_len and c[start] != quote:
                start += 1

            start += 1
            end = start + 1
            while end < c_len and c[end] != quote:
                end += 1

            # the quoted string after tag should be between
            # start and end
            result = self.get_first_word(c[start:end])

        return result

    def get_flow_data(self, c) -> list():
        result = list()
        tags = [
            {'tag': 'ain0.inner', 'id': 'A'},
            {'tag': 'ain2.inner', 'id': 'B'},
            {'tag': 'ain4.inner', 'id': 'C'},
            {'tag': 'ain6.inner', 'id': 'D'},
        ]
        for tag in tags:
            if tag['tag'] in c:
                flow = self.extract_tag_data(c, tag['tag'])
                try:
                    if len(flow) > 0:
                        flow = float(flow)
                    else:
                        flow = 0.0
                    if flow < -1:
                        flow = 0.0
                finally:
                    pass

                one = {
                    'site': self.site,
                    'utc': self.timestamp_utc,
                    'local': self.timestamp_local,
                    'tag': tag['id'],
                    'value': flow}
                result.append(one)

        return result

    def calculate_agrigate(self):
        """Calculate the total flow for all channels"""
        if len(self.data) > 0:
            self.total = 0.0
            for rec in self.data:
                self.total = self.total + rec["value"]

            self.agrigate_data = {
                "site": self.site,
                "utc": self.timestamp_utc,
                "local": self.timestamp_local,
                "tag": "TOTAL",
                "value": round(self.total, 3)}
            self.data.append(self.agrigate_data)

    def load_data(self):
        print('Requesting data from %s at %s' % (self.site, self.url))
        request_completed = False
        try:
            self.content = requests.get(self.url, timeout=20)
            request_completed = True
            self.save_html_content(self.site, self.content.text)
        except requests.exceptions.RequestException as e:
            # https://stackoverflow.com/a/16511493
            print('abbflow Request exception: %s ' % e.__str__())

        if request_completed:
            if self.flow_exists(self.content.text):
                self.data = self.get_flow_data(self.content.text)
                self.calculate_agrigate()
        return

    def save_html_content(self, site, content):
        _shortpath = site + '.html'
        _tempfile = os.path.join(os.path.abspath('.'), 'temp', _shortpath)
        with open(_tempfile, 'w') as f:
            f.write(content)
        return
