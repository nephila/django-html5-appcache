# -*- coding: utf-8 -*-
from html5_appcache.appcache_base import AppCacheManager

__version__ = "0.4.0"

appcache_registry = AppCacheManager()


# TODO: Test with caching disabled

def autodiscover():
    """
    Automatically discover appcache declarations

    Code mostly borrowed from django.contrib.admin.
    """
    import imp
    from django.utils import importlib
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an appcache.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for search_indexes.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own index registration.
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's appcache.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its appcache.py doesn't exist
        try:
            imp.find_module('appcache', app_path)
        except ImportError:
            continue

        # Step 3: import the app's appcache file. If this has errors we want them
        # to bubble up.
        importlib.import_module("%s.appcache" % app)

    appcache_registry.setup_registry()