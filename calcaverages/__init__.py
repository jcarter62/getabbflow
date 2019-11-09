from abbsitemrr import AbbSiteMRR
from abbdbclient import AbbDbClient


class CalcAverages:

    def __init__(self, site: str):
        self.site = site
        site_mrr = AbbSiteMRR(name=self.site)
        self.mrr = site_mrr.record
        self.t5min = 0
        self.avg5min = 0.0
        del site_mrr
        if self.mrr != None:
            self.calc_5min()
        return

    def calc_5min(self):
        client = AbbDbClient()
        db = client.mrr
        records = db.find({"_id": self.site})
        if records.count() > 0:
            record = records[0]
            self.t5min = record['t5min']

        records = []
        db_detail = client.data
        if self.t5min > 0:
            # we have a valid t5min value, now get all data records
            # and agrigate for an average.
            records = db_detail.find({"site": self.site, "t5min": self.t5min})

        sumflow = 0.0
        avgflow = 0.0
        if records:
            for r in records:
                for f in r['flow']:
                    if f['tag'] < 'E':
                        sumflow += f['value']
            avgflow = sumflow / records.count()
            s = f'Site: {self.site}, Records: {records.count()}, Avg Flow: {avgflow}'
        else:
            s = f'Site: {self.site}, No Records'

        self.avg5min = avgflow

        print(s)
