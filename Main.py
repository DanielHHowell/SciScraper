import requests
import xmltodict
import sqlbackend

#PMC Portion
#Codes input into PMC-friendly search terms with a main topic AND an OR query


class Global:
    def __init__(self):
        pass
g = Global()


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



def efetch():
    #Retrieves relevant data into an OrderedDict formatted from server's XML
    baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id='
    search = baseURL + ','.join(g.PMCIDs) + '&rettype=report_type&retmode=xml'
    r = requests.get(search)
    xmldata = xmltodict.parse(r.text)

    #Sends data into nested-dict to be stored in the SQL-side, looping through each article
    g.mainDict = {}
    for i in xmldata['pmc-articleset']['article']:
        article_data = i['front']['article-meta']
        PMC = article_data['article-id'][1]['#text']
        g.mainDict[PMC] = {}

        #DOI information
        reference = article_data['article-id']
        if len(reference)==4:
            DOI = reference[3]['#text']
            g.mainDict[PMC]['DOI'] = DOI
        else:
            DOI = reference[2]['#text']
            g.mainDict[PMC]['DOI'] = DOI

        #Title
        title_location = article_data['title-group']['article-title']
        if type(title_location)==str:
            g.mainDict[PMC]['Title']=title_location
        else:
            g.mainDict[PMC]['Title']=title_location['#text']

        #Authors - requires ELIF tree due to format variation in in whether ['contrib-group'] and ['contrib'] contains a list or dict
        name_location = article_data['contrib-group']
        g.mainDict[PMC]['Authors'] = []

        if type(name_location) == list:
            for j in name_location:
                try:
                    lastname = j['contrib']['name']['surname']
                    firstname = j['contrib']['name']['given-names']
                    fullname = ' '.join((firstname, lastname))
                    g.mainDict[PMC]['Authors'].append(fullname)
                    #contrib-group is list and contrib is dic
                except:
                    for k in j['contrib']:
                        lastname = k['name']['surname']
                        firstname = k['name']['given-names']
                        fullname = ' '.join((firstname, lastname))
                        g.mainDict[PMC]['Authors'].append(fullname)
                        #contrib-group is list and contrib is list

        else:
            for j in name_location['contrib']:
                lastname = j['name']['surname']
                firstname = j['name']['given-names']
                fullname = ' '.join((firstname,lastname))
                g.mainDict[PMC]['Authors'].append(fullname)
                #contrib-group is dic and contrib is list

        #Date (annoying conditional location)

        date_location = article_data['pub-date']

        if len(date_location[0])==4:
            year = date_location[0]['year']
            month = date_location[0]['month']
            day = date_location[0]['day']
            pub_date = '.'.join((day, month, year))
            g.mainDict[PMC]['Date'] = pub_date

        elif len(date_location[1])==4:
            year = date_location[1]['year']
            month = date_location[1]['month']
            day = date_location[1]['day']
            pub_date = '.'.join((day, month, year))
            g.mainDict[PMC]['Date'] = pub_date

        elif len(date_location[2])==4:
            year = date_location[2]['year']
            month = date_location[2]['month']
            day = date_location[2]['day']
            pub_date = '.'.join((day, month, year))
            g.mainDict[PMC]['Date'] = pub_date


            #Keywords
        #mainDict[PMC]['Keywords'] = []
        #keywords_location = article_data['kwd-group']['kwd']
        #for j in keywords_location:
        #    print(j)
        #    mainDict[PMC]['Keywords'].append(j)


def sql_insert():
    sqlbackend.create_table()
    for i in g.mainDict:
        ref = g.mainDict[i]
        sqlbackend.insert(i, ref['DOI'], ref['Title'], ', '.join(ref['Authors']), ref['Date'])
    print(sqlbackend.view())

esearch()
efetch()
sql_insert()