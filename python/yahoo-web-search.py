#!/usr/bin/env python
# yahoo-web-search.py
import cgi
import sys
import urllib
import xml.etree.ElementTree as etree

BASE_URI = 'http://api.search.yahoo.com/WebSearchService/V1/webSearch'

def print_page_titles(term):
    term = cgi.escape(term)
    uri = BASE_URI + "?appid=restbook&query=" + term
    response = urllib.urlopen(uri)

    doc = etree.parse(response.read())
    for title in doc.iter('/ResultSet/Result/Title/[]'):
        print(title)

if not sys.argv[1:]:
    print('Usage: {0} [search term]'.format(__file__))
    sys.exit(1)
print_page_titles(' '.join(sys.argv))
