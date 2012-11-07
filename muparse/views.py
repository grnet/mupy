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

from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
from django.http import HttpResponse
from mupy.muparse.models import *
from mupy.muparse.forms import *
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.cache import cache
import json, bz2

@login_required
def home(request, search_id = None):
    result = None
    if search_id:
        savedsearches = SavedSearch.objects.get(pk=search_id)
        graphs = []
        if not request.user.is_superuser:
            try:
                nodegroups = request.user.get_profile().nodegroups.all()
            except UserProfile.DoesNotExist:
                raise Http404
            graphs.extend(["%s"%(i.pk) for i in savedsearches.graphs.filter(node__group__in=nodegroups)])
        else:
            graphs.extend(["%s"%(i.pk) for i in savedsearches.graphs.all()])
        graphs = ','.join(graphs)
        result = {'result':graphs, 'display_type': savedsearches.display_type, 'description': savedsearches.description}
    saved_searches = SavedSearch.objects.all().order_by('description')
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        saved_searches = saved_searches.filter(graphs__in=NodeGraphs.objects.filter(node__group__in=nodegroups)).distinct()
    searches = []
    if saved_searches:
        searches.extend([s.description for s in saved_searches])
    return render_to_response('main.html', {'saved':searches, "new_window": result}, context_instance =RequestContext(request))


@login_required
def get_node_tree(request, user_id):    
    if int(request.user.pk) != int(user_id):
        raise Http404
    glist = cache.get('user_%s_tree'%(request.user.pk))
    if glist:
        glist = bz2.decompress(glist)
        return HttpResponse(glist, mimetype="application/json")
    grlist = []
    nlist = []
    parsed_node = []
    parsed_group = []
    graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('node__group', 'node', 'graph__category__name')
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs = graphs.filter(node__group__in=nodegroups)
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
                nlist.sort(key=lambda item:item['title'], reverse=False)
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
        gdict['graphname'] = graph.graph.name
        gdict['slug'] = graph.graph.slug
        gdict['url'] = graph.baseurl
        gdict['key'] = "graph_%s" %(graph.pk)
        gdict['pageurl'] = graph.pageurl
        gdict['nodeurl'] = graph.node.url
        gcdict['children'].append(gdict)
        if (index == (len_graphs-1)):
            nlist.append(ndict)
            nlist.sort(key=lambda item:item['title'], reverse=False)
            grdict['children']= nlist
            grlist.append(grdict)
            ndict['children'].append(gcdict)
    glist = json.dumps(grlist)
    cache.set('user_%s_tree'%(request.user.pk), bz2.compress(glist), 60 * 60 * 24 *5)
    return HttpResponse(glist, mimetype="application/json")

@login_required
def get_node_tree_category(request, user_id):
    if int(request.user.pk) != int(user_id):
        raise Http404
    glist = cache.get('user_%s_tree_cat'%(request.user.pk))
    if glist:
        glist = bz2.decompress(glist)
        return HttpResponse(glist, mimetype="application/json")
    grlist = []
    nlist = []
    graphs_list = []
    parsed_node = []
    parsed_group = []
    parsed_graph_category = []
    parsed_graph_name =[]
    graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('graph__category__name', 'graph__name', 'node__group', 'node__name')
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs = graphs.filter(node__group__in=nodegroups)
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
        ndict['title'] = graph.node.name
        ndict['graphname'] = graph.graph.name
        ndict['key'] = "graph_%s" %(graph.pk)
        ndict['url'] = graph.baseurl
        ndict['pageurl'] = graph.pageurl
        ndict['nodeurl'] = graph.node.url
        ndict['type'] = "graph"
        grdict['children'].append(ndict)
        
        if (index == (len_graphs-1)):
            grlist.append(gcdict)
    glist = json.dumps(grlist)
    cache.set('user_%s_tree_cat'%(request.user.pk), bz2.compress(glist), 60 * 60 * 24 *5)
    return HttpResponse(glist, mimetype="application/json")

@login_required
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
    
@login_required
@never_cache
def load_search(request, search_id=None):
    savedsearches = SavedSearch.objects.get(pk=search_id)
    graphs = []
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs.extend(["%s"%(i.pk) for i in savedsearches.graphs.filter(node__group__in=nodegroups)])
    else:
        graphs.extend(["%s"%(i.pk) for i in savedsearches.graphs.all()])
    graphs = ','.join(graphs)
    result = json.dumps({'result':graphs, 'display_type': savedsearches.display_type, 'description': savedsearches.description})
    return HttpResponse(result, mimetype="application/json")

@login_required
@never_cache
def load_search_blank(request, search_id=None):
    savedsearches = SavedSearch.objects.get(pk=search_id)
    graphs = []
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs.extend([int("%s"%(i.pk)) for i in savedsearches.graphs.filter(node__group__in=nodegroups)])
    else:
        graphs.extend([int("%s"%(i.pk)) for i in savedsearches.graphs.all()])
    nodegraphs = NodeGraphs.objects.filter(pk__in=graphs)
    return render_to_response('searches_window.html', {'graphs':nodegraphs}, context_instance =RequestContext(request))

@login_required
@never_cache
def delete_search(request, search_id=None):
    try:
        savedsearch = SavedSearch.objects.get(pk=search_id)
        savedsearch.delete()
        response = json.dumps({"result": "Successfully deleted %s"%(savedsearch.description), 'errors': 'None'})
    except Exception as e:
        response = json.dumps({"result": "Errors: %s" %(e), 'errors': "True"})
    return HttpResponse(response, mimetype="application/json")

@login_required
@never_cache  
def saved_searches(request):
    searches = []
    saved_searches = SavedSearch.objects.all().order_by('description')
    searches = saved_searches
    if not request.user.is_superuser:
        try:
            nodegroups = request.user.get_profile().nodegroups.all()
        except UserProfile.DoesNotExist:
            raise Http404
        searches = []
        saved_searches = saved_searches.filter(graphs__in=NodeGraphs.objects.filter(node__group__in=nodegroups)).distinct()
        for s in saved_searches:
            s_graphs = s.graphs.filter(node__group__in=nodegroups)
            if s_graphs:
                search_dict = {
                               'pk': s.pk,
                               'description': s.description,
                               'graphs': s_graphs
                               }
                searches.append(search_dict)
    return render_to_response('saved_searches.html', {"saved":searches}, context_instance =RequestContext(request))

