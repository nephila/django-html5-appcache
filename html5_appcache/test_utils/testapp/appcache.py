# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from html5_appcache import appcache_registry
from html5_appcache.appcache import BaseAppCache

from .models import News

class NewsAppCache(BaseAppCache):
    models = (News, )
    manager = None

    def get_network(self):
        urls = []
        for item in News.objects.filter(published=True):
            urls.append(reverse('news_detail_live', kwargs={'pk': item.pk}))
        return urls

    def get_urls(self):
        urls = [reverse('news_list')]
        for item in News.objects.filter(published=True):
            urls.append(reverse('news_detail', kwargs={'pk': item.pk}))
            # Adding this to later remove it in get_network
            urls.append(reverse('news_detail_live', kwargs={'pk': item.pk}))
        return urls

    def signal_connector(self, instance, **kwargs):
        self.manager.reset_manifest()

appcache_registry.append(NewsAppCache())