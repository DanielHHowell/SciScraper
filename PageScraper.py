import requests
from lxml import html
import xmltodict
import xml.etree.ElementTree as ET



def esearch(topic_input, queries, nResults, sortby):

    topic = '%22'+topic_input.replace(' ','+')+'%22'
    nResults = nResults

    if queries:
        query_terms = [i.strip() for i in queries.split(',')]
        boolean_queries = '+OR+'.join(query_terms)
        search_terms = topic+'+AND+%28'+boolean_queries+'%29'
    else:
        search_terms=topic

    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&sort='+sortby+'&retmax='+nResults+'&term='
    r = requests.get(baseURL+search_terms)
    xmldict = xmltodict.parse(r.content)
    PMCIDs = [i for i in xmldict['eSearchResult']['IdList']['Id']]

    #Formats the search nicely for use in the report
    printable_search = topic_input
    if queries:
        printable_search += ':'
        for i in query_terms:
            printable_search += ' '+i+','
        printable_search = printable_search[:-1]
    query = printable_search.title()

    return PMCIDs, query




def efetch(PMC):
    #eSummary returns most all of this data more succinctly, leaving here if necessary later
    #Retrieves relevant data into an OrderedDict formatted from server's XML
    #eFetch can return (retmode) either xml or medline

    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search = baseURL + PMC + '&rettype=report_type&retmode=xml'
    r = requests.get(search, stream=True)
    data = ET.fromstring(r.content)
    PMC = {}


    for i in data.iter(tag='article-id'):
        if i.attrib['pub-id-type'] == "doi":
            PMC['DOI']=i.text

    for i in data.iter(tag='title-group'):
        PMC['Title']= i.find('article-title').text

    PMC['Authors'] = []
    for i in data.iter(tag='contrib'):
        if i.attrib['contrib-type'] == "author":
            for j in i.findall('name'):
                surname = j.find('surname').text
                given_name = j.find('given-names').text
                full_name = ' '.join((given_name,surname))
                PMC['Authors'].append(full_name)


    for i in data.iter(tag='pub-date'):
        if i.attrib['pub-type'] == "epub":
         day = i.find('day').text
         month = i.find('month').text
         year = i.find('year').text
         pub_date = '.'.join((day, month, year))
         PMC['Date'] = pub_date

def esummary(PMC):

    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id='
    search = baseURL + PMC + '&retmode=report_type&rettype=xml'
    r = requests.get(search, stream=True)
    tree = ET.fromstring(r.content)
    PMC_data = {}
    PMC_data['Date']=tree[0][1].text
    PMC_data['Authors'] = []
    for author in tree[0][4]:
        PMC_data['Authors'].append(author.text)
    PMC_data['Title']=tree[0][5].text.title()
    PMC_data['DOI']=tree[0][10].text


    abstract_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search_abstract = abstract_URL + PMC + '&retmode=report_type&rettype=medline'
    r2 = requests.get(search_abstract).text
    abstract = r2[r2.find('AB') + 6:r2.find('FAU')]
    PMC_data['Abstract'] = " ".join(abstract.split())
    PMC_data['Link'] = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC'+PMC
    return PMC_data

def image_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    img_links = data.xpath('//img[@class="tileshop"]/@src')
    img_URLs = ['https://www.ncbi.nlm.nih.gov/'+i for i in img_links if img_links][1:4]
    return img_URLs

