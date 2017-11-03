import requests
from bs4 import BeautifulSoup
from lxml import html

def image_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    img_links = data.xpath('//img[@class="small-thumb"]/@src-large')
    if len(img_links) < 1:
        img_links.append('blank')
    return img_links


def text_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    text_data = data.xpath('//p[@class="p p-first-last"]//text()')
    if len(text_data)<1:
        text_data.append('blank')
    return str(text_data)
