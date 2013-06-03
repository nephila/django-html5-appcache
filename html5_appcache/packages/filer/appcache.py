# -*- coding: utf-8 -*-
from filer.models import File, Image

from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache


class FilerAppCache(BaseAppCache):
    """
    Appcache file form django-filer models
    """
    models = (File, Image)

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()
appcache_registry.register(FilerAppCache())
