# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
from django.http import HttpResponse
from mupy.muparse.models import *
from django.views.decorators.cache import cache_page
import json

def home(request):
#    groups = NodeGroup.objects.all().select_related(depth=3)
    return render_to_response('out.html', context_instance =RequestContext(request))

@cache_page(60 * 60 * 24 *5)
def get_node_tree(request):
    glist = []
    groups = NodeGroup.objects.select_related(depth=5)
    for group in groups:
        gdict = {}
        gdict['name'] = group.name
        gdict['url'] = group.url
        nlist = []
        for node in group.node_set.all():
            ndict = {}
            ndict['name'] = node.name
            ndict['url'] = node.url
            nlist.append(ndict)
            graphlist = []
#            for graph in node.nodegraphs_set.all():
#                graphdict = {}
#                graphdict['name'] = graph.graph.name
#                graphdict['slug'] = graph.graph.slug
#                graphdict['url'] = graph.baseurl
#                graphlist.append(graphdict)
#            ndict['graphs'] = graphlist
        gdict['nodes'] = nlist
        glist.append(gdict)
    glist = json.dumps(glist)
    return render_to_response('out.html', {"glist":glist}, context_instance =RequestContext(request))
#    return HttpResponse(glist, mimetype="application/json")


@cache_page(60 * 60 * 24 *5)
def get_node_tree(request):
    grlist = []
    nlist = []
    parsed_node = []
    parsed_group = []
    
    graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('node', 'graph__category__name')
    len_graphs = len(graphs)
    for index, graph in enumerate(graphs):
        if graph.node not in parsed_node:
            parsed_graph_category = []
            if parsed_node:
                ndict['children'].append(gcdict)
                nlist.append(ndict)
            ndict = {}
            ndict['title'] = graph.node.name
            ndict['key'] = "node_%s" %(graph.node.pk)
            ndict['href'] = graph.node.url
            ndict['children'] = []
            ndict['type'] = "node"
            parsed_node.append(graph.node)

        if graph.node.group not in parsed_group:
            if parsed_group:
                grdict['children']= nlist
                grlist.append(grdict)
                nlist = []
            grdict={}
            grdict['title'] = graph.node.group.name
            grdict['key'] = "group_%s" %(graph.node.group.pk)
            grdict['href'] = graph.node.group.url
            grdict['children'] = []
            grdict['type'] = "group"
            parsed_group.append(graph.node.group)

        if graph.graph.category.name not in parsed_graph_category:
            if parsed_graph_category:
                ndict['children'].append(gcdict)
            gcdict = {}
            gcdict['title'] = graph.graph.category.name
            gcdict['key'] = "graphCategory_%s_%s" %(graph.node.pk, graph.graph.category.pk)
            gcdict['children'] = []
            gcdict['type'] = "graph_category"
            parsed_graph_category.append(graph.graph.category.name)
            
        gdict = {}
        gdict['type'] = "graph"
        gdict['title'] = graph.graph.name
        gdict['slug'] = graph.graph.slug
        gdict['url'] = graph.baseurl
        gdict['key'] = "graph_%s" %(graph.pk)
        gcdict['children'].append(gdict)
        if (index == (len_graphs-1)):
            nlist.append(ndict)
            grdict['children']= nlist
            grlist.append(grdict)
            ndict['children'].append(gcdict)            
    glist = json.dumps(grlist)
    return HttpResponse(glist, mimetype="application/json")

def get_node_tree_category(request):
    grlist = []
    nlist = []
    graphs_list = []
    parsed_node = []
    parsed_group = []
    parsed_graph_category = []
    parsed_graph_name =[]
    graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('graph__category__name', 'graph__name', 'node__group', 'node__name')
    len_graphs = len(graphs)
    for index, graph in enumerate(graphs):
        current_category = graph.graph.category.name
        
        if graph.graph.category.name not in parsed_graph_category:
            if parsed_graph_category:
#                gcdict['children'] = graphs_list
#                graphs_list = []
                grlist.append(gcdict)
            gcdict = {}
            gcdict['title'] = graph.graph.category.name
            gcdict['key'] = "graphCategory_%s_%s" %(graph.node.pk, graph.graph.category.pk)
            gcdict['children'] = []
            gcdict['type'] = "graph_category"
            parsed_graph_category.append(graph.graph.category.name)
                 
        if graph.graph.name not in parsed_graph_name:
            parsed_group = []
            gdict = {}
            gdict['type'] = "graph"
            gdict['title'] = graph.graph.name
            gdict['slug'] = graph.graph.slug
            gdict['children'] = []
            gcdict['children'].append(gdict)
            parsed_graph_name.append(graph.graph.name)
        

        
        if graph.node.group.name not in parsed_group:
            grdict = {}
            grdict['title'] = graph.node.group.name
            grdict['key'] = "group_%s" %(graph.node.group.pk)
            grdict['href'] = graph.node.group.url
            grdict['children'] = []
            grdict['type'] = "group"
    #        grdict['children'].append(ndict)
            gdict['children'].append(grdict)
            parsed_group.append(graph.node.group.name)

        ndict = {}
        ndict['title'] = graph.node.name
        ndict['key'] = "graph_%s" %(graph.pk)
        ndict['url'] = graph.baseurl
        ndict['type'] = "graph"
        grdict['children'].append(ndict)
        
        if (index == (len_graphs-1)):
#            nlist.append(ndict)
#            grdict['children']= nlist
            grlist.append(gcdict)
#            ndict['children'].append(gcdict)
   
    glist = json.dumps(grlist)
    return HttpResponse(glist, mimetype="application/json")


