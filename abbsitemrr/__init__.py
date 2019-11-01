from pymongo import MongoClient


class AbbSiteMRR:

    def __init__(self, name: str = '') -> None:
        host = '10.100.20.25'
        uri = "mongodb://%s" % host
        self.client = MongoClient(uri)
        self.db = self.client['abb']
        self.mrr = self.db['data_mrr']
        self.name = name
        self.record = None
        try:
            records = self.mrr.find({"_id": self.name})
            if records.count() > 0:
                self.record = records[0]
        except Exception as e:
            s = 'Exception occurred. ' + e.__str__()
            print(s)

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
