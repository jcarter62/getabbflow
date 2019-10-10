import threading
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import arrow
import time


class GetAbbFlow():
    """
    A class used to obtain flow values from an ABB SM500 paperless recorder.

    Attributes:
    site: str
        name of site
    address: str
        ip address or fqdn
    url: str
        calculated url used to request the flow values
    data: list of objects
        the result of requesting the flow values

    Methods:

    """

    site = ''
    address = ''
    url = ''
    data = list()
    timestamp_float = 0
    timestamp_utc = ''
    timestamp_local = ''

    _html_content = ''
    tbls = None
    bs = None
    driver = None

    result = {}
    barrel = ''
    value = 0.0

    total = 0.0
    agrigate_data = {}
    url = ''

    def __init__(self, address, site='') -> None:
        ts = arrow.utcnow()
        self.timestamp_float = ts.float_timestamp
        self.timestamp_utc = ts.format('YYYY-MM-DD HH:mm:ss')
        self.timestamp_local = ts.to('local').format('YYYY-MM-DD HH:mm:ss ZZ')
        self.address = address
        self.site = site
        url = self.build_url(address)
        self.url = url
        self.load_data()

    def build_url(self, address):
        # Example url:
        # http://13l.recorder.wwd.local/isapiext.dll/?100000101
        prefix = 'http://'
        postfix = '/isapiext.dll/?100000101'
        self.url = prefix + address + postfix
        return self.url

    def last_numeric_char(self, s):
        """Determine the position of the last numeric type character in a string."""
        keep = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.'}
        i = 0
        not_done = True
        while not_done:
            if s[i] in keep:
                i += 1
            else:
                not_done = False

            if i >= len(s):
                not_done = False
        return i

    def smart_trim(self, s):
        '''
        Trim string, and then return only only the first word.
        The first word is the float value contained.
        '''
        trm = s.strip().lstrip()
        pos = self.last_numeric_char(trm)
        result = s[0:pos]
        return result

    def extract_row(self, s):
        '''Extract data from the html table row, and send back as an object.'''
        self.result = {
            "site": self.site,
            "utc": self.timestamp_utc,
            "local": self.timestamp_local,
            "tag": "",
            "value": 0.0}
        self.barrel = s.contents[3].text
        self.value = float(self.smart_trim(s.contents[5].text))
        if self.value < -10:
            self.value = 0.0
        self.result['tag'] = self.barrel
        self.result['value'] = self.value
        return self.result

    def save_result(self, oneRowData):
        self.data.append(oneRowData)
        return

    def load_data(self):
        options = Options()
        options.add_argument('--headless')
        chrome_driver_path = os.path.join(os.path.abspath('.'), 'chromedriver')
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
        self.driver.get(self.url)

        time.sleep(5)
        self._html_content = self.driver.page_source.replace('&nbsp;', ' ')
        self.bs = bs4.BeautifulSoup(self._html_content, features='html.parser')

        self.tbls = self.bs.select('table')

        self.data = list()
        for t in self.tbls:
            try:
                if t.attrs['border'] == '2' and t.attrs['width'] == '100%':
                    # We found the data table, now extract the data.
                    for row in t.contents[1].contents:
                        datarow = str(type(row)).__contains__('element.Tag')
                        if datarow:
                            if ' BRL' in row.text:
                                rowdata = self.extract_row(row)
                                self.save_result(rowdata)
            except:
                pass

        self.driver.quit()
        self.calculate_agrigate()
        return

    def calculate_agrigate(self):
        """Calculate the total flow for all channels"""
        self.total = 0.0
        for rec in self.data:
            self.total = self.total + rec["value"]

        self.agrigate_data = {
            "site": self.site,
            "utc": self.timestamp_utc,
            "local": self.timestamp_local,
            "tag": "TOTAL",
            "value": self.total}
        self.data.append(self.agrigate_data)
