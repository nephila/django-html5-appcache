# -*- coding: utf-8 -*-
from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache

from cms.models import Page, Title

class CmsAppCache(BaseAppCache):
    models = (Page, Title)
    manager = None

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()
appcache_registry.register(CmsAppCache())
