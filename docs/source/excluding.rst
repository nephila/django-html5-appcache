*****************************
Excluding urls from the cache
*****************************

Sometimes you don't want urls to be cached for various reasons (they can pull
content from external sites with no way to invalidate the local cache, or
they are just non meant to be available offline).

``django-html5-appcache`` provides different ways to exclude urls from cache to
meet as many usecases as possible.

Configuration
-------------

To statically exclude urls from cache or add to the fallback section, use
:setting:`HTML5_APPCACHE_NETWORK_URL` and :setting:`HTML5_APPCACHE_NETWORK_URL`.


AppCache class
--------------

In the ``AppCache`` classes, is it possible to override
:py:meth:`BaseAppCache._get_fallback <html5_appcache.appcache_base.BaseAppCache._get_fallback>` and
:py:meth:`BaseAppCache._get_network <html5_appcache.appcache_base.BaseAppCache._get_network>`
to fine-tune the urls in each section of the manifest file.

.. _markup-customization:

Markup
------

When using :setting:`sitemap <HTML5_APPCACHE_USE_SITEMAP>`, by default
every relative URL is considered to be cached, while external URLs are not cached.
It's possible to control the behavior of each url by using custom attributes
in your tags.

For each ``img``, ``script`` and ``link`` tag, you can add data-attributes to
control how each referenced url is considered:

* `data-appcache='noappcache'`: the referenced url is added to the NETWORK section
* `data-appcache-fallback=URL`: the referenced url is added in the FALLBACK section, with *URL* as a target
