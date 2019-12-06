from flask import Flask, render_template, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
import os, json
# from abbapi import AbbAPI
from abbsites import AbbSites
from abbsitemrr import AbbSiteMRR
from abballsitesmrr import AbbAllSitesMRR
import arrow

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/')
def home_route():
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
    return render_template('map.html', context={})


@app.route('/site/<site>')
def route_site_recent(site):
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
    url = 'http://localhost:5200/orders_summary'
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
    url = 'http://localhost:5200/order_detail/' + site
    request_completed = False
    try:
        content = requests.get(url, timeout=10)
        request_completed = True
        result = content.json()['data']
    except requests.exceptions.RequestException as e:
        # https://stackoverflow.com/a/16511493
        print('abbflow Request exception: %s ' % e.__str__())
    return result

# @app.route('/data/<site>')
# def site_route(site):
#     data = AbbAPI(site=site)
#     return render_template('site.html', context=data)


# @app.route('/getdata/<site>')
# def site_data(site):
#     data = AbbAPI(site=site)
#     return jsonify(data.data)



# def load_sites_from_file():
#     filename = os.path.join(os.path.abspath('.'), 'data.json')
#     with open(filename, 'r') as f:
#         data = json.load(f)
#
#     result = []
#     for s in data['sites']:
#         if s['abb']['urlname'] > '':
#             result.append(s['name'])
#
#     return result
