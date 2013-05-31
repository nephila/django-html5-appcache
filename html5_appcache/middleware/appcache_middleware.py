# -*- coding: utf-8 -*-
import re
from lxml import etree
from django.utils.translation import ugettext_lazy as _
from lxml.html.html5parser import document_fromstring

from html5_appcache import appcache_registry
from html5_appcache.appcache import AppCacheManager


class AppCacheAssetsFromResponse(object):
    """
    Extracts appcache assets from the rendered template
    """
    _cached = set()
    _network = set()
    _fallback = {}

    def handle_img(self, tag, attrib):
        if 'src' in attrib:
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['src'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['src']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['src'])

    def handle_script(self, tag, attrib):
        if 'src' in attrib:
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['src'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['src']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['src'])

    def handle_link(self, tag, attrib):
        if 'href' in attrib and 'rel' in attrib and attrib['rel']=='stylesheet':
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['href'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['href']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['href'])

    def walk_tree(self, tree):
        if isinstance(tree.tag, basestring):
            t = etree.QName(tree.tag)
            if t.localname == "img":
                self.handle_img(t.localname, tree.attrib)
            if t.localname == "script":
                self.handle_script(t.localname, tree.attrib)
            if t.localname == "link":
                self.handle_link(t.localname, tree.attrib)
            for node in tree:
                self.walk_tree(node)

    def process_response(self, request, response):
        if response['Content-Type'].find("text/html")>-1:
            lxdoc = document_fromstring(response.content)
            self.walk_tree(lxdoc)
            response.appcache = {'cached': self._cached,
                                 'fallback': self._fallback,
                                 'network': self._network}
        return response