# -*- coding: utf-8 -*-
"""
Cache maintains two version of the manifest file:
1. if ``get_cache_version() == 1`` it means the all the data are up to date
2. if ``get_cache_version() == 2`` manifest data are stale and need to be regenerated

The use of a version permit to continue serving older, but somehow still valid,
manifest data. Depending on the actual data, it may need immediate update.
"""
from html5_appcache.settings import get_setting

manifest_cache_keys = (
    "manifest", "timestamp", "data_clean"
)


def get_cache_key(key):
    return "%s:%s" % (
        get_setting('CACHE_KEY'), key)


def get_cache_version_key():
    return "%s:version" % get_setting('CACHE_KEY')


def get_cache_version():
    return get_cached_value("data_clean", 1)


def get_cached_value(key, version=None):
    from django.core.cache import cache
    if not version:
        version = get_cache_version()
    return cache.get(get_cache_key(key), version=version)


def set_cached_value(key, value, version=1):
    from django.core.cache import cache
    return cache.set(get_cache_key(key), value, get_setting('CACHE_DURATION'),
                     version=version)


def get_cached_manifest():
    return get_cached_value("manifest")


def set_cached_manifest(manifest):
    """
    When setting new manifest, both versions are updated.
    """
    set_cached_value("data_clean", 1)
    set_cached_value("manifest", manifest, 1)
    set_cached_value("manifest", manifest, 2)


def reset_cache_manifest():
    """
    Move to version 2 (meaning stale data).
    """
    set_cached_value("data_clean", 2)


def is_manifest_clean():
    """
    Signals if the cache is
    """
    return get_cache_version() == 1


def clear_cache_manifest():
    """
    Clear all the values in the cache for both version
    """
    for key in manifest_cache_keys:
        set_cached_value(key, None, 1)
        set_cached_value(key, None, 2)