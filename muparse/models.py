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
        return "%s:%s:%s" %(self.node, self.graph, self.baseurl)

class SavedSearch(models.Model):
    description = models.CharField(max_length=255)
    display_type = models.CharField(max_length=64)
    graphs = models.ManyToManyField(NodeGraphs, blank=True, null=True)
    
    def __unicode__(self):
        return self.description