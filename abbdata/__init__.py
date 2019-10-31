from abbflow import AbbFlow
from abbacft import AbbAcFt
from abbsavedata import AbbSaveData
from timeutil import TimeUtil
import arrow


class AbbData:

    def __init__(self, address, site='') -> None:
        self.address = address
        self.site = site
        self.data = {
            'site': site,
            'state': '',
            't0': 0,
            't5min': 0,
            'qtrhr': 0,
            'qtrday': 0,
            'acft': {},
            'flow': {},
        }
        self.load_data()

    def load_data(self):
        flow = AbbFlow(address=self.address, site=self.site)
        acft = AbbAcFt(address=self.address, site=self.site)
        self.data['acft'] = acft.data
        self.data['flow'] = flow.data

        if acft.data.__len__() <= 0:
            state = 'error'
        else:
            state = 'ok'

        current_time = arrow.utcnow()
        tu = TimeUtil()
        self.data['t0'] = current_time.timestamp
        self.data['t5min'] = tu.t5min(current_time)
        self.data['qtrhr'] = tu.qtrhr(current_time)
        self.data['qtrday'] = tu.qtrday(current_time)
        self.data['local'] = current_time.to('local').format('YYYY-MM-DD HH:mm:ss ZZ')

        self.data['state'] = state
        self.data['tflow'] = self.get_flow_total()

    #        self.save_data()

    def get_flow_total(self):
        result = 0
        for r in self.data['flow']:
            if r['tag'] == 'TOTAL':
                result = r['value']
        return result


    def save_data(self):
        db = AbbSaveData()
        key = f'%-15s - %d' % (self.site, self.data['t0'])
        db.save_record(key=key, data=self.data)
        return
