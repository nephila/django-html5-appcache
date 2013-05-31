# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from .models import News


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = "0.5"
    multisite = False
    model = News

    def items(self):
        if self.multisite:
            return self.model.objects.filter(published=True).filter(sites=Site.objects.get_current())
        else:
            return self.model.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.modification_date