# Django settings for mupy project.
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'mupy')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Stavros Kroustouris', 'staurosk@noc.grnet.gr'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mupy',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'mupy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mupy.wsgi.application'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, 'templates'),
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # third party
    'south',

    # first party
    'muparse',
    'accounts',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'


def _dictmerge(a, b):
    """ deep merge two dictionaries """
    ret = dict(a.items() + b.items())
    for key in set(a.keys()) & set(b.keys()):
        if isinstance(a[key], dict) and isinstance(b[key], dict):
            ret[key] = _dictmerge(a[key], b[key])
    return ret

from local_settings import *  # noqa
for var, val in [i for i in locals().items() if i[0].startswith('EXTRA_')]:
    name = var[len('EXTRA_'):]
    try:
        locals()[name] += val  # append list
    except TypeError:
        locals()[name] = _dictmerge(locals()[name], val)  # merge dict
