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

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^/?$', 'muparse.views.home', name='home'),
    url(r'^menu/$', 'muparse.views.get_menu', name='menu'),
    url(r'^savedsearch/$', 'muparse.views.save_search', name='save_search'),
    url(r'^savedearches/$', 'muparse.views.saved_searches', name='saved_searches'),
    url(r'^loadsearch/(?P<search_id>\d+)/?$', 'muparse.views.load_search', name='load_search'),
    url(r'^default_search/(?P<search_id>\d+)/?$', 'muparse.views.default_search', name='default_search'),
    url(r'^delete/(?P<search_id>\d+)/?$', 'muparse.views.delete_search', name='delete_search'),
)
