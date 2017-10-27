import requests
from bs4 import BeautifulSoup


def content_grab(PMC):
    baseURL = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC'
    r = requests.get(baseURL+str(PMC))
    soup = BeautifulSoup(r.content, 'html.parser')
    imgs = soup.findAll("div", {"class": "small-thumb"})
    for img in imgs:
        print(img.get('href'))
    #print(''.join(soup.body.h2.find_all_next(string=True)))
    #print(soup.text)

content_grab(5470759)
