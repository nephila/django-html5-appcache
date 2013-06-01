# -*- coding: utf-8 -*-
from django.test import SimpleTestCase, Client, RequestFactory
from django.conf import settings

from html5_appcache import autodiscover
from html5_appcache.settings import DJANGOCMS, DJANGOCMS_2_3
from html5_appcache.cache import clear_cache_manifest
from html5_appcache.test_utils.testapp.models import News


class BaseDataTestCase(SimpleTestCase):

    client = None

    def get_request(self, path, data={}, language=None):
        request = RequestFactory().get(path, data=data)

        request.session = self.client.session
        if not language:
            language = settings.LANGUAGE_CODE
        request.LANGUAGE_CODE = language
        return request

    @classmethod
    def setUpClass(cls):
        super(BaseDataTestCase, cls).setUpClass()
        News.objects.create(title="news1", body="body1")
        News.objects.create(title="news2", body="body2")
        cls.client = Client()
        autodiscover()
        if DJANGOCMS:
            from cms.api import create_page
            for lang in settings.LANGUAGES:
                p = create_page("test%s" % lang[0], language=lang[0],
                                template="base.html")
                p.publish()

    @classmethod
    def tearDownClass(cls):
        clear_cache_manifest()
        News.objects.all().delete()
        if DJANGOCMS:
            from cms.models import Page
            Page.objects.all().delete()
        super(BaseDataTestCase, cls).tearDownClass()