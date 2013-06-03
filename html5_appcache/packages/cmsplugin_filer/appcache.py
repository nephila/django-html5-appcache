# -*- coding: utf-8 -*-
from cmsplugin_filer_file.models import FilerFile
from cmsplugin_filer_image.models import FilerImage, ThumbnailOption
from cmsplugin_filer_folder.models import FilerFolder
from cmsplugin_filer_link.models import FilerLinkPlugin
from cmsplugin_filer_teaser.models import FilerTeaser
from cmsplugin_filer_video.models import FilerVideo

from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache


class CmspluginFilerAppCache(BaseAppCache):
    """
    Appcache file form cmsplugin filer plugin models
    """
    models = (FilerFile, FilerImage, ThumbnailOption, FilerFolder,
              FilerLinkPlugin, FilerTeaser, FilerVideo)

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()
appcache_registry.register(CmspluginFilerAppCache())
