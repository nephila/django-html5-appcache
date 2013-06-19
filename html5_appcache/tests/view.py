# -*- coding: utf-8 -*-
import re
from django.core.management import call_command

from html5_appcache.cache import reset_cache_manifest, get_cached_manifest, clear_cache_manifest
from html5_appcache.models import GlobalPermission
from html5_appcache.test_utils.base import BaseDataTestCase
from html5_appcache.views import ManifestAppCache, CacheStatusView, ManifestUpdateView


class ManifestViewTest(BaseDataTestCase):
    version_rx = re.compile(r"version: \$([0-9\.]+)\$")

    @classmethod
    def setUpClass(cls):
        cls.cache_perm = GlobalPermission.objects.create(codename="can_view_cache_status")
        cls.manifest_perm = GlobalPermission.objects.create(codename="can_update_manifest")
        super(ManifestViewTest, cls).setUpClass()

    def setUp(self):
        clear_cache_manifest()

    def test_manifest_version(self):
        request = self.get_request('/', user=self.admin)
        view = ManifestAppCache.as_view(appcache_update=1)
        response = view(request)
        version = self.version_rx.findall(response.content)
        self.assertTrue(version)
        reset_cache_manifest()
        response = view(request)
        version2 = self.version_rx.findall(response.content)
        self.assertNotEqual(version, version2)

    def test_command_view_equivalent(self):
        request = self.get_request('/', user=self.admin)
        view = ManifestAppCache.as_view(appcache_update=1)
        response = view(request)
        # version / date / comments removed as we're interested in
        # extracted urls. stripped for the same reason
        manifest_view = re.sub("# (date|version).+", "", response.content).strip()
        clear_cache_manifest()
        call_command("update_manifest")
        # version / date / comments removed as we're interested in
        # extracted urls. stripped for the same reason
        manifest_command = re.sub("# (date|version).+", "", get_cached_manifest()).strip()
        self.assertEqual(manifest_command, manifest_view)

    def test_update_manifest_view_noauth(self):
        request = self.get_request('/')
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        view = ManifestUpdateView.as_view(appcache_update=1)
        response = view(request)
        self.assertTrue(response.content.find('"success": false') > -1)

    def test_update_manifest_staff(self):
        self.user.user_permissions.add(self.manifest_perm)
        request = self.get_request('/', user=self.user)
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        view = ManifestUpdateView.as_view(appcache_update=1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find("OK") > -1)
        self.user.user_permissions.remove(self.manifest_perm)

        request = self.get_request('/', user=self.user)
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        view = ManifestUpdateView.as_view(appcache_update=1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find('"success": false') > -1)

    def test_update_manifest_no_ajax(self):
        self.user.user_permissions.add(self.manifest_perm)
        request = self.get_request('/', user=self.user)
        view = ManifestUpdateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.user.user_permissions.remove(self.manifest_perm)

    def test_cache_status_noauth(self):
        request = self.get_request('/')
        view = CacheStatusView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_cache_status_staff(self):
        self.user.user_permissions.add(self.cache_perm)
        request = self.get_request('/', user=self.user)
        view = CacheStatusView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.user.user_permissions.remove(self.cache_perm)

        request = self.get_request('/', user=self.user)
        view = CacheStatusView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
