# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView

from html5_appcache.test_utils.testapp.models import News


class NewsListView(ListView):
    model = News

class NewsDetailView(DetailView):
    model = News