# -*- coding: utf-8 -*-
from django.test import RequestFactory, TransactionTestCase

from html5_appcache.cache import (get_cached_manifest, set_cached_manifest,
                                  clear_cache_manifest, get_cache_version,
                                  reset_cache_manifest)
from html5_appcache.views import ManifestAppCache


class CacheTest(TransactionTestCase):

    def setUp(self):
        clear_cache_manifest()

    def test_cache(self):
        start = get_cache_version()
        self.assertIsNone(get_cached_manifest())
        set_cached_manifest("ciao")
        self.assertEqual(get_cached_manifest(), "ciao")
        reset_cache_manifest()
        self.assertIsNone(get_cached_manifest())
        self.assertEqual(get_cache_version(), start+1)

    def test_base_view(self):
        request = RequestFactory().get('/fake-path')
        view = ManifestAppCache.as_view()
        response = view(request)
        self.assertContains(response, "CACHE MANIFEST")
