from django.core.management.base import NoArgsCommand
from bs4 import BeautifulSoup
import urllib
from mupy.muparse.models import *

baseUrl = "http://munin.grnet.gr"

class Command(NoArgsCommand):
    
    def parseUrlSoup(self, url):
        serverListPage = urllib.urlopen("%s/%s" %(baseUrl, url))
        htmlText = serverListPage.read()
        serverListPage.close()
        return BeautifulSoup(htmlText)

    
    def handle_noargs(self, **options):
        soup = self.parseUrlSoup("index.html")
        homePage = soup.find_all('span', attrs={'class':'domain'})
        for nodeGroup in homePage:
            ng_url = "%s/%s" %(baseUrl, nodeGroup.a.get('href'))
            ng,created = NodeGroup.objects.get_or_create(name=nodeGroup.a.text, url=ng_url)
            self.stdout.write('Added nodeGroup: %s\n' % ng.name.encode('utf8'))
#            print i.a.text, i.a.get('href')
            for node in nodeGroup.findParent('li').findChildren('span', attrs={'class':'host'}):
                #print node.a.text, node.a.get('href')
                n_url = "%s/%s" %(baseUrl, node.a.get('href'))
                n,created = Node.objects.get_or_create(name=node.a.text, url=n_url, group=ng)
                self.stdout.write('-Added node: %s\n' % n.name.encode('utf8'))
                nodeSoup = self.parseUrlSoup(node.a.get('href'))
                metricsTable = nodeSoup.find_all('td',{'class':'graphbox'})
                for metricGroup in metricsTable:
                    metricCategory = metricGroup.get('id')
                    graphCategories = metricGroup.find_all('div', {'class':'lighttext'})
                    gc,created = GraphCategory.objects.get_or_create(name=metricCategory)
                    self.stdout.write('-Added Category: %s\n' % gc.name.encode('utf8'))
                    for graphCategory in graphCategories:
                        pageUrl = "%s/%s/%s/%s" %(baseUrl, nodeGroup.a.text, n.name, graphCategory.a.get('href'))
                        self.stdout.write('-Page URL: %s\n' % pageUrl.encode('utf8'))
                        t = graphCategory.findParent('tr').find_next_sibling('tr')
                        g,created = Graph.objects.get_or_create(name=graphCategory.a.text, slug=t.img.get('src').split('/')[-1:][0].split('-')[0], category=gc)
                        self.stdout.write('--Added Graph: %s\n' % g.name.encode('utf8'))
                        baseurl = "%s%s" %(baseUrl, t.img.get('src').split('.png')[0].split('-day')[0])
                        nodegraph, created = NodeGraphs.objects.get_or_create(node=n, graph=g, baseurl=baseurl, pageurl=pageUrl)
                        self.stdout.write('--Added NodeGraph: %s\n' % nodegraph)

a = Node.objects.all()
for i in a:
    print "Node:",i
    for g in i.graphs.all():
        print "=====>", g
                #n,created = Node.objects.get_or_create(name=node.a.text, url=n_url, group=ng)
                
#            domainSoup = self.parseUrlSoup(i.a.get('href'))
#            servers = domainSoup.find('td', attrs={'class':'linkbox'})
#            
#            for server in servers.ul.find_all('span', attrs={'class':'domain'}):
#                if 'diskstats' in server.a.text:
#                    continue
#                print "+", server.a
#                n_url = "%s/%s/%s" %(baseUrl, i.a.text, server.a.get('href'))
##                n,created = Node.objects.get_or_create(name=server.a.text, url=n_url, group=ng)
##                self.stdout.write('-Added node: %s\n' % n.name.encode('utf8'))
#                for metric in server.findParent('li').findChildren('span', attrs={'class':'host'}):
#                    if "diskstats" in metric.a.get('href'):
#                        continue
##                    gc,created = GraphCategory.objects.get_or_create(name=metric.text)
##                    self.stdout.write('-Added Category: %s\n' % gc.name.encode('utf8'))
##                    print "==>", metric.a.text, metric.a.get('href')
#                    node_services = []
#                    for service in metric.findParent('li').findChildren('span', attrs={'class':'service'}):
#                        service_text = service.a.text
#                        service_slug = service.a.get('href').split('/')[-1:][0].rstrip('.html')
#                        print service_text, service.a.get('href')
##                        c,created = Graph.objects.get_or_create(name=service_text, slug=service_slug, category=gc)
##                        self.stdout.write('--Added Graph: %s\n' % c.name.encode('utf8'))
#                        node_services.append(c)
#                    n.graphs = node_services
#                    n.save()
##                        serviceContents = self.parseUrlSoup("%s/%s" %(i.a.text, service.a.get('href')))
##                        graphs = serviceContents.find_all('img')
##                        for graph in graphs:
##                            print "==========>", graph

