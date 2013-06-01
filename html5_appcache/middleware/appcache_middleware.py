# -*- coding: utf-8 -*-
import re
from lxml import etree
from lxml.html.html5parser import document_fromstring


class AppCacheAssetsFromResponse(object):
    """
    Extracts appcache assets from the rendered template.

    It supports custom attributes to opt-in / opt-out assets.

    Currently supports the following tags:
    * img: extracts the data in the ``src`` attribute
    * script: extracts the data in the ``src`` attribute
    * link: extracts the data in the ``href`` attribute if ``rel==stylesheet``
    """
    _cached = set()
    _network = set()
    _fallback = {}

    def handle_img(self, tag, attrib):
        """
        Processes the img tag
        """
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
        if (response['Content-Type'].find("text/html")>-1 and
                request.GET.get("appcache_analyze", False)):
            lxdoc = document_fromstring(response.content)
            self.walk_tree(lxdoc)
            response.appcache = {'cached': self._cached,
                                 'fallback': self._fallback,
                                 'network': self._network}
        return response