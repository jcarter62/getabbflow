from couchdb import client, Server, HTTPError


class AbbSaveData:

    def __init__(self) -> None:
        self.server = Server('http://abbadmin:password@10.100.20.230:5984')
        if 'abb' in self.server:
            self.db = self.server['abb']
        else:
            self.db = self.server.create('abb')
        super().__init__()

    def save_record(self, key, data):
        # determine if record exists.
        record = self.db.get(id=key)

        if record is None:
            local_record = data
            local_record['_id'] = key
            self.db.save(local_record)
        else:
            local_record = data
            local_record['_id'] = key
            local_record['_rev'] = record.rev
            self.db.save(data)

        return
