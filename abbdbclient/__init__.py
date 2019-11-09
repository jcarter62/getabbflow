from pymongo import MongoClient


class AbbDbClient:

    def __init__(self):
        host = '10.100.20.25'
        uri = "mongodb://%s" % host
        self.client = MongoClient(uri)
        self.db = self.client['abb']
        self.data = self.db['data']
        self.mrr = self.db['data_mrr']
        return

    def __del__(self):
        self.mrr = None
        self.data = None
        self.db = None
        self.client = None
        return
