# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.test import RequestFactory, Client
from django.test.utils import override_settings

from html5_appcache import appcache_registry
from html5_appcache.cache import clear_cache_manifest
from html5_appcache.settings import get_setting


class Command(BaseCommand):
    help = 'Update appcache manifest loading all the pages from the sitemap. Manifest is loaded in the cache.'

    def handle(self, *args, **options):
        self.language = "en"
        request = RequestFactory().get('/fake-path')
        request.LANGUAGE_CODE=self.language
        appcache_registry.setup(request, "html5_appcache/manifest")
        if get_setting("OVERRIDE_URLCONF"):
            return self.get_overridden_urls()
        else:
            return self.get_urls()

    def get_url(self, client, url):
        response = client.get(url, data={"appcache_analyze":1}, LANGUAGE_CODE=self.language)
        if response.status_code == 200:
            appcache_registry.add_appcache(response.appcache)
        elif response.status_code == 302:
            self.get_url(client, response['Location'])
        else:
            print "Unrecognized code %s for %s" % (response.status_code, url)

    def get_urls(self):
        clear_cache_manifest()
        client = Client()
        urls = appcache_registry.get_urls()
        for url in urls:
            self.get_url(client, url)
        manifest = appcache_registry.get_manifest(update=True)

    @override_settings(HTML5_APPCACHE_OVERRIDDEN_URLCONF=True)
    def get_overridden_urls(self):
        from cms.appresolver import clear_app_resolvers
        from django.core.urlresolvers import clear_url_caches
        clear_app_resolvers()
        clear_url_caches()
        return self.get_urls()
