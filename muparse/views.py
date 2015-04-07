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

import json
import bz2

from django.shortcuts import render
from django.http import HttpResponse
from muparse.models import NodeGraphs
from muparse.forms import *
from accounts.models import UserProfile
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.cache import cache


@login_required
def home(request):
    saved_searches = SavedSearch.objects.filter(user=request.user)
    default = saved_searches.filter(default=True) or False
    return render(request, 'main.html', {'saved': saved_searches, 'default': default})


def common_start(sa, sb):
    '''
    returns the longest common substring from the beginning of sa and sb
    '''
    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return

    return ''.join(_iter())


@login_required
def get_node_tree(request):
    glist = cache.get('user_%s_tree' % (request.user.pk))
    if glist:
        glist = bz2.decompress(glist)
        return HttpResponse(glist, mimetype="application/json")
    grlist = []
    nlist = []
    parsed_node = []
    parsed_group = []
    graphs = NodeGraphs.objects.all().prefetch_related(
        'node',
        'graph',
        'node__group',
        'graph__category'
    ).order_by('node__group', 'node', 'graph__category__name')
    try:
        nodes = request.user.get_profile().nodes.all()
    except UserProfile.DoesNotExist:
        raise Http404
    graphs = graphs.filter(node__in=nodes)
    len_graphs = len(graphs)
    for index, graph in enumerate(graphs):
        if graph.node not in parsed_node:
            parsed_graph_category = []
            if parsed_node:
                ndict['children'].append(gcdict)
                nlist.append(ndict)
            ndict = {}
            ndict['title'] = graph.node.name
            ndict['children'] = []
            parsed_node.append(graph.node)
        if graph.node.group not in parsed_group:
            if parsed_group:
                nlist.sort(key=lambda item: item['title'], reverse=False)
                grdict['children'] = nlist
                grlist.append(grdict)
                nlist = []
            grdict = {}
            grdict['title'] = graph.node.group.name
            grdict['children'] = []
            grdict['baseurl'] = common_start(graph.baseurl, graph.node.url)
            parsed_group.append(graph.node.group)
        if graph.graph.category.name not in parsed_graph_category:
            if parsed_graph_category:
                ndict['children'].append(gcdict)
            gcdict = {}
            gcdict['title'] = graph.graph.category.name
            gcdict['children'] = []
            gcdict['nodeurl'] = graph.pageurl.replace(common_start(graph.baseurl, graph.node.url), '')
            parsed_graph_category.append(graph.graph.category.name)
        gdict = {}
        gdict['title'] = graph.graph.name
        gdict['url'] = graph.baseurl.replace(common_start(graph.baseurl, graph.node.url), '')
        gdict['key'] = 'graph_%s' % (graph.pk)
        gcdict['children'].append(gdict)
        if (index == (len_graphs - 1)):
            nlist.append(ndict)
            nlist.sort(key=lambda item: item['title'], reverse=False)
            grdict['children'] = nlist
            grlist.append(grdict)
            ndict['children'].append(gcdict)
    glist = json.dumps(grlist)
    cache.set('user_%s_tree' % (request.user.pk), bz2.compress(glist), 60 * 60 * 24 *5)
    return HttpResponse(glist, mimetype="application/json")


