import os

import arrow


class LogDir:

    def __init__(self, app_name='logs'):
        import os
        application_name = app_name
        osname = os.name
        if osname == 'nt':
            _log_folder = os.path.join(os.getenv('APPDATA'), 'log', application_name)
        else:
            _log_folder = os.path.join(os.getenv('HOME'), '.log', application_name)

        os.makedirs(_log_folder, exist_ok=True)

        self.log_folder = _log_folder
        return


class LogFile:

    def __init__(self, app_name=''):
        if app_name == '':
            self.appname = 'app'
        else:
            self.appname = app_name

        self.filename = self.appname + '-' + self.get_time_stamp_string() + '.txt'
        log_dir = LogDir().log_folder
        self.full_path = os.path.join(log_dir, self.filename)
        return

    def get_time_stamp_string(self):
        now = arrow.now()
        fn = now.format('YYYYMMDD')
        return fn
