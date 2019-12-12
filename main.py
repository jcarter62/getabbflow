import logging
import os

import arrow
from flask import Flask, render_template, send_from_directory, request
from flask_bootstrap import Bootstrap

from abballsitesmrr import AbbAllSitesMRR
from abbsitemrr import AbbSiteMRR
from abbsites import AbbSites
from logdir import LogFile

app = Flask(__name__)
bootstrap = Bootstrap(app)

logfile = LogFile(app_name='abbui')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_file_handler = logging.FileHandler(filename=logfile.full_path)
logger.addHandler(log_file_handler)

app.logger = logger


@app.route('/favicon.ico')
def favicon():
    log(request)
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/')
def home_route():
    log(request)
    sites = AbbSites()
    all_mrr = AbbAllSitesMRR().data
    total = 0.0
    for mrr in all_mrr:
        if mrr['state'] == 'ok':
            mrr['tflowfmt'] = ('%10.2f' % mrr['tflow']).lstrip(' ') + 'cfs'
            total += mrr['tflow']
        else:
            mrr['tflowfmt'] = '-'
        mrr['age'] = calc_age(mrr)
        mrr['title'] = calc_title(mrr)
        mrr['site'] = mrr['site'].rstrip(' ')

    total_str = ('%10.2f' % total).lstrip(' ') + 'cfs'
    #
    # Now let's go get the current orders from wmis database.
    #
    orders = get_orders_summary()
    for o in orders:
        o['latname'] = sites.find_sort_name(o['latname'])

    for mrr in all_mrr:
        mrr['orders'] = '--'
        for o in orders:
            if o['latname'] == mrr['site']:
                mrr['orders'] = o['flow']
                break

    return render_template('home.html', context={'data': all_mrr, 'total': total_str})


def calc_title(record) -> str:
    result = ''
    current_time = arrow.utcnow().timestamp
    age = current_time - record['t0']
    result = 'Record Age in Seconds %d, State = %s ' % (age, record['state'])
    return result


def calc_age(record) -> str:
    current_time = arrow.utcnow().timestamp
    age = current_time - record['t0']
    if age < 120:
        result = '0'
    elif age < 240:
        result = '1'
    elif age < 360:
        result = '2'
    elif age < 480:
        result = '3'
    else:
        result = '4'

    result = 'age' + result
    return result


@app.route('/map')
def route_map():
    log(request)
    return render_template('map.html', context={})


@app.route('/site/<site>')
def route_site_recent(site):
    log(request)
    one_site = AbbSiteMRR()
    one_site.set_name(site)
    flow = one_site.tflow()
    timestamp = one_site.local()
    data = one_site.record
    comb = []
    #
    for row in data['flow']:
        tag = row['tag']
        cfs = row['value']
        acft = acft4tag(data['acft'], tag)
        comb.append({'tag': tag, 'acft': acft, 'cfs': cfs})

    sites = AbbSites()
    this_site = sites.find_user_name(site)
    orders = get_orders_detail(this_site)

    obj = {'flow': flow, 'timestamp': timestamp, 'data': data, 'site': site, 'combined': comb, 'orders': orders}
    return render_template('site.html', context=obj)


def cfs4tag(rows, tag) -> float:
    for row in rows:
        if row['tag'] == tag:
            return row['value']
    return 0


def acft4tag(rows, tag):
    for row in rows:
        if row['tag'] == tag:
            return row['value']
    return '-'


def get_orders_summary():
    import requests
    result = []
    filename = os.path.join(os.path.abspath('.'), 'abborders_url.json')

    url = abb_orders_url() + 'orders_summary'
    request_completed = False
    try:
        content = requests.get(url, timeout=10)
        request_completed = True
        result = content.json()['data']
    except requests.exceptions.RequestException as e:
        # https://stackoverflow.com/a/16511493
        print('abbflow Request exception: %s ' % e.__str__())

    return result


def get_orders_detail(site):
    import requests
    result = []
    url = abb_orders_url() + 'order_detail/' + site
    request_completed = False
    try:
        content = requests.get(url, timeout=10)
        request_completed = True
        result = content.json()['data']
    except requests.exceptions.RequestException as e:
        # https://stackoverflow.com/a/16511493
        print('abbflow Request exception: %s ' % e.__str__())
    return result


def abb_orders_config_filename():
    import os
    filename = os.path.join(os.path.abspath('.'), 'abborders_url.json')
    return filename


def abb_orders_url():
    import json
    filename = abb_orders_config_filename()
    try:
        with open(filename, 'r') as f:
            results = json.load(f)
    except Exception as e:
        results = {"url": "http://localhost:5200/"}

    return results['url']


def log(req):
    import arrow
    now_string = arrow.now().format("YYYY/MM/DD-HH:mm:ss")
    obj = {
        'stamp': now_string,
        'url': req.path,
        'ip': req.remote_addr,
        'agent': req.user_agent,
    }

    new_file = LogFile(app_name='abbui').full_path
    current_file = app.logger.handlers[0].baseFilename
    if current_file != new_file:
        handler = app.logger.handlers[0]
        app.logger.removeHandler(hdlr=handler)
        handler = logging.FileHandler(filename=new_file)
        app.logger.addHandler(handler)

    logger.info('%(ip)s %(stamp)s %(url)s %(agent)s' % obj)

    return
