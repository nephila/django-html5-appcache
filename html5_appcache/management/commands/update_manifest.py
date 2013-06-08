# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from django.test import RequestFactory, Client
from django.test.utils import override_settings

from html5_appcache import appcache_registry
from html5_appcache.cache import clear_cache_manifest
from html5_appcache.settings import get_setting
from html5_appcache.utils import is_external_url


class Command(BaseCommand):
    """
    This command update the manifest in the cache.

    * It loads the declared urls (using sitemap or appcache classes)
    * Explores the above urls scanning for assets.

    When using django CMS you must set ``HTML5_APPCACHE_OVERRIDDE_URLCONF=True``
    to enable using the static urlconf.
    """
    help = 'Update appcache manifest loading all the pages from the sitemap.' \
           'Manifest is loaded in the cache.'
    language = None

    def handle(self, *args, **options):
        self.language = "en"
        request = RequestFactory().get('/')
        request.LANGUAGE_CODE = self.language
        appcache_registry.setup(request, "html5_appcache/manifest")
        if get_setting("OVERRIDE_URLCONF"):
            return self.get_overridden_urls()
        else:
            return self.get_urls()

    def get_urls(self):
        clear_cache_manifest()
        appcache_registry.extract_urls()
        appcache_registry.get_manifest(update=True)

    @override_settings(HTML5_APPCACHE_OVERRIDDEN_URLCONF=True)
    def get_overridden_urls(self):
        from cms.appresolver import clear_app_resolvers
        from django.core.urlresolvers import clear_url_caches
        clear_app_resolvers()
        clear_url_caches()
        return self.get_urls()
