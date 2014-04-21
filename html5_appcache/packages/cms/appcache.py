# -*- coding: utf-8 -*-
from cms.models import Page, Title

from html5_appcache import appcache_registry
from html5_appcache.appcache_base import BaseAppCache




try:
    # These will fail with django CMS 3.0+
    from cms.plugins.text.models import Text
    from cms.plugins.file.models import File
    from cms.plugins.flash.models import Flash
    from cms.plugins.googlemap.models import GoogleMap
    from cms.plugins.link.models import Link
    from cms.plugins.picture.models import Picture
    from cms.plugins.video.models import Video
    from cms.plugins.teaser.models import Teaser
    from cms.plugins.twitter.models import TwitterRecentEntries, TwitterSearch
    from cms.plugins.inherit.models import InheritPagePlaceholder

    class CmsAppCache(BaseAppCache):
        """
        Appcache file form django CMS models
        """
        models = (Page, Title, File, Flash, GoogleMap, Link, Picture, Video,
                  TwitterSearch, TwitterRecentEntries, InheritPagePlaceholder,
                  Teaser, Text)

        def signal_connector(self, instance, **kwargs):
            self.manager.reset_manifest()
    appcache_registry.register(CmsAppCache())
except ImportError:
    from djangocms_text_ckeditor.models import Text
    from djangocms_file.models import File
    from djangocms_flash.models import Flash
    from djangocms_googlemap.models import GoogleMap
    from djangocms_link.models import Link
    from djangocms_picture.models import Picture
    from djangocms_video.models import Video
    from djangocms_teaser.models import Teaser
    from djangocms_twitter.models import TwitterRecentEntries, TwitterSearch
    from djangocms_inherit.models import InheritPagePlaceholder

    class CmsAppCache(BaseAppCache):
        """
        Appcache file form django CMS models
        """
        models = (Page, Title, File, Flash, GoogleMap, Link, Picture, Video,
                  TwitterSearch, TwitterRecentEntries, InheritPagePlaceholder,
                  Teaser, Text)

        def signal_connector(self, instance, **kwargs):
            self.manager.reset_manifest()
    appcache_registry.register(CmsAppCache())
