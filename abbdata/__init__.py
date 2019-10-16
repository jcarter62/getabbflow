from abbflow import AbbFlow
from abbacft import AbbAcFt


class AbbData:

    def __init__(self, address, site='') -> None:
        self.address = address
        self.site = site
        self.data = {
            'site': site,
            'acft': {},
            'flow': {}
        }
        self.load_data()

    def load_data(self):
        flow = AbbFlow(address=self.address, site=self.site)
        acft = AbbAcFt(address=self.address, site=self.site)
        self.data['acft'] = acft.data
        self.data['flow'] = flow.data
