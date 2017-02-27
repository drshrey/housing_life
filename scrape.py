import requests
import sys
from bs4 import BeautifulSoup
import json


def extract_listings(parsed):
    listings = parsed.find_all('p', class_='result-info')
    with open('listings.json', 'w') as outfile:
        for listing in listings:
            price = int(listing.find(class_='result-price').string[1:])
            size = listing.find(class_='housing')
            if size is not None:
                size = size.text.replace(' ', '').replace('\n', '')
            else:
                size = ''
            title = listing.find(class_='result-title')
            if title is not None:
                title = title.string
            else:
                title = ''
            hood = listing.find(class_='result-hood')
            if hood is not None:
                hood = hood.text
            else:
                hood = ''
            datetime= listing.find(class_='result-date')
            if datetime is not None:
                datetime = datetime.attrs['datetime']
            else:
                datetime = ''
            pid = listing.find(class_='result-title')
            if pid is not None:
                pid = pid.attrs['data-id']
            else:
                pid = ''
            href = listing.find(class_='result-title')
            if href is not None:
                href = href.attrs['href']
            else:
                href = ''
            data = {
                'price': price,
                'size': size,
                'title': title,
                'hood': hood,
                'datetime': datetime,
                'pid': pid,
                'href': href
            }
            json.dump(data, outfile)
    return listings

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

def fetch_search_results(*args, **kwargs):
    base = 'https://sfbay.craigslist.org/search/sfc/apa'
    with open('list.html', 'w') as list_html:
	for s in range(100, 1380, 100):
	    print('s value: {}'.format(s))
	    kwargs['s'] = s
	    resp = requests.get(base, params=kwargs, timeout=3)
	    resp.raise_for_status()  # <- no-op if status==200
	    list_html.write(resp.content)    
    html, encoding = read_search_results()
    return html, encoding


def read_search_results(*args, **kwargs):
    with open('list.html', 'r') as list_html:
        content = list_html.read()
        return (content, 'UTF-8')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results( \
	   min_price=4000, max_price=6000)
    # content = fetch_search_results(min_price=4000, max_price=6200)    
    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    print len(listings)
