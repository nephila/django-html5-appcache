# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.generic import TemplateView

from . import appcache_registry


class ManifestAppCache(TemplateView):
    """
    Basic template view.
    It just get the temlate from AppCacheManager and wrap it in a response
    """
    template_name = "html5_appcache/manifest"
    appcache_update = 0

    def get(self, request, *args, **kwargs):
        appcache_registry.setup(self.request, self.template_name)
        manifest = appcache_registry.get_manifest(update=kwargs.get("appcache_update", False))
        if manifest:
            return HttpResponse(content=manifest, content_type="text/cache-manifest")
        return HttpResponse(content="CACHE MANIFEST", content_type="text/cache-manifest")