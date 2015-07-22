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

from django.shortcuts import render
from django.http import HttpResponse
from muparse.models import SavedSearch
from muparse.forms import SavedSearchForm
from accounts.models import UserProfile
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from muparse.models import NodeGraphs


@login_required
def home(request):
    saved_search = SavedSearch.objects.filter(user=request.user)
    if saved_search:
        default = saved_search.filter(default=True)
        if default:
            saved_search = default
        graphs = saved_search[0].graphs.all()
    else:
        nodes = request.user.get_profile().nodes.all()
        graphs = NodeGraphs.objects.filter(node__in=nodes)[:50]
        default = False
    return render(request, 'main.html', {'graphs': graphs, 'default': default})


@login_required
def get_menu(request):
    return render(request, 'partial/graphs_menu.html')


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
        response = json.dumps({"result": "Successfully saved %s graphs as %s" % (len(graph_pks), search.description), 'errors': None})
        return HttpResponse(response, mimetype="application/json")
    else:
        response = json.dumps({"result": "Errors: %s" % (form.errors.as_text()), 'errors': True})
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
    result = json.dumps({'result': graphs, 'display_type': savedsearches.display_type, 'description': savedsearches.description})
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
