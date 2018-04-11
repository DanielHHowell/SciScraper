from nltk import *
import requests
from bs4 import BeautifulSoup
from collections import Counter



def text_grab(PMC):
    url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"+PMC
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = ""

    #Grabs all the article text while ignoring the references section
    paragraphs = soup.find_all("div", "tsec sec")
    for i in paragraphs[:-1]:
        text+= ' '+i.text
    return text

def get_continuous_chunks(text):
    stopwords = ['et', 'al.', 'n', 'deviation', 'windowFigure', 'windowFig', ' ]',
                 'additional', 'data', 'file', ' ', 'distribution', 'significant',
                 'clinical', 'adverse', 'sample', 'studies', 'significance',
                 '<', '>', '=', 'window', 't', 't-test', 'supplementary', 'Supplementary', 'important'
                 'experimental', 'study', 'subjects', 'conditions', 'experiments']
    words = word_tokenize(text)
    filtered_text = [w for w in words if w not in stopwords]
    processed_text = pos_tag(filtered_text)

    #Regex to grammatically identify a set of: adjective+noun(+noun)
    #From NLTK: JJ* = adjective/numeral/ordinal/comparative/superlative, NN* = Nouns
    chunkGram = r"Chunk: {<JJ.?><NN.?>?<NN.?>}"
    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(processed_text)
    keywords = [i.leaves() for i in chunked if type(i)==Tree]
    newkeys = []

    for list in keywords:
        if len(list)<2:
            newkeys.append(list[0][0])
        else:
            temp = []
            for tuple in list:
                temp.append(tuple[0])
            newkeys.append(" ".join(temp))

    counted = Counter(newkeys).most_common(11)
    keywords = [i[0] for i in counted]
    return keywords



