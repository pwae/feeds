#!/usr/bin/python

import urllib

from BeautifulSoup import BeautifulSoup

URL = 'http://www.apress.com/dailydeals/index/'

HTML_ESCAPE = {
    "&":    "&amp;",
    "\"":   "&quot;",
    "'":    "&apos;",
    ">":    "&gt;",
    "<":    "&lt;",
}

def simple_escape(text):
    return ''.join(HTML_ESCAPE.get(c,c) for c in text)

def get_article(url):
    f = urllib.urlopen(url)
    b = BeautifulSoup(f.read())

    title = b.find('div', {'class': 'product-name'}).findChild('h1').text
    try:
        sub_title = b.find('div', {'class': 'product-name'}).findChild('h2').text
    except:
        sub_title = None
    description = b.find('div', {'class': 'std'})
    sub_text = b.find('ul', {'class': 'meta-snippet' })
    url = f.url

    return { 'title': title,
             'subtitle': sub_title,
             'description': description,
             'sub_text': sub_text,
             'url': url,
    }


def print_article():
    entry = get_article(URL)
    
    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<feed xmlns="http://www.w3.org/2005/Atom">'
    print '  <title>Apress Daily Deal - New book each day</title>'
    print '  <link href="%s" />' % simple_escape(URL)

    print '  <entry>'
    if entry['subtitle']:
        print '    <title>%s - %s</title>' % (entry['title'], entry['subtitle'])
    else:
        print '    <title>%s</title>' % (entry['title'])

    print '    <link href="%s" />' % entry['url']
    print '    <content type="html">%s\n\n%s</content>' % (entry['description'], entry['sub_text'])
    print '  </entry>'


    print '</feed>'

if __name__ == '__main__':
    print_article()
