# -*- coding: utf-8 -*-
from django.test import SimpleTestCase, Client

from html5_appcache.cache import clear_cache_manifest
from html5_appcache.test_utils.testapp.models import News


class BaseDataTestCase(SimpleTestCase):

    client = None

    @classmethod
    def setUpClass(cls):
        super(BaseDataTestCase, cls).setUpClass()
        News.objects.create(title="news1", body="body1")
        News.objects.create(title="news2", body="body2")
        cls.client = Client()
        cls.client.get("/")

    @classmethod
    def tearDownClass(cls):
        clear_cache_manifest()
        News.objects.all().delete()
        super(BaseDataTestCase, cls).tearDownClass()