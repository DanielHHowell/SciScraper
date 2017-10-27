import requests
import sqlbackend
from lxml import html
import xml.etree.ElementTree as ET

#PMC Portion
#Codes input into PMC-friendly search terms with a main topic AND an OR query


class Global:
    def __init__(self):
        pass
g = Global()

g.mainDict = {}

def esearch():
    topic_input = input()
    topic = topic_input.replace(' ','+')
    queries = input()
    nResults = input()
    if queries:
        query_terms = [i.strip() for i in queries.split(',')]
        boolean_queries = '+OR+'.join(query_terms)
        search_terms = topic+'+AND+('+boolean_queries+')'
    else:
        search_terms=topic
    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&retmax='+nResults+'&term='
    r = requests.get(baseURL+search_terms)
    xmldict = xmltodict.parse(r.content)
    g.PMCIDs = [i for i in xmldict['eSearchResult']['IdList']['Id']]
    print(g.PMCIDs)



def efetch(PMC):
    #Retrieves relevant data into an OrderedDict formatted from server's XML
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

def sql_insert():
    sqlbackend.create_table()
    for i in g.mainDict:
        ref = g.mainDict[i]
        sqlbackend.insert(i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']), ref['Date'])
    print(sqlbackend.view())

esearch()
for PMC in g.PMCIDs:
    print(PMC)
    #efetch(PMC)

print(g.mainDict)
#sql_insert()
