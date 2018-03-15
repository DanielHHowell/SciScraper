import requests
from lxml import html

def image_scraper(PMC):
    base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    search = base_url+PMC
    r = requests.get(search)
    data = html.fromstring(r.content)
    img_links = data.xpath('//img[@class="small-thumb"]/@src-large')
    img_URLs = []
    if len(img_links) > 0:
        img_URLs = ['https://www.ncbi.nlm.nih.gov/'+i for i in img_links]
    if len(img_URLs)>4:
        return img_URLs[1:4]
    return img_URLs


def text_scraper(PMC):
    """Retrieves abstract if unavailable in NCBI API"""
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
