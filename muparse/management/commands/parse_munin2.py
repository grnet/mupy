# -*- coding: utf-8 -*-
# Copyright 2014 Leonidas Poulopoulos
# Copyright 2014 Costas Drogos
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
from django.conf import settings

MNODES = settings.MUNIN_NODES


class Command(NoArgsCommand):

    def parseUrlSoup(self, baseUrl, urlPage):
        if urlPage:
            serverListPage = urllib.urlopen("%s/%s" %(baseUrl, urlPage))
        else:
            serverListPage = urllib.urlopen("%s" %(baseUrl))
        htmlText = serverListPage.read()
        serverListPage.close()
        return BeautifulSoup(htmlText)

    def handle_noargs(self, **options):
        for mnode in MNODES:
            mnode_dict = mnode[1]
            mnode_id = mnode[0]
            baseUrl = mnode_dict['url']
            cgiPath = mnode_dict['cgi_path']
            soup = self.parseUrlSoup(baseUrl, "index.html")
            homePage = soup.find_all('span', attrs={'class': 'domain'})
            for nodeGroup in homePage:
                ng_url = "%s/%s" %(baseUrl, nodeGroup.a.get('href'))
                self.stdout.write('NodeCategory: %s\n' % nodeGroup.a.text)
                nodegroupSoup = self.parseUrlSoup(ng_url, "")
                nodes = nodegroupSoup.find('div', attrs={'id': 'content'})\
                                     .find('ul', recursive=False).find_all('li', recursive=False)
                for node in nodes:
                    node_name = node.find('span', attrs={'class':'domain'}, recursive=False)
                    n_url = "%s/%s/%s" %(baseUrl, nodeGroup.a.text, node_name.a.get('href'))
                    self.stdout.write('-Node: %s %s\n' % (node_name.a.text, n_url))

                    services_categories = node.find_all('ul', recursive=False)
                    # get inside node
                    for service_category in services_categories:
                        category_group = service_category.find_all('li')
                        # a node has graph categories (class=host) that have services (class=service)
                        for category in category_group:
                            self.stdout.write('--GraphCategory: %s\n' % category.a.text)
                            services = category.findChildren('span', attrs={'class': 'service'})
                            for service in services:
                                self.stdout.write('---Graph: %s\n' % service.a.text)
