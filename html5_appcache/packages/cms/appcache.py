# -*- coding: utf-8 -*-
from cms.models import Page, Title
from cms.plugins.file.models import File
from cms.plugins.flash.models import Flash
from cms.plugins.googlemap.models import GoogleMap
from cms.plugins.link.models import Link
from cms.plugins.picture.models import Picture
from cms.plugins.video.models import Video
from cms.plugins.teaser.models import Teaser
from cms.plugins.twitter.models import TwitterRecentEntries, TwitterSearch
from cms.plugins.inherit.models import InheritPagePlaceholder

from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache


class CmsAppCache(BaseAppCache):
    """
    Appcache file form django CMS models
    """
    models = (Page, Title, File, Flash, GoogleMap, Link, Picture, Video,
              TwitterSearch, TwitterRecentEntries, InheritPagePlaceholder,
              Teaser)

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()
appcache_registry.register(CmsAppCache())

try:
    # This will fail with django CMS 3.0+
    from cms.plugins.text.models import Text

    class CmsTextAppCache(BaseAppCache):
        models = (Text, )
        manager = None

        def signal_connector(self, instance, **kwargs):
            self.manager.reset_manifest()
    appcache_registry.register(CmsTextAppCache())
except ImportError:
    pass
