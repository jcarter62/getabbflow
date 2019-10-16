import arrow
import requests
from requests.exceptions import Timeout
import os


class AbbAcFt:

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

    def load_data(self):
        print('Requesting data from %s at %s' % (self.site, self.url))
        request_completed = False
        try:
            self.content = requests.get(self.url, timeout=4)
            request_completed = True
        except Timeout:
            print('Request %s timeout' % self.site)

        if request_completed:
            if self.acft_exists(self.content.text):
                self.data = self.get_acft_data(self.content.text)
        return

    def build_url(self, address) -> str:
        # Example url:
        # http://13l.recorder.wwd.local/isapiext.dll/?100000502
        prefix = 'http://'
        postfix = '/isapiext.dll/?100000502'
        self.url = prefix + address + postfix
        return self.url

    def acft_exists(self, c) -> bool:
        if 'tbat0.inner' in c:
            return True
        else:
            return False

    def get_acft_data(self, c) -> list():
        result = list()
        tags = [
            {'tag': 'tbat0.inner', 'id': 'A'},
            {'tag': 'tbat2.inner', 'id': 'B'},
            {'tag': 'tbat4.inner', 'id': 'C'},
            {'tag': 'tbat6.inner', 'id': 'D'},
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

    def get_first_word(self, s):
        result = ''
        numchars = ['-', '+', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ]
        ptr = 0
        while (ptr < len(s)) and (s[ptr] in numchars):
            result = result + s[ptr]
            ptr += 1

        return result
