import sys # Used to add the BeautifulSoup folder the import path
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import json as m_json

if __name__ == "__main__":
    ### Import Beautiful Soup
    ### Here, I have the BeautifulSoup folder in the level of this Python script
    ### So I need to tell Python where to look.

    ### Create opener with Google-friendly user agent
    opener = urllib.request.build_opener()



    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.

    url = "http://www.marketwatch.com/search?q=ATVI&m=Ticker&rpp=15&mp=2005&bd=true&bd=false&bdv=08%2F16%2F2017&rs=true"

    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")

    #print(soup.prettify().encode("utf-8"))

    lst = []

    for x in soup.findAll(class_="searchresult"):
        print((x.a.contents[0].encode("utf-8")))
        lst.append(((x.a.contents[0].encode("utf-8"))))

    for x in soup.findAll(class_="deemphasized"):
        print(x.contents[0].encode("utf-8"))

    print(lst)
    for i in lst:
        print(str(i))

    #for i in soup.findAll(class_="f"):
    #    print(i)

    ### Parse and find
    ### Looks like google contains URLs in <cite> tags.
    ### So for each cite tag on each page (10), print its contents (url)
    #for cite in soup.findAll('cite'):
    #    print(cite.text)

    print
