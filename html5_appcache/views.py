# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.generic import TemplateView

from . import appcache_registry
from html5_appcache.appcache import AppCacheManager


class ManifestAppCache(TemplateView):
    template_name = "html5_appcache/manifest"
    manager = None

    def get(self, request, *args, **kwargs):
        self.manager = AppCacheManager(self.request, appcache_registry, self.template_name)
        manifest = self.manager.get_manifest()
        return HttpResponse(content=manifest, content_type="text/cache-manifest")