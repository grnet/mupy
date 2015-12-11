import bz2
import json
from django import template
from muparse.models import SavedSearch, NodeGraphs, common_start
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('partial/saved_searches.html', takes_context=True)
def show_saved_searches(context):
    user = context.get('request').user
    try:
        saved_searches = SavedSearch.objects.filter(user=user)
    except:
        saved_searches =  SavedSearch.objects.none()
    finally:
        default = saved_searches.filter(default=True) or False
        return {'saved': saved_searches, 'default': default}


@register.inclusion_tag('partial/graphs.html', takes_context=True)
def load_graphs(context):
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
    return {'nodes': grlist}


@register.inclusion_tag('partial/graphs.html', takes_context=True)
def load_graphs_by_type(context):
    request = context.get('request')
    glist = cache.get('user_%s_tree_cat' % (request.user.pk))
    if glist:
        grlist = json.loads(bz2.decompress(glist))
    else:
        grlist = []
        gcdict = {}
        parsed_group = []
        parsed_graph_category = []
        parsed_graph_name = []
        graphs = NodeGraphs.objects.all().select_related('node', 'graph', 'node__group', 'graph__category').order_by('graph__category__name', 'graph__name', 'node__group', 'node__name')
        if not request.user.is_superuser:
            nodes = request.user.get_profile().nodes.all()
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
    return {'nodes': grlist, 'bytype': True}

