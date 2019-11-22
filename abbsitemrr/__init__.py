from abbdbclient import AbbDbClient


class AbbSiteMRR:

    def __init__(self, name: str = '') -> None:
        self.client = AbbDbClient().client
        self.db = self.client['abb']
        self.mrr = self.db['data_mrr']
        self.name = name
        self.record = None
        self.all_records = self.mrr.find({})

        if name != '':
            self.set_name(name=name)

    def set_name(self, name: str = ''):
        for record in self.all_records:
            if record['site'] == name:
                self.record = record
                return
        # if we get here, there was no match
        self.record = None
        return

    def tflow(self):
        if self.record is None:
            result = None
        else:
            result = self.record['tflow']
        return result

    def local(self):
        if self.record is None:
            result = None
        else:
            result = self.record['local']
        return result
