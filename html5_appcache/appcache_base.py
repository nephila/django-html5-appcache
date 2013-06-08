# -*- coding: utf-8 -*-
import string
import time
from datetime import datetime
from lxml import etree
from lxml.html import document_fromstring

from django.template import RequestContext
from django.template.loader import render_to_string

from html5_appcache.settings import DJANGOCMS_2_3, get_setting, DJANGO_1_4
from html5_appcache.cache import (get_cached_value, set_cached_value,
                                  is_manifest_clean, reset_cache_manifest,
                                  set_cached_manifest, get_cached_manifest)
from html5_appcache.utils import is_external_url


class BaseAppCache(object):
    """
    Base class for Appcache classes
    """
    manager = None

    def __init__(self):
        pass

    def _add_language(self, request, urls):
        """ For django CMS 2.3 we need to manually add language code to the
        urls returned by the appcache classes

        :return: list of urls
        """
        if DJANGOCMS_2_3:
            new_urls = []
            for url in urls:
                if not is_external_url(url, request):
                    new_urls.append("/%s%s" % (request.LANGUAGE_CODE, url))
                else:
                    new_urls.append(url)
            return new_urls
        else:
            return urls

    def _get_assets(self, request):
        """
        override this method to customize asset (images, files, javascripts,
        stylesheets) urls.

        :return: list of urls
        """
        return []

    def _get_urls(self, request):
        """
        override this method to define cached urls.

        If you use a sitemap-enabled application, it's not normally necessary.

        :return: list of urls
        """
        return []

    def _get_network(self, request):
        """
        override this method to define network (non-cached) urls.

        :return: list of urls
        """
        return []

    def _get_fallback(self, request):
        """
        override this method to define fallback urls.

        :return: dictionary mapping original urls to fallback
        """
        return {}

    def get_assets(self, request):
        """
        Public method that return assets urls. Do not override, use :py:meth:`_get_assets`

        :return: list of urls
        """
        return self._add_language(request, self._get_assets(request))

    def get_urls(self, request):
        """
        Public method that return cached urls. Do not override, use :py:meth:`_get_urls`

        :return: list of urls
        """
        return self._add_language(request, self._get_urls(request))

    def get_network(self, request):
        """
        Public method that return network (non-cached) urls. Do not override, use :py:meth:`_get_network`

        :return: list of urls
        """
        return self._add_language(request, self._get_network(request))

    def get_fallback(self, request):
        """
        Public method that return fallback urls. Do not override, use :py:meth:`_get_fallback`

        :return: dictionary mapping original urls to fallback
        """
        return self._get_fallback(request)

    def signal_connector(self, instance, **kwargs):
        """
        You **must** override this method in you ``AppCache`` class.
        """
        return NotImplementedError("signal_connector must be implemented for appcache to work")


