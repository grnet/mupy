import bz2
import json
from django import template
from muparse.models import SavedSearch, NodeGraphs
from accounts.models import UserProfile
from django.core.cache import cache
from muparse.views import common_start

register = template.Library()


@register.inclusion_tag('partial/saved_searches.html', takes_context=True)
def show_saved_searches(context):
    saved_searches = SavedSearch.objects.filter(user=context.get('request').user)
    default = saved_searches.filter(default=True) or False
    return {'saved': saved_searches, 'default': default}


@register.inclusion_tag('partial/graphs.html', takes_context=True)
def load_graphs(context, by_type=False):
    request = context.get('request')
    glist = cache.get('user_%s_tree' % (request.user.pk))
    if glist:
        grlist = json.loads(bz2.decompress(glist))
    else:
        grlist = []
        nlist = []
        gcdict = {}
        ndict = {}
        nlist = []
        grdict = {}
        parsed_node = []
        parsed_group = []
        graphs = NodeGraphs.objects.all().prefetch_related(
            'node',
            'graph',
            'node__group',
            'graph__category'
        ).order_by('node__group', 'node', 'graph__category__name')
        nodes = request.user.get_profile().nodes.all()
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
    return {'nodes': grlist, 'by_type': by_type}
