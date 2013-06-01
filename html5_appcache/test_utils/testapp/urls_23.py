# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.contrib import admin

import html5_appcache
html5_appcache.autodiscover()

from .sitemap import NewsSitemap
from .views import NewsListView, NewsDetailView

sitemaps = {
    'news': NewsSitemap,
}

urlpatterns = patterns('',
    url("^list/$", NewsListView.as_view(), name="news_list"),
    url("^(?P<pk>\d+)/live/", NewsListView.as_view(), name="news_detail_live"),
    url("^(?P<pk>\d+)/$", NewsDetailView.as_view(), name="news_detail"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
if html5_appcache.settings.DJANGOCMS:
    urlpatterns += patterns('',
        url(r'^', include('cms.urls')),
    )