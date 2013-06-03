# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django import template
from html5_appcache.utils import cache_badge

register = template.Library()


def appcache_link(parser, token):
    """
    Add the correct attribute to th ``<html>`` tag
    """
    return AppCacheNode()


class AppCacheNode(template.Node):
    """ Templatetag Node class """
    def __init__(self):
        pass

    def render(self, context):
        from html5_appcache.settings import get_setting
        if get_setting("DISABLE"):
            return ""
        else:
            return mark_safe('manifest="%s"' % reverse('appcache_manifest'))
register.tag('appcache_link', appcache_link)


def appcache_icon(parser, token):
    """
    Add the cache status icon
    """
    return AppCacheStatusIconNode()


class AppCacheStatusIconNode(template.Node):
    """ Templatetag Node class """
    def __init__(self):
        pass

    def render(self, context):
        return cache_badge(context['request'], {})
register.tag('appcache_icon', appcache_icon)
