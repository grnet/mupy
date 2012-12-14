# -*- coding: utf-8 -*-
# Copyright 2012 Leonidas Poulopoulos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.management.base import NoArgsCommand
from bs4 import BeautifulSoup
import urllib
from mupy.muparse.models import *
from django.conf import settings


baseUrl = settings.MUNIN_URL
cgiPath = settings.MUNIN_CGI_PATH

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
                        imageUrl = "%s/%s%s/%s/%s" %(baseUrl, cgiPath, nodeGroup.a.text, n.name, g.slug)
                        nodegraph, created = NodeGraphs.objects.get_or_create(node=n, graph=g, baseurl=imageUrl, pageurl=pageUrl)
                        self.stdout.write('--Added NodeGraph: %s\n' % nodegraph)

