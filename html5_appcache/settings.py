# -*- coding: utf-8 -*-
from django.conf import settings

def get_setting(key):
    local_settings = {
        'CACHE_KEY': getattr(settings, "HTML5_APPCACHE_CACHE_KEY", "html5_appcache"),
        'CACHE_DURATION': getattr(settings, "HTML5_APPCACHE_CACHE_DURATION", 86400),
        'USE_SITEMAP': getattr(settings, "HTML5_APPCACHE_USE_SITEMAP", True),
        'SITEMAP_URL': getattr(settings, "HTML5_APPCACHE_SITEMAP_URL", "/sitemap.xml"),
        'CACHED_URL': getattr(settings, "HTML5_APPCACHE_CACHED_URL", []),
        'NETWORK_URL': getattr(settings, "HTML5_APPCACHE_NETWORK_URL", []),
        'FALLBACK_URL': getattr(settings, "HTML5_APPCACHE_FALLBACK_URL", {}),
        'OVERRIDE_URLCONF': getattr(settings, "HTML5_APPCACHE_OVERRIDE_URLCONF", False),
        'OVERRIDDEN_URLCONF': getattr(settings, "HTML5_APPCACHE_OVERRIDDEN_URLCONF", False),
    }
    return local_settings[key]