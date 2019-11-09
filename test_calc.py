from calcaverages import CalcAverages
from abbsites import AbbSites

sites = AbbSites().sites['sites']

for site in sites:
    siteavg = CalcAverages(site=site['name'])
