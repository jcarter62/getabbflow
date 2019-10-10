import requests
import bs4
from pandas.io.html import read_html
import lxml
import html5lib

page = 'http://13l.recorder.wwd.local/isapiext.dll/?100000101'


def get_page(url):
    _res = requests.get(page)
    _res.raise_for_status()
    _bs = bs4.BeautifulSoup(_res.text, features='html.parser')
    _htmlpage = _bs.contents
    result = _htmlpage
    return result


page_text = get_page(page)
tbl = read_html(page_text, attrs={"border": "2"}, flavor='bs4')

print("table")
