# MUPY

<img src="https://github.com/grnet/mupy/blob/master/mupy/static/images/mupy_logo.png" alt="MuPy">

## What is Mupy?

Mupy is a Munin Python Parser. It is written in Python and is powered by Django framework.
Its functionality is pretty straightforward. It parses the HTML DOM of a munin site, stores the graphable
data into a db and provides a friendly user interface for retrieving munin graphs.

### Features
- parse multiple Munin instances
- save a search and use it again later
- set permissions, which hosts can be seen by a specific user.


### Munin version compatibility
Mupy was built on Munin version 1.4.5, but is supports version 2 as well.


## Installation

### Installation Requirements
Mupy's installation and operation depends on the following modules/packages

* python-django (>=1.4.5)
* python-mysqldb
* python-ldap (if ldap user auth is needed)
* python-bs4 (won't work with <4)
* memcached
* python-django-south

1. Untar the package (or clone via git) to your desired location, copy sample_local_settings.py to local_settings.py, apache/django.wsgi.dist to local files ommiting dist and edit loca_settings.py and apache/django.wsgi according to your needs. Pay special attention to:
	- `MUNIN_URL` : url that munin welcome page lives, eg. "http://munin.example.com"
	- `MUNIN_CGI_PATH` : if images are updated frequently (without the need to visit) then set the cgi path here, eg. "cgi-bin/munin-cgi-graph/"

2. To serve via Apache (static files),
create an alias for the static dir in your apache conf and a WSGI script alias eg.

		Alias /static       /<installation_location>/mupy/static
		WSGIScriptAlias /      /<installation_location>/mupy/apache/django.wsgi

3. Copy `sample_local_settings.py` to `local_settings.py`
4. Run `./manage.py syncdb --noinput`
5. Run `./manage.py migrate`
6. Run `./manage.py createsuperuser`
7. Run `./manage.py collectstatic`
8. Run `./manage.py parse_munin2` to parse the `MUNIN_URL` and store data into db. In case you have an older version of munin you have to run `./manage parse_munin`. A daily cronjob of this command is suggested.
9. Restart Apache (or `touch apache/django.wsgi`) and enjoy


## Documentation
Here is a small description of the way that mupy should be used.
The idea is to let each account monitor only some of the hosts.

### Settings
The munin nodes are stored in the dictionary `MUNIN_NODES` in local_settings.py.
Look at sample_local_settings for an example.

### Usage
Whenever a user is created, the administrator (set in the `ADMIN` in
local_settings), receives an email notification to go and chose which hosts can
 be viewed by the new user. The new user cannot see any host by default.

#### Selecting which hosts can be viewed by users
In the administration panel (`/admin/`), there is a link named `user profiles`
under `Accounts` section. Select it, then select `add user profile`. There
should be a select input with the names of the existing users (you can add a
new one by clicking the `+` button). Then there is a multy-select box with host
names. Move the nodes that the user will be able to see on the box below. Save
the changes.

### Screenshot

<img src="https://github.com/grnet/mupy/blob/master/mupy/static/images/mupy_screenshot.jpeg" alt="MuPy">

