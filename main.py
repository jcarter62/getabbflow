from flask import Flask, render_template, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
import os, json
from abbapi import AbbAPI

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/')
def home_route():
    site_names = load_sites_from_file()
    return render_template('home.html', context={'sites': site_names})


@app.route('/data/<site>')
def site_route(site):
    data = AbbAPI(site=site)
    return render_template('site.html', context=data)


@app.route('/getdata/<site>')
def site_data(site):
    data = AbbAPI(site=site)
    return jsonify(data.data)

def load_sites_from_file():
    filename = os.path.join(os.path.abspath('.'), 'data.json')
    with open(filename, 'r') as f:
        data = json.load(f)

    result = []
    for s in data['sites']:
        if s['abb']['urlname'] > '':
            result.append(s['name'])

    return result
