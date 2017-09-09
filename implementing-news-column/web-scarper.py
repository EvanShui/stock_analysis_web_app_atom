import sys # Used to add the BeautifulSoup folder the import path
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import json as m_json
import re

if __name__ == "__main__":
    ### Import Beautiful Soup
    ### Here, I have the BeautifulSoup folder in the level of this Python script
    ### So I need to tell Python where to look.

    ### Create opener with Google-friendly user agent
    opener = urllib.request.build_opener()
    # use if you want to scrape google's search results
    #opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.

    #for google
    #url = "https://www.google.com/search?source=hp&q=1234"

    #for marketwatch
    url = "http://www.marketwatch.com/search?q=ATVI&m=Ticker&rpp=15&mp=2005&bd=true&bd=false&bdv=08%2F16%2F2017&rs=true"

    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")

    #print(soup.prettify().encode("utf-8"))

    lst = []
    #for title and link of marketwatch articles
    #for x in soup.findAll(class_="searchresult"):
    #    print(x.a.encode("utf-8"))
    #for x in soup.findAll(class_="deemphasized")[1:-1]:
    #    print(x.contents[0].string)
    #    print(x.contents[1][5:].encode("utf-8"))

    soup_tuple_list = zip(soup.findAll(class_="searchresult"), soup.findAll(class_="deemphasized")[1:-1])
    for article, date in soup_tuple_list:
        time = date.contents[1][5:]
        time = re.findall(r'\|.[A-Za-z ]*', time)[0]
        info = date.contents[0].string + time
        print(info)
        article.a['target'] = "_blank"
        lst.append((article.a.encode("utf-8"),info))
    for i in lst:
        print(i[0])
        print(i[1])

    #for x in soup.findAll(class_="block"):
    #    print((x.a))
        #print((x.a.contents[0].encode("utf-8")))

    #for x in soup.findAll(class_="searchresult"):
    #    print((x.a.contents[0].encode("utf-8")))
    #    lst.append(((x.a.contents[0].encode("utf-8"))))

    #for x in soup.findAll(class_="deemphasized"):
    #    print(x.contents[0].encode("utf-8"))

    #for i in soup.findAll(class_="f"):
    #    print(i)

    ### Parse and find
    ### Looks like google contains URLs in <cite> tags.
    ### So for each cite tag on each page (10), print its contents (url)
    #for cite in soup.findAll('cite'):
    #    print(cite.text)

    print
