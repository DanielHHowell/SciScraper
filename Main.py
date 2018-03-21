import PageScraper
import ReportGenerator
import sqlbackend
from collections import OrderedDict


def sciscraper(topic,queries,nResults,sortby):
    PMCIDs, query = [PMC for PMC in PageScraper.esearch(topic, queries, nResults, sortby)]
    mainDict = OrderedDict((PMC, PageScraper.esummary(PMC)) for PMC in PMCIDs)
    for PMC in mainDict:
        mainDict[PMC]['Images'] = PageScraper.image_scraper(PMC)
    return mainDict, query

def sql_insert():
    sqlbackend.create_table()
    for i in g.mainDict:
        ref = g.mainDict[i]
        sqlbackend.insert(g.query, i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']),
                          ref['Date'], ref['Abstract'], ', '.join(ref['Images']))
    return
