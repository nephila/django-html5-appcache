# -*- coding: utf-8 -*-
import sys
import os

from html5_appcache.settings import DJANGOCMS, DJANGOCMS_2_3

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
ROOT_URLCONF = 'html5_appcache.test_utils.testapp.urls'
CMS_TEMPLATES = ()
CMS_LANGUAGES = ()
CMS_FRONTEND_LANGUAGES = ()
CMS_MENU_TITLE_OVERWRITE = False
# We need to modifiy settings according to the django CMS version available
if DJANGOCMS:
    if DJANGOCMS_2_3:
        MIDDLEWARE_CLASSES =  [
            'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.doc.XViewMiddleware',
            'cms.middleware.multilingual.MultilingualURLMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
        ]
        ROOT_URLCONF = 'html5_appcache.test_utils.testapp.urls_23'
        INSTALLED_APPS =  INSTALLED_APPS + [
            'cms',
            'mptt',
            'menus',
            'sekizai'
        ]
        TEMPLATE_CONTEXT_PROCESSORS = [
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'cms.context_processors.media',
            'sekizai.context_processors.sekizai',
        ]
        CMS_TEMPLATES = (
            ('base.html', 'Template One'),
        )
        CMS_LANGUAGES = (('en', 'English'),('de','German'),('it','Italian'))
        CMS_FRONTEND_LANGUAGES = [lang[0] for lang in CMS_LANGUAGES]
        ROOT_URLCONF = 'html5_appcache.test_utils.testapp.urls_23'
    else:
        MIDDLEWARE_CLASSES = [
            'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.doc.XViewMiddleware',
            'django.middleware.common.CommonMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
        ]
        INSTALLED_APPS = INSTALLED_APPS + [
            'cms',
            'mptt',
            'menus',
            'sekizai',
            'filer',
            'html5_appcache.packages.cms',
            'html5_appcache.packages.filer',
            'html5_appcache.packages.cmsplugin_filer',
        ]
        TEMPLATE_CONTEXT_PROCESSORS = [
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'cms.context_processors.media',
            'sekizai.context_processors.sekizai',
        ]
        CMS_TEMPLATES = (
            ('base.html', 'Template One'),
        )
        CMS_LANGUAGES = {
            'default': {
                'fallbacks': ['en', 'de', 'it'],
                'redirect_on_fallback': True,
                'public': True,
                'hide_untranslated': False,
            }
        }
        CMS_FRONTEND_LANGUAGES = CMS_LANGUAGES['default']['fallbacks']
else:
    MIDDLEWARE_CLASSES = [
        'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.doc.XViewMiddleware',
    ]
    
    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
]


def run_tests():

    from django.conf import settings

    settings.configure(
        SITE_ID=1,
        INSTALLED_APPS=INSTALLED_APPS,
        MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
        TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory',
            }
        },
        ROOT_URLCONF=ROOT_URLCONF,
        USE_I8N=True,
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'),('de','German'),('it','Italian')),
        STATIC_URL='/some/url/',
        STATIC_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'static'),
        TEST_OUTPUT_VERBOSE=True,
        CMS_TEMPLATES=CMS_TEMPLATES,
        CMS_MODERATOR=False,
        CMS_PERMISSION=False,
        CMS_LANGUAGES=CMS_LANGUAGES,
        CMS_FRONTEND_LANGUAGES=CMS_FRONTEND_LANGUAGES,
        CMS_MENU_TITLE_OVERWRITE=False,
        CMS_SOFTROOT=False,
        CMS_SHOW_START_DATE=True,
        CMS_SHOW_END_DATE=True,
        CMS_SEO_FIELDS=True,
        CMS_URL_OVERWRITE=True,
        CMS_REDIRECTS=True,
        CMS_APPHOOKS=False,
        CMS_TEMPLATE_INHERITANCE_MAGIC=True,
        CMS_PAGE_CHOICES_CACHE_KEY="foo",
        CMS_SITE_CHOICES_CACHE_KEY="foo",
        CMS_FLAT_URLS=False,
        CMS_MEDIA_URL='/some/url/',
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