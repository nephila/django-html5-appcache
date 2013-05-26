# -*- coding: utf-8 -*-
from django.core.cache import cache

from .settings import get_setting

manifest_cache_keys = (
    "manifest", "version", "timestamp"
)

def get_cache_key(key):
    return "%s:%s" % (
        get_setting('CACHE_KEY'), key)

def get_cache_version_key():
    return "%s:version" % get_setting('CACHE_KEY')

def get_cache_version():
    version = cache.get(get_cache_version_key())
    if version is None:
        return 1
    return version

def get_cached_value(key):
    return cache.get(get_cache_key(key), version=get_cache_version())

def set_cached_value(key, value):
    return cache.set(get_cache_key(key), value,
                     get_setting('CACHE_DURATION'),
                     version=get_cache_version())

def get_cached_manifest():
    if get_cached_value("data_clean"):
        return cache.get(get_cache_key("manifest"), version=get_cache_version())
    else:
        version = get_cache_version()
        if version > 1:
            cache.incr(get_cache_version_key())
        else:
            cache.set(get_cache_version_key(), 2,
                      get_setting('CACHE_DURATION'))


def set_cached_manifest(manifest):
    set_cached_value("data_clean", True)
    cache.set(get_cache_key("manifest"), manifest,
              get_setting('CACHE_DURATION'),
              version=get_cache_version())

def reset_cache_manifest():
    set_cached_value("data_clean", False)

def clear_cache_manifest():
    for key in manifest_cache_keys:
        if key != "version":
            cache.set(get_cache_key(key), None, version=get_cache_version())