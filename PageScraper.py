import requests
from bs4 import BeautifulSoup
from lxml import html

def image_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    img_links = data.xpath('//img[@class="small-thumb"]/@src-large')
    if len(img_links) > 0:
        img_URLS = ['https://www.ncbi.nlm.nih.gov/'+i for i in img_links]
    else:
        img_links.append('blank')
    return img_URLS


def text_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    text_data = data.xpath('//*[@id="P1"]/text()')
    if not text_data:
        text_data = data.xpath('//*[@id="__p1"]/text()')
    if not text_data:
        text_data = data.xpath('//*[@id="__p4"]/text()')
    if not text_data:
        text_data = data.xpath('//*[@id="Par1"]/text()')
    if not text_data:
        text_data = data.xpath('//*[@id="Par1"]/text()[1]')
    if not text_data:
        text_data.append('blank')
    formatted_text=str(text_data)[1:-1]
    return formatted_text


def test():
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5625021/'
    r = requests.get(base_url)
    data = html.fromstring(r.content)
    #text_data = data.xpath('//*[@id="__p4"]/text()')
    text_data = data.xpath('//*[@id="P1"]/text()')
    if not text_data:
        text_data = data.xpath('//*[@id="__p4"]/text()')

    print(text_data)

