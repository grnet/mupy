from django.conf import settings
from muparse.models import MuninNodes
import requests
from django.core.exceptions import ImproperlyConfigured


def get_all_nodes():
    MNODES = []
    for node in settings.MUNIN_NODES:
        if isinstance(node, tuple):
            MNODES.append(node)
        else:
            raise ImproperlyConfigured('Munin node should be a tupple')
    for node in MuninNodes.objects.all():
        MNODES.append((node.name, node.as_dict()))
    if not MNODES:
        raise Exception('No nodes found!!')
    return MNODES


def get_v2_nodes():
    nodes = []
    for node in get_all_nodes():
        url = node[1].get('url')
        try:
            html = requests.get(url).text
            if html[html.find('version ') + 8] == '2':
                nodes.append(node)
        except:
            print 'Could not fetch %s' % (url)
    return nodes


def get_v1_nodes():
    nodes = []
    for node in get_all_nodes():
        url = node[1].get('url')
        try:
            html = requests.get(url).text
            if html[html.find('version ') + 8] == '1':
                nodes.append(node)
        except:
            print 'Could not fetch %s' % (url)
    return nodes

