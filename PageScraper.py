import requests
from lxml import html
import xmltodict
from xml.etree.ElementTree import fromstring


def esearch(topic_input, queries, nResults, sortby):

    # Formats the terms for the API search
    topic = '%22' + topic_input.replace(' ', '+') + '%22'
    if queries:
        query_terms = [i.strip() for i in queries.split(',')]
        boolean_queries = '+OR+'.join(query_terms)
        search_terms = topic + '+AND+%28' + boolean_queries + '%29'
    else:
        search_terms = topic

    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&sort=' + sortby + '&retmax=' + nResults + '&term='
    r = requests.get(base_url + search_terms)
    xmldict = xmltodict.parse(r.content)
    PMCIDs = [i for i in xmldict['eSearchResult']['IdList']['Id']]

    # Formats the search  for use in the report title, returning 'query'
    printable_search = topic_input
    if queries:
        printable_search += ':'
        for i in query_terms:
            printable_search += ' ' + i + ','
        printable_search = printable_search[:-1]
    query = printable_search.title()

    return PMCIDs, query


def efetch(pmc):

    # eSummary returns most all of this data more succinctly, leaving here if necessary later
    # Retrieves relevant data into an OrderedDict formatted from server's XML
    # eFetch can return (retmode) either xml or medline
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search = base_url + pmc + '&rettype=report_type&retmode=xml'
    r = requests.get(search, stream=True)
    data = fromstring(r.content)
    pmc = {}

    for i in data.iter(tag='article-id'):
        if i.attrib['pub-id-type'] == "doi":
            pmc['DOI'] = i.text
    for i in data.iter(tag='title-group'):
        pmc['Title'] = i.find('article-title').text
    pmc['Authors'] = []
    for i in data.iter(tag='contrib'):
        if i.attrib['contrib-type'] == "author":
            for j in i.findall('name'):
                surname = j.find('surname').text
                given_name = j.find('given-names').text
                full_name = ' '.join((given_name, surname))
                pmc['Authors'].append(full_name)
    for i in data.iter(tag='pub-date'):
        if i.attrib['pub-type'] == "epub":
            day = i.find('day').text
            month = i.find('month').text
            year = i.find('year').text
            pub_date = '.'.join((day, month, year))
            pmc['Date'] = pub_date


def esummary(pmc):

    # Retrieves the Date, Authors, Title and DOI from the API's XML report
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id='
    search = base_url + pmc + '&retmode=report_type&rettype=xml'
    r = requests.get(search, stream=True)
    tree = fromstring(r.content)
    pmc_data = {'Date': tree[0][1].text, 'Authors': [author.text for author in tree[0][4]],
                'Title': tree[0][5].text.title(), 'DOI': tree[0][10].text}

    # Retrieves the abstract from the Medline version of the API report
    abstract_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search_abstract = abstract_url + pmc + '&retmode=report_type&rettype=medline'
    r2 = requests.get(search_abstract).text
    abstract = r2[r2.find('AB') + 6:r2.find('FAU')]
    pmc_data['Abstract'] = " ".join(abstract.split())
    pmc_data['Link'] = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC' + pmc

    return pmc_data


def image_scraper(pmc):

    # Retrieves images 2-4 from the public-facing article URL
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url + pmc
    r = requests.get(search)
    data = html.fromstring(r.content)
    img_links = data.xpath('//img[@class = "tileshop"]/@src|//img[@class = "fig-image"]/@src')
    img_urls = ['https://www.ncbi.nlm.nih.gov/' + i for i in img_links if img_links][1:4]
    return img_urls
