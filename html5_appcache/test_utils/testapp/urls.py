# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

import html5_appcache

html5_appcache.autodiscover()

from .sitemap import NewsSitemap
from .views import NewsListView, NewsDetailView

sitemaps = {
    'news': NewsSitemap,
}

urlpatterns = patterns('',
    url("^$", NewsListView.as_view(), name="news_list"),
    url("^(?P<pk>\d+)/live/", NewsListView.as_view(), name="news_detail_live"),
    url("^(?P<pk>\d+)/$", NewsDetailView.as_view(), name="news_detail"),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
