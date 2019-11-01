from abbsitemrr import AbbSiteMRR
from abbsites import AbbSites


class AbbAllSitesMRR:

    def __init__(self):
        self.sites = AbbSites()
        self.data = []
        for s in self.sites.names:
            mrr = AbbSiteMRR(name=s)
            if mrr.record is None:
                pass
            else:
                self.data.append(mrr.record)

        self.data.sort(key=lambda x: x['site'])

        return
