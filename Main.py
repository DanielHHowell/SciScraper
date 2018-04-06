import PageScraper
import ReportGenerator
import sqlbackend
import KeywordAnalysis
from collections import OrderedDict


def sciscraper(topic,queries,nResults,sortby):
    PMCIDs, query = [PMC for PMC in PageScraper.esearch(topic, queries, nResults, sortby)]
    mainDict = OrderedDict((PMC, PageScraper.esummary(PMC)) for PMC in PMCIDs)
    for PMC in mainDict:
        mainDict[PMC]['Images'] = PageScraper.image_scraper(PMC)
    alltext = [KeywordAnalysis.text_grab(i) for i in PMCIDs]
    keywords = [i for i in KeywordAnalysis.get_continuous_chunks(" ".join(alltext)) if i != topic]
    return mainDict, query, keywords

def sql_insert(mainDict, query):
    sqlbackend.create_table()
    for i in mainDict:
        ref = mainDict[i]
        sqlbackend.insert(query, i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']),
                          ref['Date'], ref['Abstract'], ', '.join(ref['Images']))
    return
