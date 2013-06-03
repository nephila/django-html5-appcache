# -*- coding: utf-8 -*-
from distutils.version import LooseVersion

import django
from django.conf import settings

try:
    import cms
    DJANGOCMS = True
    DJANGOCMS_2_3 = LooseVersion(cms.__version__) < LooseVersion('2.4')
except ImportError:
    DJANGOCMS = False
    DJANGOCMS_2_3 = False

DJANGO_1_3 = (LooseVersion(django.get_version()) < LooseVersion('1.4') and
              LooseVersion(django.get_version()) >= LooseVersion('1.3'))
DJANGO_1_4 = (LooseVersion(django.get_version()) < LooseVersion('1.5') and
              LooseVersion(django.get_version()) >= LooseVersion('1.4'))
DJANGO_1_5 = (LooseVersion(django.get_version()) < LooseVersion('1.6') and
              LooseVersion(django.get_version()) >= LooseVersion('1.5'))

def get_setting(key):
    local_settings = {
        'DISABLE': getattr(settings, "HTML5_APPCACHE_DISABLE", False),
        'ADD_WILDCARD': getattr(settings, "HTML5_APPCACHE_ADD_WILDCARD", True),
        'CACHE_KEY': getattr(settings, "HTML5_APPCACHE_CACHE_KEY", "html5_appcache"),
        'CACHE_DURATION': getattr(settings, "HTML5_APPCACHE_CACHE_DURATION", 86400),
        'USE_SITEMAP': getattr(settings, "HTML5_APPCACHE_USE_SITEMAP", True),
        'DISCARD_EXTERNAL': getattr(settings, "HTML5_APPCACHE_DISCARD_EXTERNAL", True),
        'SITEMAP_URL': getattr(settings, "HTML5_APPCACHE_SITEMAP_URL", "/sitemap.xml"),
        'CACHED_URL': getattr(settings, "HTML5_APPCACHE_CACHED_URL", []),
        'NETWORK_URL': getattr(settings, "HTML5_APPCACHE_NETWORK_URL", []),
        'FALLBACK_URL': getattr(settings, "HTML5_APPCACHE_FALLBACK_URL", {}),
        'OVERRIDE_URLCONF': getattr(settings, "HTML5_APPCACHE_OVERRIDE_URLCONF", False),
        'OVERRIDDEN_URLCONF': getattr(settings, "HTML5_APPCACHE_OVERRIDDEN_URLCONF", False),
        'DJANGOCMS_2_3': getattr(settings, "HTML5_APPCACHE_DJANGOCMS_2_3", DJANGOCMS_2_3),
        'DJANGOCMS': getattr(settings, "HTML5_APPCACHE_DJANGOCMS", DJANGOCMS),
    }
    return local_settings[key]