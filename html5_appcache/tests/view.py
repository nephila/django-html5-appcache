# -*- coding: utf-8 -*-
import re

from django.test import SimpleTestCase, RequestFactory
from html5_appcache.cache import reset_cache_manifest

from html5_appcache.views import ManifestAppCache


class ManifestViewTest(SimpleTestCase):
    version_rx = re.compile(r"version: \$([0-9\.]+)\$")

    def test_manifest_version(self):
        request = RequestFactory().get('/fake-path')
        view = ManifestAppCache.as_view()
        response = view(request)
        version = self.version_rx.findall(response.content)
        self.assertTrue(version)
        reset_cache_manifest()
        response = view(request)
        version2 = self.version_rx.findall(response.content)
        self.assertNotEqual(version, version2)
