from abbdbclient import AbbDbClient


# from pymongo import MongoClient


class AbbSaveData:

    def __init__(self) -> None:
        self.db_client = AbbDbClient()
        self.db = self.db_client.db
        self.collection = self.db_client.data
        self.mrr = self.db_client.mrr
        # host = '10.100.20.25'
        # uri = "mongodb://%s" % host
        # print(uri)
        # self.client = MongoClient(uri)
        # self.db = self.client['abb']
        # self.collection = self.db['data']
        # self.mrr = self.db['data_mrr']
        super().__init__()

    def save_record(self, key, data):
        local_record = data
        local_record['_id'] = key
        try:
            print('find_one %s' % key)
            records = self.collection.find({"_id": key})
            this_record = None
            if (records.count() > 0):
                this_record = records[0]
            if this_record is None:
                self.collection.insert_one(local_record)
            else:
                self.collection.find_one_and_replace({"_id": key}, local_record)

            self.save_most_recent_record(local_record)

        except Exception as e:
            s = 'Exception occurred. ' + e.__str__()
            print(s)

        return

    def save_most_recent_record(self, data):
        local_record = data
        key = local_record['site']
        local_record['data_key'] = local_record['_id']
        local_record['_id'] = key

        try:
            records = self.mrr.find({"_id": key})
            this_record = None
            if records.count() > 0:
                this_record = records[0]

            if this_record is None:
                self.mrr.insert_one(local_record)
            else:
                self.mrr.find_one_and_replace({"_id": key}, local_record)

        except Exception as e:
            s = 'Exception occurred. ' + e.__str__()
            print(s)

        return
