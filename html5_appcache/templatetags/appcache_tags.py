# -*- coding: utf-8 -*-
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


def appcache_link(parser, token):
    """
    Add the correct attribute to th ``<html>`` tag
    """
    return AppCacheNode()


class AppCacheNode(template.Node):
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
    _template = "html5_appcache/templatetags/icon.html"

    def __init__(self):
        pass

    def render(self, context):
        local = {}
        template_context = RequestContext(context['request'], local)
        rendered = render_to_string(self._template, context_instance=template_context)
        return rendered
register.tag('appcache_icon', appcache_icon)
