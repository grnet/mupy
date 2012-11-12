from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    
    url(r'^(?P<search_id>\d+)?$', 'mupy.muparse.views.home', name='home'),
    url(r'^json_cat/(?P<user_id>\w+)/$', 'mupy.muparse.views.get_node_tree_category', name='getjson_category'),
    url(r'^json/(?P<user_id>\w+)/$', 'mupy.muparse.views.get_node_tree', name='getjson_all'),
    url(r'^savesearch$', 'mupy.muparse.views.save_search', name='save_search'),
    url(r'^savedearches$', 'mupy.muparse.views.saved_searches', name='saved_searches'),
    url(r'^loadsearch/(?P<search_id>\d+)?$', 'mupy.muparse.views.load_search', name='load_search'),
    url(r'^newpage/(?P<search_id>\d+)/$', 'mupy.muparse.views.load_search_blank', name='load_search_blank'),
    url(r'^delete/(?P<search_id>\d+)?$', 'mupy.muparse.views.delete_search', name='delete_search'),
    )
