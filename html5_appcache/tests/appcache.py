# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.test import RequestFactory

from html5_appcache.cache import (set_cached_manifest, get_cached_manifest,
                                  clear_cache_manifest)
from html5_appcache.test_utils import setup_view
from html5_appcache.test_utils.base import BaseDataTestCase
from html5_appcache.test_utils.testapp.models import News
from html5_appcache.views import ManifestAppCache


class AppcacheTestCase(BaseDataTestCase):

    def tearDown(self):
        clear_cache_manifest()
        super(AppcacheTestCase, self).tearDown()

    def test_context_sitemap(self):
        request = RequestFactory().get('/fake-path')
        view = ManifestAppCache()
        view = setup_view(view, request)
        response = view.get(request)
        self.assertEqual(len(view.manager.context['cached_urls']), 3)

    def test_context_no_sitemap(self):
        with self.settings(HTML5_APPCACHE_USE_SITEMAP=False):
            request = RequestFactory().get('/fake-path')
            view = ManifestAppCache()
            view = setup_view(view, request)
            response = view.get(request)
            self.assertEqual(len(view.manager.context['cached_urls']), 3)

    def test_signal_save(self):
        set_cached_manifest("dummy")
        news1 = News.objects.get(pk=1)
        news1.title = "news1b"
        news1.save()
        manifest = get_cached_manifest()
        self.assertIsNone(manifest)

    def test_signal_delete(self):
        set_cached_manifest("dummy")
        news3 = News.objects.create(title="news3", body="body3")
        news3.delete()
        manifest = get_cached_manifest()
        self.assertIsNone(manifest)


class UpdateCommandTestCase(BaseDataTestCase):

    def tearDown(self):
        clear_cache_manifest()
        super(UpdateCommandTestCase, self).tearDown()

    def test_update_command(self):
        t_cache = """CACHE:
/
/1/
/2/
/some/url/css/stile.css
/static/img/icon1.png
/static/img/icon2.png
"""
        t_network = """NETWORK:
/1/live/
/2/live/
http://www.example.com/static/css/stile.css
"""
        t_fallback = """FALLBACK:
http://www.example.com/static/img/icon1.png /static/img/fallback.png
http://www.example.com/static/img/icon2.png /static/img/fallback.png
"""
        call_command("update_manifest")
        manifest = get_cached_manifest()
        self.assertTrue(manifest.find("CACHE MANIFEST")>-1)
        self.assertTrue(manifest.find(t_cache)>-1)
        self.assertTrue(manifest.find(t_network)>-1)
        self.assertTrue(manifest.find(t_fallback)>-1)