from abbflow import AbbFlow
from abbacft import AbbAcFt
from abbsavedata import AbbSaveData


class AbbData:

    def __init__(self, address, site='') -> None:
        self.address = address
        self.site = site
        self.data = {
            'site': site,
            'state': '',
            'acft': {},
            'flow': {}
        }
        self.load_data()

    def load_data(self):
        flow = AbbFlow(address=self.address, site=self.site)
        acft = AbbAcFt(address=self.address, site=self.site)
        self.data['acft'] = acft.data
        self.data['flow'] = flow.data
        state = ''
        if acft.data.__len__() <= 0:
            state = 'error'
        else:
            state = 'ok'
        self.data['state'] = state
        self.save_data()

    def save_data(self):
        db = AbbSaveData()
        key = self.site
        db.save_record(key=key, data=self.data)
        return
