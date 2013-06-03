# -*- coding: utf-8 -*-
from urlparse import urlparse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import SimpleTestCase, Client, RequestFactory
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.http import urlencode
from django.utils.importlib import import_module

from html5_appcache import autodiscover
from html5_appcache.settings import DJANGOCMS, DJANGOCMS_2_3
from html5_appcache.cache import clear_cache_manifest
from html5_appcache.test_utils.testapp.models import News


class BaseClient(Client):

    def get_request(self, path, data={}, **extra):
        "Construct a GET request."

        parsed = urlparse(path)
        r = {
            'CONTENT_TYPE':    str('text/html; charset=utf-8'),
            'PATH_INFO':       self._get_path(parsed),
            'QUERY_STRING':    urlencode(data, doseq=True) or force_unicode(parsed[4]),
            'REQUEST_METHOD':  str('GET'),
            }
        r.update(extra)
        return WSGIRequest(self._base_environ(**r))


class BaseDataTestCase(SimpleTestCase):

    client = None

    def get_request(self, path, data={}, language=None, user=None,
                    enforce_csrf_checks=False):

        if user:
            user = authenticate(username=user.username, password=user.username)
        request = self.client.get_request(path, data)
        request._dont_enforce_csrf_checks = not enforce_csrf_checks

        if not language:
            language = settings.LANGUAGE_CODE
        request.LANGUAGE_CODE = language
        if user:
            request.user = user
        else:
            request.user = AnonymousUser()
        return request

    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser(username="admin",
                                                  email="admin@example.com",
                                                  password="admin")
        cls.user = User.objects.create_user(username="staff",
                                            email="staff@example.com",
                                            password="staff")
        super(BaseDataTestCase, cls).setUpClass()
        News.objects.create(title="news1", body="body1")
        News.objects.create(title="news2", body="body2")
        cls.client = BaseClient()
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
        User.objects.all().delete()
        if DJANGOCMS:
            from cms.models import Page
            Page.objects.all().delete()
        super(BaseDataTestCase, cls).tearDownClass()