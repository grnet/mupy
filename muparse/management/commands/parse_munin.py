# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.core.management.base import NoArgsCommand
from bs4 import BeautifulSoup
import urllib
from muparse.models import *
from django.conf import settings

mnodes = settings.MUNIN_NODES


class Command(NoArgsCommand):

    def parseUrlSoup(self, baseUrl, urlPage):
        serverListPage = urllib.urlopen("%s/%s" %(baseUrl, urlPage))
        htmlText = serverListPage.read()
        serverListPage.close()
        return BeautifulSoup(htmlText)


    def handle_noargs(self, **options):
        for mnode in mnodes:
            mnode_dict = mnode[1]
            mnode_id = mnode[0]
            baseUrl = mnode_dict['url']
            cgiPath = mnode_dict['cgi_path']
            soup = self.parseUrlSoup(baseUrl, "index.html")
            homePage = soup.find_all('span', attrs={'class':'domain'})
            for nodeGroup in homePage:
                ng_url = "%s/%s" %(baseUrl, nodeGroup.a.get('href'))
                ng,created = NodeGroup.objects.get_or_create(name="%s@%s"%(nodeGroup.a.text, mnode_dict['name']), url=ng_url)
                self.stdout.write('Added nodeGroup: %s\n' % ng.name.encode('utf8'))
    #            print i.a.text, i.a.get('href')
                for node in nodeGroup.findParent('li').findChildren('span', attrs={'class':'host'}):
                    #print node.a.text, node.a.get('href')
                    n_url = "%s/%s" %(baseUrl, node.a.get('href'))
                    n,created = Node.objects.get_or_create(name=node.a.text, url=n_url, group=ng)
                    self.stdout.write('-Added node: %s\n' % n.name.encode('utf8'))
                    nodeSoup = self.parseUrlSoup(baseUrl, node.a.get('href'))
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