class AppCacheManager(object):
    """
    Main class.
    """
    _cached = set()
    _network = set()
    _fallback = {}
    _external_appcaches = []

    request = None
    _template = None
    context = {}

    def __init__(self):
        self.registry = []

    def register(self, instance):
        self.registry.append(instance)

    def clear(self):
        self.registry = []

    def setup_registry(self):
        """
        Setup the manager bootstrapping the appcache instances
        """
        self._setup_signals()

    def _setup_signals(self):
        """
        Loads the signals for all the models declared in the appcache instances
        """
        from django.db.models.signals import post_save, post_delete
        for appcache in self.registry:
            appcache.manager = self
            for model in appcache.models:
                post_save.connect(appcache.signal_connector, sender=model)
                post_delete.connect(appcache.signal_connector, sender=model)

    def setup(self, request, template):
        """
        Setup is required wen updating the manifest file
        """
        self.request = request
        self.language = getattr(self.request, 'LANGUAGE_CODE', "").split("-")[0]
        self._network = set()
        self._cached = set()
        self._fallback = {}
        self._template = template
        self._external_appcaches = {'cached':[], 'network':[], 'fallback':{}}
        self.context = {}

    def get_version_timestamp(self):
        """
        Create the timestamp according to the current time.

        It tries to make it unique even for very short timeframes
        """
        timestamp = get_cached_value("timestamp")
        if not timestamp:
            timestamp = int(time.time()*100)*10000 + datetime.utcnow().microsecond
            set_cached_value("timestamp", timestamp)
        return timestamp

    def reset_manifest(self):
        """
        Clear the cache (if clean)
        """
        if is_manifest_clean():
            reset_cache_manifest()

    def get_urls(self):
        """
        Retrieves the urls from the sitemap and :meth:`BaseAppCache.get_urls` of
        the appcache instances
        """
        urls = set()
        if get_setting('USE_SITEMAP'):
            urls.update(self._get_sitemap())
        for appcache in self.registry:
            urls.update(appcache.get_urls(self.request))
        return urls

    def get_cached_urls(self):
        """
        Create the cached urls set.

        Merges the assets, the urls, removes the network urls and the external urls

        See :meth:`BaseAppCache.get_urls`, :meth:`get_network_urls`
        """
        if not self._cached:
            self._cached = self.get_urls()
            for appcache in self.registry:
                self._cached.update(appcache.get_assets(self.request))
            self._cached.update(self._external_appcaches['cached'])
        self._cached.difference_update(self.get_network_urls())
        if get_setting('DISCARD_EXTERNAL'):
            self._cached = filter(lambda url: not is_external_url(url, self.request),
                                  self._cached)
        return self._cached

    def get_network_urls(self):
        """
        Create the network urls set.

        ``*`` (wildcard entry) is added when :setting:`ADD_WILDCARD` is True (default)
        """
        if not self._network:
            for appcache in self.registry:
                self._network.update(appcache.get_network(self.request))
            self._network.update(self._external_appcaches['network'])
        if get_setting("ADD_WILDCARD"):
            self._network.update(("*",))
        return self._network

    def get_fallback_urls(self):
        """
        Creates the fallback urls set.
        """
        if not self._fallback:
            for appcache in self.registry:
                self._fallback.update(appcache.get_fallback(self.request))
            self._fallback.update(self._external_appcaches['fallback'])
        return self._fallback

    def add_appcache(self, appcache):
        """
        Adds the externally retrieved urls to the internal set.

        `appcache` is a dictionary with `cached`, `network`, `fallback` keys
        """
        self._external_appcaches.update(appcache)

    def _get_sitemap(self):
        """
        Pretty ugly method that fetches the current sitemap and parses it to
        retrieve the list of available urls
        """
        from django.contrib.sites.models import get_current_site
        from django.test import Client
        from django.contrib.sitemaps.views import sitemap

        def walk_sitemap(urlset, doc):
            """
            Nested function for convenience. Recursively scans the sitemap to
            retrieve the urls
            """
            if isinstance(doc.tag, basestring):
                tag = etree.QName(doc.tag)
                if tag.localname == "loc":
                    urlset.append(doc.text)
            for node in doc:
                urlset = walk_sitemap(urlset, node)
            return urlset
        req_protocol = 'https' if self.request.is_secure() else 'http'
        req_site = get_current_site(self.request)
        client = Client()
        path = get_setting('SITEMAP_URL')
        if DJANGO_1_4 and not DJANGOCMS_2_3:
            path = "/%s%s" % (self.language, get_setting('SITEMAP_URL'))
        sitemap = client.get(path, follow=True, LANGUAGE_CODE=self.language)
        local_urls = []
        lxdoc = document_fromstring(sitemap.content)
        walk_sitemap(local_urls, lxdoc)
        if get_setting('DJANGOCMS_2_3'):
            lang_fix = "/" + self.language
        else:
            lang_fix = ""
        return map(lambda x: string.replace(
            x,"%s://%s" % (req_protocol, req_site), lang_fix),
                   local_urls)

    def _fetch_url(self, client, url):
        """
        Scrape a single URL and fetches assets
        """
        if not is_external_url(url):
            response = client.get(url, data={"appcache_analyze":1}, LANGUAGE_CODE=self.language)
            if response.status_code == 200:
                self.add_appcache(response.appcache)
            elif response.status_code == 302:
                self._fetch_url(client, response['Location'])
            else:
                print("Unrecognized code %s for %s\n" % (
                    response.status_code, url))

    def extract_urls(self):
        """
        Run through the cached urls and fetches assets by scraping the pages
        """
        from django.test import Client
        client = Client()
        urls = self.get_urls()
        for starting_url in urls:
            self._fetch_url(client, starting_url)


    def get_manifest(self, update=False):
        """
        Either get the manifest file out of the cache or render it and save in
        the cache.
        """
        if not is_manifest_clean() and update:
            self.context = {
                'version': self.get_version_timestamp(),
                'date': datetime.fromtimestamp(self.get_version_timestamp()/1000000).isoformat(),
                'cached_urls': sorted(self.get_cached_urls()),
                'network_urls': sorted(self.get_network_urls()),
                'fallback_urls': self.get_fallback_urls(),
            }
            context = RequestContext(self.request, self.context)
            manifest = render_to_string(self._template, context_instance=context)
            set_cached_manifest(manifest)
            return manifest
        else:
            return get_cached_manifest()