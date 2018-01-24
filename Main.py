import requests
import xmltodict
import sqlbackend
from lxml import html
import xml.etree.ElementTree as ET
import PageScraper
import ReportGenerator


#PMC Portion
#Codes input into PMC-friendly search terms with a main topic AND an OR query


class Global:
    def __init__(self):
        pass
g = Global()

g.mainDict = {}

def esearch(a,b,c):
    topic_input = a
    topic = "%22"+topic_input.replace(' ','+')+"%22"
    queries = b
    g.nResults = c

    if queries:
        query_terms = [i.strip() for i in queries.split(',')]
        boolean_queries = '+OR+'.join(query_terms)
        search_terms = topic+'+AND+%28'+boolean_queries+'%29'
    else:
        search_terms=topic
    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&sort=relevance&retmax='+g.nResults+'&term='
    r = requests.get(baseURL+search_terms)
    xmldict = xmltodict.parse(r.content)
    g.PMCIDs = [i for i in xmldict['eSearchResult']['IdList']['Id']]

    #Formats the search nicely for use in the report
    printable_search = topic_input

    if queries:
        printable_search += ':'
        for i in query_terms:
            printable_search += ' '+i+','
        printable_search = printable_search[:-1]

    g.query = printable_search.title()
    print(printable_search)




def efetch(PMC):
    #eSummary returns most all of this data more succinctly, leaving here if necessary later
    #Retrieves relevant data into an OrderedDict formatted from server's XML
    #eFetch can return (retmode) either xml or medline

    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search = baseURL + PMC + '&rettype=report_type&retmode=xml'
    r = requests.get(search, stream=True)
    data = ET.fromstring(r.content)
    g.mainDict[PMC] = {}


    for i in data.iter(tag='article-id'):
        if i.attrib['pub-id-type'] == "doi":
            g.mainDict[PMC]['DOI']=i.text

    for i in data.iter(tag='title-group'):
        g.mainDict[PMC]['Title']= i.find('article-title').text

    g.mainDict[PMC]['Authors'] = []
    for i in data.iter(tag='contrib'):
        if i.attrib['contrib-type'] == "author":
            for j in i.findall('name'):
                surname = j.find('surname').text
                given_name = j.find('given-names').text
                full_name = ' '.join((given_name,surname))
                g.mainDict[PMC]['Authors'].append(full_name)


    for i in data.iter(tag='pub-date'):
        if i.attrib['pub-type'] == "epub":
         day = i.find('day').text
         month = i.find('month').text
         year = i.find('year').text
         pub_date = '.'.join((day, month, year))
         g.mainDict[PMC]['Date'] = pub_date

def esummary(PMC):

    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id='
    search = baseURL + PMC + '&retmode=report_type&rettype=xml'
    r = requests.get(search, stream=True)
    tree = ET.fromstring(r.content)
    g.mainDict[PMC] = {}
    g.mainDict[PMC]['Date']=tree[0][1].text
    g.mainDict[PMC]['Authors'] = []
    for author in tree[0][4]:
        g.mainDict[PMC]['Authors'].append(author.text)
    g.mainDict[PMC]['Title']=tree[0][5].text
    g.mainDict[PMC]['DOI']=tree[0][10].text

    efetch_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search_abstract = efetch_URL + PMC + '&retmode=report_type&rettype=medline'
    r2 = requests.get(search_abstract).text
    abstract = r2[r2.find('AB') + 6:r2.find('FAU')]
    g.mainDict[PMC]['Abstract'] = " ".join(abstract.split())



def sql_insert():
    sqlbackend.create_table()
    for i in g.mainDict:
        ref = g.mainDict[i]
        sqlbackend.insert(g.query, i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']),
                          ref['Date'], ref['Abstract'], ', '.join(ref['Images']))


def sciscraper(a,b,c):
    esearch(a,b,c)
    for PMC in g.PMCIDs:
        esummary(PMC)
        g.mainDict[PMC]['Images'] = []
        for image in PageScraper.image_scraper(PMC):
            g.mainDict[PMC]['Images'].append(image)
    #ReportGenerator.markdown_generator(g.mainDict, g.query, g.nResults)
    #ReportGenerator.htmltest()
    return g.mainDict