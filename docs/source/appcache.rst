.. _appcache:

************************************
Enabling caching in your application
************************************

``django-html5-appcache`` will automatically include your application urls in
the manifest file the if you have a sitemap-enabled application; however,
to enable cache invalidation, is strongly advised to explicitly enable appcache
support in your application.

Basic support
-------------

For basic appcache support, you must create a ``appcache.py`` in your application
directory (along ``models.py`` file), write an ``AppCache`` class and register it::

    from html5_appcache import appcache_registry
    from html5_appcache.appcache_base import BaseAppCache

    from .models import MyModel, AnotherModel

    class MyModelAppCache(BaseAppCache):
        models = (MyModel, AnotherModel)

        def signal_connector(self, instance, **kwargs):
            self.manager.reset_manifest()
    appcache_registry.register(MyModelAppCache())

This code declare support for ``MyModel`` and ``AnotherModel`` and hooks
``MyModelAppCache.signal_connector`` with ``post_save`` and ``post_delete`` signals.

Anytime you save or delete an instance of ``MyModel`` and ``AnotherModel`` cache
will be marked as **dirty**.

.. _custom-urls:

Custom urls support
-------------------

If you don't have a sitemap or you just want to customize the urls in the manifest
file, you can add methods to the basic ``AppCache`` class above::

    class MyModelAppCache(BaseAppCache):
        ...

        def _get_urls(self, request):
            ...
            return urls

        def _get_assets(self, request):
            ...
            return urls

        def _get_network(self, request):
            ...
            return urls

        def _get_fallback(self, request):
            ...
            return urls

* ``_get_urls(self, request)``: returns a list of urls to be
  included in the ``CACHE`` section of the manifes file;

* ``_get_assets(self, request)``: returns a list of asset urls to be
  included in the ``CACHE`` section of the manifes file; if you add urls in
  ``_get_urls`` method, you have to return the assets in the above urls in this
  method;

* ``_get_network(self, request)``: returns a list of urls to be
  included in the ``NETWORK`` section of the manifes file;

* ``_get_fallback(self, request)``: returns a dictionary of urls to be
  included in the ``FALLBACK`` section of the manifes file; the dictionary key is
  used as the leftmost url in each manifest row, the value as the rightmost
  (i.e: the manifest instruct browser to substitute ``key`` url with ``value`` url
  when offline).

``request`` object is passed for convenience

django CMS plugins
------------------

See :ref:`djangocms-plugins`.