# -*- coding: utf-8 -*-
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
        return mark_safe('manifest="%s"' % reverse('appcache_manifest'))
register.tag('appcache_link', appcache_link)