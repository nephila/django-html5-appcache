# -*- coding: utf-8 -*-
import os.path

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import TemplateView, View

from html5_appcache import appcache_registry
from html5_appcache.cache import is_manifest_clean


class ManifestAppCache(TemplateView):
    """
    Basic template view.
    It just get the temlate from AppCacheManager and wrap it in a response
    """
    template_name = "html5_appcache/manifest"
    appcache_update = 0

    def get(self, request, *args, **kwargs):
        appcache_registry.setup(request, self.template_name)
        if kwargs.get("appcache_update", False):
            if request.user.is_authenticated() and request.user.has_perm('html5_appcache.can_update_manifest'):
                manifest = appcache_registry.get_manifest(update=True)
            else:
                return HttpResponseForbidden(_("Current user is not authorized for this action"))
        else:
            manifest = appcache_registry.get_manifest()
        if manifest:
            return HttpResponse(content=manifest, content_type="text/cache-manifest")
        return HttpResponse(content="CACHE MANIFEST", content_type="text/cache-manifest")


class ManifestUpdateView(ManifestAppCache):
    def get(self, request, *args, **kwargs):
        appcache_registry.setup(request, self.template_name)
        if kwargs.get("appcache_update", False):
            if request.user.is_authenticated() and request.user.has_perm('html5_appcache.can_update_manifest'):
                manifest = appcache_registry.get_manifest(update=True)
                return HttpResponse(content="OK", content_type="text/plain")
            else:
                return HttpResponseForbidden(_("Current user is not authorized for this action"))
        return HttpResponseBadRequest(_("Method not allowed for this view"))


class CacheStatusView(View):
    icons = ('html5_appcache_dirty', 'html5_appcache_clean')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.has_perm('html5_appcache.can_view_cache_status'):
            filepath = os.path.join(settings.STATIC_ROOT, "img", "%s.png" % (
                self.icons[int(is_manifest_clean())]
            ) )
            with open(filepath, "rb") as wrapper:
                response = HttpResponse(list(wrapper), content_type='text/plain')
                response['Content-Length'] = os.path.getsize(filepath)
                return response
        else:
            return HttpResponseForbidden(_("Current user is not authorized for this action"))
