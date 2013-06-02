# -*- coding: utf-8 -*-
from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache

from filer.models import File
from cmsplugin_filer_file.models import FilerFile

class FilerAppCache(BaseAppCache):
    models = (File,)
    manager = None

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()
appcache_registry.register(CmsAppCache())
