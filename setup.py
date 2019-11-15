def clear():
    from os import system, name, getenv

    _term = getenv('TERM')
    if getenv('TERM') is None:
        pass
    else:
        if name == 'nt':
            # for windows
            _ = system('cls')
        else:
            # for mac and linux(here, os.name is 'posix')
            _ = system('clear')


def user_input(msg, def_val) -> str:
    result = def_val
    s = '%s (%s):' % (msg, def_val)
    inp = input(s)
    if inp != '':
        result = inp
    return result


def config_filename():
    import os
    filename = os.path.join(os.path.abspath('.'), 'db.json')
    return filename


def load_config():
    import json
    filename = config_filename()
    try:
        with open(filename, 'r') as f:
            db_obj = json.load(f)
    except Exception as e:
        # Assume, we do not have a file, create a default object.
        db_obj = {"host": "localhost", "port": 27017}

    r1 = db_obj['host']
    r2 = db_obj['port']
    return r1, r2, db_obj


def save_config(obj):
    import json
    filename = config_filename()
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)


host, port, db_obj = load_config()

clear()
host = user_input(msg='Please provide Mongo DB Host Address', def_val=host)
port = user_input(msg='Please provide Mongo DB Port', def_val=port)

db_obj['host'] = host
db_obj['port'] = port

if user_input(msg='Update config file ? ', def_val='yes') == 'yes':
    save_config(db_obj)

save_config(db_obj)
