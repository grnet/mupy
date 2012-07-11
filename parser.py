from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
        print "Attrs: %s" %attrs
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :", data

# URL extractor
# Copyright 2004, Paul McGuire
from pyparsing import *
import urllib
import pprint

# Define the pyparsing grammar for a URL, that is:
#    URLlink ::= <a href= URL>linkText</a>
#    URL ::= doubleQuotedString | alphanumericWordPath
# Note that whitespace may appear just about anywhere in the link.  Note also
# that it is not necessary to explicitly show this in the pyparsing grammar; by default,
# pyparsing skips over whitespace between tokens.
def parselocation():
    
    escapechar = "\\"
    wordtext = CharsNotIn('\\*?^():"[]|=')
    escape = Suppress(escapechar) + (Word(printables, exact=1) | White(exact=1))
    wordvalues = Combine(OneOrMore(wordtext | escape | '=>'))
    
    linkOpenTagSpan, linkCloseTagSpan = makeHTMLTags("span")
    linkOpenTagSpan.setParseAction(withAttribute(("class","domain")))
    
    linkOpenTagSpanHost, linkCloseTagSpanHost = makeHTMLTags("span")
    linkOpenTagSpanHost.setParseAction(withAttribute(("class","host")))

    linkOpenTagHref,linkCloseTagHref = makeHTMLTags("a")
    
    
    tableAllOpen, tableAllClose  =  makeHTMLTags("table")
    tableAllOpen.setParseAction(withAttribute(("class","largeinvisiblebox")))
    
    
    
    linkGroups = SkipTo(linkOpenTagSpan).suppress() + linkOpenTagSpan.suppress() + linkOpenTagHref + SkipTo(linkCloseTagHref).setResultsName("nodegroup") + linkCloseTagHref.suppress() + linkCloseTagSpan.suppress()
    
    
    
    linkHosts = linkOpenTagSpanHost.suppress() + linkOpenTagHref + SkipTo(linkCloseTagHref) + linkCloseTagHref.suppress() + linkCloseTagSpanHost.suppress()
    
    
    allGroupHosts = OneOrMore(linkGroups + Group(OneOrMore(SkipTo(linkOpenTagSpanHost).suppress() + linkHosts).setResultsName("host")).setResultsName("hosts"))
    
    
    
    # Go get some HTML with some links in it.
    serverListPage = urllib.urlopen( "http://munin.grnet.gr" )
    htmlText = serverListPage.read()
    serverListPage.close()
    
    # scanString is a generator that loops through the input htmlText, and for each
    # match yields the tokens and start and end locations (for this application, we are
    # not interested in the start and end values).
    print allGroupHosts.parseString(htmlText).asList()
    
    print "\n\n\n\n"
    for toks,strt,end in allGroupHosts.scanString(htmlText):
        print "%s => %s" %(toks.nodegroup, toks.startA.href)
        print toks.hosts
        print "Hosts:\n"
#    for toks,strt,end in linkHosts.scanString(htmlText):
#        print toks[0]
#    print list(link.scanString(htmlText))
    
    
    # Create dictionary from list comprehension, assembled from each pair of tokens returned 
    # from a matched URL.
#    pprint.pprint( 
#        dict( [ (toks.body,toks.startA.href) for toks,strt,end in link.scanString(htmlText) ] )
#        )

from bs4 import BeautifulSoup

def parseUrlSoup(url):
    baseUrl = "http://munin.grnet.gr"
    serverListPage = urllib.urlopen("%s/%s" %(baseUrl, url))
    htmlText = serverListPage.read()
    serverListPage.close()
    return BeautifulSoup(htmlText)

def parseText():
    baseUrl = "http://munin.grnet.gr"
    soup = parseUrlSoup("index.html")
    b = soup.find_all('span', attrs={'class':'domain'})
    for i in b:
        print i.a.text, i.a.get('href')
        domainSoup = parseUrlSoup(i.a.get('href'))
        servers = domainSoup.find('td', attrs={'class':'linkbox'})
        
        for server in servers.ul.find_all('span', attrs={'class':'domain'}):
            if 'diskstats' in server.a.text:
                continue
            print "+", server.a
            for metric in server.findParent('li').findChildren('span', attrs={'class':'host'}):
                if "diskstats" in metric.a.get('href'):
                    continue
                print "==>", metric.a.text, metric.a.get('href')
                for service in metric.findParent('li').findChildren('span', attrs={'class':'service'}):
                    print "======>", service.a.text, "%s/%s" %(i.a.text, service.a.get('href'))
                    serviceContents = parseUrlSoup("%s/%s" %(i.a.text, service.a.get('href')))
                    graphs = serviceContents.find_all('img')
                    for graph in graphs:
                        print "==========>", graph
            
#            serverItem = server.li.find('span', attrs={'class':'domain'})
#            print serverItem, '\n\n\n'
#        for l in servers:
#            print l, 'LAAAAAAAAAAAAA\n\n\n'
#            for l in servers:
#                print l.a.text
#        for j in i.findParent('li').findChildren('span', attrs={'class':'host'}):
#            print "==>", j.a.text, j.a.get('href')
#            
#            for k in j.find_next_siblings('a'):
#                print "---------", k.text, k.get('href')
     
if __name__ == "__main__":
#    parser = MyHTMLParser()
#    file = open('index.html').read()
#    parser.feed(file)
    parseText()
