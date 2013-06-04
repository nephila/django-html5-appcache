# -*- coding: utf-8 -*-
from lxml import etree
from lxml.html.html5parser import document_fromstring


class AppCacheAssetsFromResponse(object):
    """
    Extracts appcache assets from the rendered template.

    Currently supports the following tags:
     * img: extracts the data in the ``src`` attribute
     * script: extracts the data in the ``src`` attribute
     * link: extracts the data in the ``href`` attribute if ``rel==stylesheet``

    It supports custom data-attribute to exclude assets from caching:
     * `data-appcache='noappcache'`: the referenced url is added to the NETWORK
       section
     * `data-appcache-fallback=URL`: the referenced url is added in the
       FALLBACK section, with *URL* as a target

    """
    _cached = set()
    _network = set()
    _fallback = {}

    def handle_img(self, tag, attrib):
        """
        Extract assets from the img tag
        """
        if 'src' in attrib:
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['src'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['src']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['src'])

    def handle_script(self, tag, attrib):
        """
        Extract assets from the script tag
        """
        if 'src' in attrib:
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['src'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['src']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['src'])

    def handle_link(self, tag, attrib):
        """
        Extract assets from the link tag (only for stylesheets)
        """
        if 'href' in attrib and 'rel' in attrib and attrib['rel'] == 'stylesheet':
            if 'data-appcache' in attrib and attrib['data-appcache'] == 'noappcache':
                self._network.add(attrib['href'])
            elif 'data-appcache-fallback' in attrib:
                self._fallback[attrib['href']] = attrib['data-appcache-fallback']
            else:
                self._cached.add(attrib['href'])

    def walk_tree(self, tree):
        """
        Walk the DOM tree
        """
        if isinstance(tree.tag, basestring):
            tag = etree.QName(tree.tag)
            if tag.localname == "img":
                self.handle_img(tag.localname, tree.attrib)
            if tag.localname == "script":
                self.handle_script(tag.localname, tree.attrib)
            if tag.localname == "link":
                self.handle_link(tag.localname, tree.attrib)
            for node in tree:
                self.walk_tree(node)

    def process_response(self, request, response):
        """
        This method is called only if ``appcache_analyze`` parameter is attached
        to the querystring, to avoid overhead during normal navigation
        """
        if (response['Content-Type'].find("text/html")>-1 and
                request.GET.get("appcache_analyze", False)):
            lxdoc = document_fromstring(response.content)
            self.walk_tree(lxdoc)
            response.appcache = {'cached': self._cached,
                                 'fallback': self._fallback,
                                 'network': self._network}
        return response