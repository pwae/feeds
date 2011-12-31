#!/usr/bin/python
import re
from mechanize import Browser

ARTICLE_DATA = '\t\t\t\t<td ><p class="Body_Text"><br>'

HTML_ESCAPE = {
    "&":    "&amp;",
    "\"":   "&quot;",
    "'":    "&apos;",
    ">":    "&gt;",
    "<":    "&lt;",
}

def simple_escape(text):
    return ''.join(HTML_ESCAPE.get(c,c) for c in text)

def get_articlelist():
    entry_page = "http://www.ausleisure.com.au/default.asp?PageID=2&n=Latest+News"

    br = Browser()
    br.open(entry_page)
    entries = []

    for l in br.links():
        if l.url.startswith("default.asp?PageID=2&ReleaseID=") and not l.text == '[IMG]':
            date = l.text[:10]
            title = l.text[15:]
            url = l.absolute_url
            data = get_article(url)

            entry = {
                'title':    simple_escape(title),
                'link':     simple_escape(url),
                'id':       simple_escape(url),
                'updated':  '%s-%s-%sT00:00:00Z' % (date[6:], date[3:5], date[:2]),
                'content':  simple_escape(data),
            }

            entries.append(entry)

    return entries

def get_article(url):
    br = Browser()
    br.open(url)
    resp = br.response()

    data = ''
    for line in resp.readlines():
        if line.startswith(ARTICLE_DATA):
            data = line[len(ARTICLE_DATA):]
            break

    return data

def print_atom():
    data = get_articlelist()

    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<feed xmlns="http://www.w3.org/2005/Atom">'
    print '  <title>Australasian Leisure Management - Latest News</title>'
    print '  <link href="%s" />' % simple_escape('http://www.ausleisure.com.au/default.asp?PageID=2&n=Latest+News')

    for entry in data:
        print '  <entry>'
        print '    <title>%s</title>' % entry['title']
        print '    <link href="%s" />' % entry['link']
        print '    <id>%s</id>' % entry['id']
        print '    <updated>%s</updated>' % entry['updated']
        print '    <content type="html">%s</content>' % entry['content']
        print '  </entry>'

    print '</feed>'

if __name__ == '__main__':
    print_atom()
