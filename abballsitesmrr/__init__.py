from abbsitemrr import AbbSiteMRR
from abbsites import AbbSites


class AbbAllSitesMRR:

    def __init__(self):
        self.sites = AbbSites()
        self.data = []
        sitemrr = AbbSiteMRR()
        for s in self.sites.names:
            sitemrr.set_name(name=s)
            if sitemrr.record is None:
                pass
            else:
                self.data.append(sitemrr.record)

        self.data.sort(key=lambda x: x['site'])

        return
