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
from django.db import models

class NodeGroup(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name

class GraphCategory(models.Model):
    name = models.SlugField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
class Graph(models.Model):
    name = models.SlugField(max_length=255)
    slug = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(GraphCategory)
        
    def __unicode__(self):
        return self.name

class Node(models.Model):
    name = models.SlugField(max_length=255)
    url = models.CharField(max_length=512)
    group = models.ForeignKey(NodeGroup)
    graphs = models.ManyToManyField(Graph, blank=True, null=True, through='NodeGraphs')
    
    def __unicode__(self):
        return self.name
    
    def get_graph_categories(self):
        cat_list = []
        for graph in self.graphs.all():
            cat_list.append(graph.category.pk)
        return GraphCategory.objects.filter(pk__in=list(set(cat_list)))

class NodeGraphs(models.Model):
    node = models.ForeignKey(Node)
    graph = models.ForeignKey(Graph)
    baseurl = models.CharField(max_length=512)
    pageurl = models.CharField(max_length=512)
    
    def __unicode__(self):
        return u"%s:%s:%s" %(self.node, self.graph, self.baseurl)

class SavedSearch(models.Model):
    description = models.CharField(max_length=255)
    display_type = models.CharField(max_length=64)
    graphs = models.ManyToManyField(NodeGraphs, blank=True, null=True)
    
    def __unicode__(self):
        return self.description