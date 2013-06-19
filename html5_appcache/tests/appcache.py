# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.conf import settings

from html5_appcache import appcache_registry
from html5_appcache.cache import *
from html5_appcache.test_utils.base import BaseDataTestCase
from html5_appcache.test_utils.testapp.models import News


class AppcacheTestCase(BaseDataTestCase):

    def tearDown(self):
        clear_cache_manifest()
        super(AppcacheTestCase, self).tearDown()

    def test_context_sitemap(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=True):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            self.assertEqual(len(urls), 3)

    def test_context_no_sitemap(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=False):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            self.assertEqual(len(urls), 3)

    def test_context_sitemap_de(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=True, LANGUAGE_CODE="de"):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            for url in urls:
                self.assertTrue(url.startswith("/de"))

    def test_context_sitemap_en(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=True, LANGUAGE_CODE="en"):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            for url in urls:
                self.assertTrue(url.startswith("/en"))

    def test_include_external_reference(self):
        with self.settings(HTML5_APPCACHE_DISCARD_EXTERNAL=False):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            self.assertEqual(len(urls), 6)

    def test_signal_save(self):
        set_cached_manifest("dummy")
        news1 = News.objects.get(pk=1)
        news1.title = "news1b"
        news1.save()
        self.assertFalse(is_manifest_clean())

    def test_signal_delete(self):
        set_cached_manifest("dummy")
        news3 = News.objects.create(title="news3", body="body3")
        news3.delete()
        self.assertFalse(is_manifest_clean())

    def test_context_exclude(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=False,
                           HTML5_APPCACHE_EXCLUDE_URL=['/en/list/']):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_cached_urls()
            self.assertEqual(len(urls), 2)
            self.assertNotIn('/en/list/', urls)

    def test_context_network(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=False,
                           HTML5_APPCACHE_NETWORK_URL=['/en/list/']):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_network_urls()
            self.assertEqual(len(urls), 4)
            self.assertIn('/en/list/', urls)

    def test_context_fallback(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=False,
                           HTML5_APPCACHE_FALLBACK_URL={'/en/list/': '/other/'}):
            request = self.get_request('/')
            appcache_registry.setup(request, "")
            urls = appcache_registry.get_fallback_urls()
            self.assertEqual(len(urls), 1)
            self.assertEqual(urls['/en/list/'], '/other/')

class UpdateCommandTestCase(BaseDataTestCase):

    def tearDown(self):
        clear_cache_manifest()
        super(UpdateCommandTestCase, self).tearDown()

    def test_clear_command(self):
        set_cached_manifest("dummy")
        call_command("clear_manifest")
        manifest = get_cached_manifest()
        self.assertIsNone(manifest)

    def test_update_command(self):
        lang = "/" + settings.LANGUAGE_CODE
        t_cache = """CACHE:
%s/1/
%s/2/
%s/list/
/some/url/css/stile.css
/static/img/icon1.png
/static/img/icon1_big.png
/static/img/icon2.png
/static/img/icon2_big.png
""" % (lang, lang, lang)
        t_network = """NETWORK:
*
%s/1/live/
%s/2/live/
http://www.example.com/static/css/stile.css
""" % (lang, lang)
        t_fallback = """FALLBACK:
http://www.example.com/static/img/icon1.png /static/img/fallback.png
http://www.example.com/static/img/icon2.png /static/img/fallback.png
"""
        call_command("update_manifest")
        manifest = get_cached_manifest()
        self.assertTrue(manifest.find("CACHE MANIFEST") > -1)
        self.assertTrue(manifest.find(t_cache) > -1)
        self.assertTrue(manifest.find(t_network) > -1)
        self.assertTrue(manifest.find(t_fallback) > -1)