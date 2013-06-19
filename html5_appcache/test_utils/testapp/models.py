# -*- coding: utf-8 -*-
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    published = models.BooleanField(default=True)
    modification_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return "news_detail", (), {"pk": self.pk}

    @property
    def icon(self):
        return "/static/img/icon%s.png" % self.pk

    @property
    def icon_big(self):
        return "/static/img/icon%s_big.png" % self.pk

    @property
    def ext_assett(self):
        return "http://www.example.com/static/img/icon%s.png" % self.pk

    @property
    def photo(self):
        return "/media/img/photo%s.png" % self.pk