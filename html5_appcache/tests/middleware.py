# -*- coding: utf-8 -*-
from html5_appcache.middleware.appcache_middleware import AppCacheAssetsFromResponse
from html5_appcache.test_utils.base import BaseDataTestCase
from html5_appcache.test_utils.testapp.views import NewsListView


class MiddlewareTest(BaseDataTestCase):

    def test_middleware_extraction(self):
        request = self.get_request('/', data={'appcache_analyze':1})
        mid_instance = AppCacheAssetsFromResponse()

        view = NewsListView.as_view()
        response = view(request)
        response.render()
        processed = mid_instance.process_response(request, response)
        self.assertTrue(processed.appcache)
        self.assertEqual(len(processed.appcache), 3)

        self.assertEqual(len(processed.appcache['cached']), 4)
        self.assertEqual(len(processed.appcache['fallback']), 2)
        self.assertEqual(len(processed.appcache['network']), 1)