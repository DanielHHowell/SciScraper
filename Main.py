import PageScraper
import ReportGenerator
import sqlbackend
import KeywordAnalysis
from collections import OrderedDict


def sciscraper(topic, queries, nResults, sortby):
    pmc_ids, query = [pmc for pmc in PageScraper.esearch(topic, queries, nResults, sortby)]
    main_dict = OrderedDict((pmc, PageScraper.esummary(pmc)) for pmc in pmc_ids)
    for pmc in main_dict:
        main_dict[pmc]['Images'] = PageScraper.image_scraper(pmc)
    alltext = [KeywordAnalysis.text_grab(i) for i in pmc_ids]
    keywords = [i for i in KeywordAnalysis.get_continuous_chunks(" ".join(alltext)) if i != topic]
    return main_dict, query, keywords


def sql_insert(main_dict, query):
    sqlbackend.create_table()
    for i in main_dict:
        ref = main_dict[i]
        sqlbackend.insert(query, i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']),
                          ref['Date'], ref['Abstract'], ', '.join(ref['Images']))
    return
