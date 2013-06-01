# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.views.decorators.cache import never_cache

from .views import ManifestAppCache

urlpatterns = patterns('',
    url("^manifest.appcache$",
        never_cache(ManifestAppCache.as_view()),
        name="appcache_manifest"),
    #This views is used when updating the manifest. ``appcache_update`` parameter
    #triggers the middleware
    url("^manifest.appcache/appcache_update/$",
        never_cache(ManifestAppCache.as_view(appcache_update=1)),
        name="appcache_manifest_update"),
)