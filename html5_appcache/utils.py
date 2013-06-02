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