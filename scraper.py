import csv

from bs4 import BeautifulSoup
import urllib



r = urllib.urlopen('http://sfbay.craigslist.org/sfc/sub/6016279510.html').read()
soup = BeautifulSoup(r)

