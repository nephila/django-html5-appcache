# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import ManifestAppCache

urlpatterns = patterns('',
    url("^manifest.appcache$",
        ManifestAppCache.as_view(),
        name="appcache_manifest")
)
