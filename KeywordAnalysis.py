from nltk import *
import requests
from bs4 import BeautifulSoup
from collections import Counter


def text_grab(pmc):
    url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC" + pmc
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_text = ""

    # Grabs all the article text while ignoring the references section
    paragraphs = soup.find_all("div", "tsec sec")
    for i in paragraphs[:-1]:
        article_text += ' ' + i.text
    return article_text


def get_continuous_chunks(article_text):
    stopwords = ['et', 'al.', 'n', 'deviation', 'windowFigure', 'windowFig', ' ]',
                 'additional', 'data', 'file', ' ', 'distribution', 'significant',
                 'clinical', 'adverse', 'sample', 'studies', 'significance',
                 '<', '>', '=', 'window', 't', 't-test', 'supplementary', 'Supplementary', 'important'
                                                                                           'experimental', 'study',
                 'subjects', 'conditions', 'experiments',
                 'control', 'panel']
    words = word_tokenize(article_text)
    filtered_text = [w for w in words if w not in stopwords]
    processed_text = pos_tag(filtered_text)

    # Regex to grammatically identify a set of: adjective+noun(+noun)
    # From NLTK: JJ* = adjective/numeral/ordinal/comparative/superlative, NN* = Nouns
    chunk_gram = r"Chunk: {<JJ.?><NN.?>?<NN.?>}"
    chunk_parser = RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(processed_text)
    keywords = [i.leaves() for i in chunked if type(i) == Tree]

    # NLTK returns chunks in the form of lists of tuples of the word and its pos tag
    newkeys = []
    for chunk in keywords:
        if len(chunk) < 2:
            newkeys.append(list[0][0])
        else:
            temp = []
            for pair in chunk:
                temp.append(pair[0])
            newkeys.append(" ".join(temp))

    counted = Counter(newkeys).most_common(11)
    keywords = [i[0] for i in counted]
    return keywords
