# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.test import RequestFactory, Client
from django.test.utils import override_settings

from html5_appcache import appcache_registry
from html5_appcache.appcache import AppCacheManager
from html5_appcache.settings import get_setting


class Command(BaseCommand):
    help = 'Update appcache manifest loading all the pages from the sitemap. Manifest is loaded in the cache.'

    def handle(self, *args, **options):
        if get_setting("OVERRIDE_URLCONF"):
            print "override?"
            return self.get_overridden_urls()
        else:
            return self.get_urls()

    def get_urls(self):
        request = RequestFactory().get('/fake-path')
        client = Client()
        manager = AppCacheManager(request, appcache_registry, "html5_appcache/manifest")
        urls = manager.get_urls()
        for url in urls:
            response = client.get(url)
            manager.add_appcache(response.appcache)
        manifest = manager.get_manifest()

    @override_settings(HTML5_APPCACHE_OVERRIDDEN_URLCONF=True)
    def get_overridden_urls(self):
        from cms.appresolver import clear_app_resolvers
        from django.core.urlresolvers import clear_url_caches
        clear_app_resolvers()
        clear_url_caches()
        return self.get_urls()
