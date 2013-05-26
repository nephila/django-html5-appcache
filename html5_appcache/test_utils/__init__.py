# -*- coding: utf-8 -*-
import sys
import os

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'html5_appcache',
    'html5_appcache.test_utils.testapp',
]

MIDDLEWARE_CLASSES = [
    'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    'django.core.context_processors.static'
]


def run_tests():

    from django.conf import settings

    settings.configure(
        SITE_ID=1,
        INSTALLED_APPS=INSTALLED_APPS,
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES,
        TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory',
            }
        },
        ROOT_URLCONF='html5_appcache.test_utils.testapp.urls',
        USE_I8N=True,
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'),('de','German'),('it','Italian')),
        STATIC_URL='/some/url/',
        STATIC_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir),
        TEST_OUTPUT_VERBOSE = True
    )

    from django.test.utils import get_runner

    failures = get_runner(settings)().run_tests(['html5_appcache'])
    sys.exit(failures)

def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    args and kwargs are the same you would pass to ``reverse()``

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

if __name__ == '__main__':
    run_tests()