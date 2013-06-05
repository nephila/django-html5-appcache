# -*- coding: utf-8 -*-
from urlparse import urlparse


def is_external_url(url, request=None):
    """
    Check if a protocol is declared and SERVER_NAME differs from the domain in
    the URL
    """
    path = urlparse(url)
    ext_server = True
    if request:
        ext_server = (
            "%s:%s" % (request.META['SERVER_NAME'], request.META['SERVER_PORT']) !=
            path.netloc
        )
    return len(path.scheme) != 0 and ext_server

def cache_badge(request, context, _template="html5_appcache/templatetags/icon.html"):
    """
    Renders the cache badge template
    """
    from django.template import RequestContext
    from django.template.loader import render_to_string
    template_context = RequestContext(request, context)
    return render_to_string(_template, context_instance=template_context)
