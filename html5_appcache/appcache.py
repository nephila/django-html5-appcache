# -*- coding: utf-8 -*-
from datetime import datetime
import time
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.test import Client
from django.db.models.signals import post_save, post_delete
from html5_appcache.cache import reset_cache_manifest, get_cached_manifest, get_cached_value, set_cached_value, set_cached_manifest

from .settings import get_setting


class BaseAppCache(object):

    def __init__(self):
        pass

    def get_assets(self):
        return []

    def get_urls(self):
        return []

    def get_network(self):
        return []

    def get_fallback(self):
        return {}

    def signal_connector(self, instance, **kwargs):
        return NotImplementedError("signal_connector must be implemented for appcache to work")

class AppCacheManager(object):

    def __init__(self, request, registry, template):
        self.request = request
        self.registry = registry
        self._network = set()
        self._cached = set()
        self._fallback = {}
        self._template = template
        self._external_appcaches = {'cached':[], 'network':[], 'fallback':{}}
        self.context = {}
        self._setup_signals()

    def _setup_signals(self):
        for appcache in self.registry:
            appcache.manager = self
            for model in appcache.models:
                post_save.connect(appcache.signal_connector, sender=model)
                post_delete.connect(appcache.signal_connector, sender=model)

    def get_version_timestamp(self):
        timestamp = get_cached_value("timestamp")
        if not timestamp:
            timestamp = int(time.time()*100)*10000 + datetime.utcnow().microsecond
            set_cached_value("timestamp", timestamp)
        return timestamp

    def reset_manifest(self):
        manifest = get_cached_manifest()
        if manifest:
            reset_cache_manifest()

    def get_urls(self):
        urls = set()
        if get_setting('USE_SITEMAP'):
            urls.update(self._get_sitemap())
        for appcache in self.registry:
            urls.update(appcache.get_urls())
        return urls

    def get_cached_urls(self):
        if not self._cached:
            self._cached = self.get_urls()
            for appcache in self.registry:
                self._cached.update(appcache.get_assets())
            self._cached.update(self._external_appcaches['cached'])
        self._cached.difference_update(self.get_network_urls())
        return self._cached

    def get_network_urls(self):
        if not self._network:
            for appcache in self.registry:
                self._network.update(appcache.get_network())
            self._network.update(self._external_appcaches['network'])
        return self._network

    def get_fallback_urls(self):
        if not self._fallback:
            for appcache in self.registry:
                self._fallback.update(appcache.get_fallback())
            self._fallback.update(self._external_appcaches['fallback'])
        return self._fallback

    def add_appcache(self, appcache):
        self._external_appcaches.update(appcache)

    def _get_sitemap(self):
        sitemap = Client().get(get_setting('SITEMAP_URL'))
        req_protocol = 'https' if self.request.is_secure() else 'http'
        req_site = get_current_site(self.request)
        local_urls = []
        urlset = sitemap.context_data['urlset']
        for url in urlset:
            local_urls.append(url['location'].replace("%s://%s" % (req_protocol, req_site), ""))
        return local_urls

    def get_manifest(self):
        manifest = get_cached_manifest()
        if not manifest:
            self.context = {
                'version': self.get_version_timestamp(),
                'cached_urls': sorted(self.get_cached_urls()),
                'network_urls': sorted(self.get_network_urls()),
                'fallback_urls': self.get_fallback_urls(),
            }

            context = RequestContext(self.request, self.context)
            manifest = render_to_string(self._template, context_instance=context)
            set_cached_manifest(manifest)
        return manifest