from pymongo import MongoClient


class AbbSaveData:

    def __init__(self) -> None:
        self.uri = 'mongodb://10.100.20.25'
        self.client = MongoClient(self.uri)
        self.db = self.client['abb']
        self.collection = self.db['data']
        super().__init__()

    def save_record(self, key, data):
        x = ''
        local_record = data
        local_record['_id'] = key
        x = x + '1'
        try:
            print('find_one %s' % key)
            x = x + '2'
            records = self.collection.find({"_id": key})
            this_record = None
            if (records.count() > 0):
                this_record = records[0]
            x = x + '3'
            if this_record != None:
                x = x + '4'
                self.collection.find_one_and_replace(filter(key), local_record)
                x = x + '5'
            else:
                x = x + '6'
                self.collection.insert_one(local_record)
                x = x + '7'

        except Exception as e:

            s = 'Exception occurred. ' + x + ' ' + e.__str__()
            print(s)

        return
