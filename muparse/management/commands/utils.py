from django.conf import settings
from muparse.models import MuninNodes
from django.core.exceptions import ImproperlyConfigured


def get_v2_nodes():
    MNODES = []
    for node in settings.MUNIN_NODES:
        if isinstance(node, tuple):
            if node[1].get('version', 'v2') == 'v2':
                MNODES.append(node)
            else:
                raise ImproperlyConfigured('Munin node should be a tupple')
    for node in MuninNodes.objects.filter(munin_version='v2'):
        MNODES.append((node.name, node.as_dict()))
    return MNODES


def get_v1_nodes():
    MNODES = []
    for node in settings.MUNIN_NODES:
        if isinstance(node, tuple):
            if node[1].get('version', 'v2') == 'v1':
                MNODES.append(node)
        else:
            raise ImproperlyConfigured('Munin node should be a tupple')
    for node in MuninNodes.objects.filter(munin_version='v1'):
        MNODES.append((node.name, node.as_dict()))
    return MNODES

