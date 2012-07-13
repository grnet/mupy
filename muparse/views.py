from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
from django.http import HttpResponse
from mupy.muparse.models import *
from mupy.muparse.forms import *
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
import json

def home(request):
    saved_searches = SavedSearch.objects.all()
    searches = []
    if saved_searches:
        searches.extend([s.description for s in saved_searches])
    return render_to_response('out.html', {'saved':searches}, context_instance =RequestContext(request))

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
        gdict['nodes'] = nlist
        glist.append(gdict)
    glist = json.dumps(glist)
    return render_to_response('out.html', {"glist":glist}, context_instance =RequestContext(request))

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
        gdict['nodename'] = graph.node.name
        gdict['slug'] = graph.graph.slug
        gdict['url'] = graph.baseurl
        gdict['key'] = "graph_%s" %(graph.pk)
        gdict['pageurl'] = graph.pageurl
        gdict['nodeurl'] = graph.node.url
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
            gdict['children'].append(grdict)
            parsed_group.append(graph.node.group.name)

        ndict = {}
        ndict['nodename'] = graph.node.name
        ndict['title'] = graph.graph.name
        ndict['key'] = "graph_%s" %(graph.pk)
        ndict['url'] = graph.baseurl
        ndict['pageurl'] = graph.pageurl
        ndict['nodeurl'] = graph.node.url
        ndict['type'] = "graph"
        grdict['children'].append(ndict)
        
        if (index == (len_graphs-1)):
            grlist.append(gcdict)
   
    glist = json.dumps(grlist)
    return HttpResponse(glist, mimetype="application/json")


@never_cache
def save_search(request):
    request_data = request.POST.copy()
    graph_pks = request_data.get('graphs').split(',')
    is_edit = request_data.get('is_edit')
    request_data.setlist('graphs', graph_pks)
    form = SavedSearchForm(request_data)
    if is_edit == 'edit':
        description = request_data.get('description')
        try:
            existinggraphsearch = SavedSearch.objects.get(description=description)
            form = SavedSearchForm(request_data, instance=existinggraphsearch)            
        except SavedSearch.DoesNotExist:
            pass
    if form.is_valid():
        search = form.save(commit=False)
        search.save()
        form.save_m2m()
        response = json.dumps({"result": "Successfully saved %s graphs as %s"%(len(graph_pks), search.description), 'errors': 'None'})
        return HttpResponse(response, mimetype="application/json")
    else:
        response = json.dumps({"result": "Errors: %s" %(form.errors), 'errors': "True"})
        return HttpResponse(response, mimetype="application/json")

@never_cache
def load_search(request, search_id=None):
    savedsearches = SavedSearch.objects.get(pk=search_id)
    graphs = []
    graphs.extend(["%s"%(i.pk) for i in savedsearches.graphs.all()])
    graphs = ','.join(graphs)
    result = json.dumps({'result':graphs, 'display_type': savedsearches.display_type, 'description': savedsearches.description})
    return HttpResponse(result, mimetype="application/json")

@never_cache
def delete_search(request, search_id=None):
    try:
        savedsearch = SavedSearch.objects.get(pk=search_id)
        savedsearch.delete()
        response = json.dumps({"result": "Successfully deleted %s"%(savedsearch.description), 'errors': 'None'})
    except Exception as e:
        response = json.dumps({"result": "Errors: %s" %(e), 'errors': "True"})
    return HttpResponse(response, mimetype="application/json")

@never_cache  
def saved_searches(request):
    saved_searches = SavedSearch.objects.all().order_by('description')
    return render_to_response('saved_searches.html', {"saved":saved_searches}, context_instance =RequestContext(request))
