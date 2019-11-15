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
            records = db_detail.find({"site": self.site, "t5min": self.t5min, "state": "ok"})

        sumflow = 0.0
        avgflow = 0.0
        self.avgrec = None
        if records:
            for r in records:
                self.add_to_avgrec(r)
                for f in r['flow']:
                    if f['tag'] < 'E':
                        sumflow += f['value']
            avgflow = sumflow / records.count()
            s = f'Site: {self.site}, Records: {records.count()}, Avg Flow: {avgflow}'
        else:
            s = f'Site: {self.site}, No Records'

        self.avg5min = avgflow

        print(s)

    def add_to_avgrec(self, rec):
        if self.avgrec is None:
            self.avgrec = {
                "site": self.site,
                "t5min": self.t5min,
                "count": 0,
                "A": {'min': 9999, 'max': -9999, "flow": 0.0, "flowsum": 0.0, 'use': 0.0},
                "B": {'min': 9999, 'max': -9999, 'use': 0.0},
                "C": {'min': 9999, 'max': -9999, 'use': 0.0},
                "D": {'min': 9999, 'max': -9999, 'use': 0.0},
                "flow": 0.0,
                "flowsum": 0.0
            }

        # now add this record to avgrec
        self.avgrec.count += 1
        for r in rec.acft:
            tag = r['tag']
            if r['value'] > self.avgrec[tag]['max']:
                self.avgrec[tag]['max'] = r['value']
            if r['value'] < self.avgrec[tag]['min']:
                self.avgrec[tag]['min'] = r['value']