@login_required
def get_node_tree_category(request):
    glist = cache.get('user_%s_tree_cat' % (request.user.pk))
    if glist:
        glist = bz2.decompress(glist)
        return HttpResponse(glist, mimetype="application/json")
    grlist = []
    parsed_group = []
    parsed_graph_category = []
    parsed_graph_name = []
    graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('graph__category__name', 'graph__name', 'node__group', 'node__name')
    if not request.user.is_superuser:
        try:
            nodes = request.user.get_profile().nodes.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs = graphs.filter(node__in=nodes)
    len_graphs = len(graphs)
    for index, graph in enumerate(graphs):
        if graph.graph.category.name not in parsed_graph_category:
            if parsed_graph_category:
                grlist.append(gcdict)
            gcdict = {}
            gcdict['title'] = graph.graph.category.name
            gcdict['children'] = []
            gcdict['nodeurl'] = graph.pageurl.replace(common_start(graph.baseurl, graph.node.url), '')
            parsed_graph_category.append(graph.graph.category.name)

        if graph.graph.name not in parsed_graph_name:
            parsed_group = []
            gdict = {}
            gdict['title'] = graph.graph.name
            gdict['children'] = []
            gcdict['children'].append(gdict)
            parsed_graph_name.append(graph.graph.name)

        if graph.node.group.name not in parsed_group:
            grdict = {}
            grdict['title'] = graph.node.group.name
            grdict['children'] = []
            grdict['baseurl'] = common_start(graph.baseurl, graph.node.url)
            gdict['children'].append(grdict)
            parsed_group.append(graph.node.group.name)

        ndict = {}
        ndict['title'] = graph.node.name
        ndict['key'] = "graph_%s" % (graph.pk)
        ndict['url'] = graph.baseurl.replace(common_start(graph.baseurl, graph.node.url), '')
        grdict['children'].append(ndict)
        if (index == (len_graphs - 1)):
            grlist.append(gcdict)
    glist = json.dumps(grlist)
    cache.set('user_%s_tree_cat' % (request.user.pk), bz2.compress(glist), 60 * 60 * 24 *5)
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
        response = json.dumps({"result": "Successfully saved %s graphs as %s"%(len(graph_pks), search.description), 'errors': None})
        return HttpResponse(response, mimetype="application/json")
    else:
        response = json.dumps({"result": "Errors: %s" %(form.errors.as_text()), 'errors': True})
        return HttpResponse(response, mimetype="application/json")


@login_required
@never_cache
def load_search(request, search_id=None):
    savedsearches = SavedSearch.objects.get(pk=search_id)
    graphs = []
    if not request.user.is_superuser:
        try:
            nodes = request.user.get_profile().nodes.all()
        except UserProfile.DoesNotExist:
            raise Http404
        graphs.extend(["%s" % (i.pk) for i in savedsearches.graphs.filter(node__in=nodes)])
    else:
        graphs.extend(["%s" % (i.pk) for i in savedsearches.graphs.all()])
    graphs = ','.join(graphs)
    result = json.dumps({'result':graphs, 'display_type': savedsearches.display_type, 'description': savedsearches.description})
    return HttpResponse(result, mimetype="application/json")


@login_required
@never_cache
def delete_search(request, search_id=None):
    try:
        savedsearch = SavedSearch.objects.get(pk=search_id)
        savedsearch.delete()
        response = json.dumps({"result": "Successfully deleted %s" % (savedsearch.description), 'errors': False})
    except Exception as e:
        response = json.dumps({"result": "Errors: %s" % (e), 'errors': True})
    return HttpResponse(response, mimetype="application/json")


@login_required
@never_cache
def saved_searches(request):
    searches = []
    saved_searches = SavedSearch.objects.filter(user=request.user).order_by('description')
    for s in saved_searches:
        searches.append({
            'id': s.id,
            'description': s.description,
            'url': s.get_absolute_url(),
            'default': s.default,
            'default_url': s.get_default_url(),
            'delete_url': s.get_delete_url()
        })
    return HttpResponse(json.dumps({"saved": searches}), mimetype="application/json")


@login_required
@never_cache
def default_search(request, search_id):
    default_searches = SavedSearch.objects.filter(user=request.user, default=True)
    for search in default_searches:
        search.default = False
        search.save()
    new_search = SavedSearch.objects.get(id=search_id, user=request.user)
    if not new_search:
        return HttpResponse(json.dumps({"erros": True, 'message': 'Permission Denied'}), mimetype="application/json")
    new_search.default = True
    new_search.save()
    return HttpResponse(json.dumps({"erros": False}), mimetype="application/json")
