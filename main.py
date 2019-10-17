from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os, json
from abbdata import AbbData

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    site_names = load_sites_from_file()
    return render_template('home.html', context={'sites': site_names})


def load_sites_from_file():
    filename = os.path.join(os.path.abspath('.'), 'data.json')
    with open(filename, 'r') as f:
        data = json.load(f)

    result = []
    for s in data['sites']:
        if s['abb']['urlname'] > '':
            result.append(s['name'])

    return result
