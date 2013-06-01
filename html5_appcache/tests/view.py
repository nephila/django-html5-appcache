# -*- coding: utf-8 -*-
import re

from html5_appcache.cache import reset_cache_manifest
from html5_appcache.test_utils.base import BaseDataTestCase

from html5_appcache.views import ManifestAppCache


class ManifestViewTest(BaseDataTestCase):
    version_rx = re.compile(r"version: \$([0-9\.]+)\$")

    def test_manifest_version(self):
        request = self.get_request('/')
        view = ManifestAppCache.as_view()
        response = view(request, appcache_update=1)
        version = self.version_rx.findall(response.content)
        self.assertTrue(version)
        reset_cache_manifest()
        response = view(request, appcache_update=1)
        version2 = self.version_rx.findall(response.content)
        self.assertNotEqual(version, version2)
