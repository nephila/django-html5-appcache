**************************************
Managing urls presence in the manifest
**************************************

Sometimes you don't want urls to be cached for various reasons (they can pull
content from external sites with no way to invalidate the local cache, or
they are just non meant to be available offline), or you want to insert
non-discoverable urls in it.
As there is not one-size-fit-all in managing urls in manifest,
``django-html5-appcache`` offers different methods to get the urls **in** or **out**
of the manifest file to meet as many usecases as possible.

Configuration
-------------

To include urls in the manifest, use :setting:`HTML5_APPCACHE_CACHED_URL`,
to exclude them use :setting:`HTML5_APPCACHE_EXCLUDE_URL`.

To insert a URL in **NETWORK** see :setting:`HTML5_APPCACHE_NETWORK_URL`; for
**FALLBACK** see :setting:`HTML5_APPCACHE_FALLBACK_URL`.


AppCache class
--------------

In the ``AppCache`` classes, is it possible to override methods to fine-tune
the urls in each section of the manifest file:

* :py:meth:`BaseAppCache._get_urls <html5_appcache.appcache_base.BaseAppCache._get_urls>`:
  to add urls to the **CACHE** section
* :py:meth:`BaseAppCache._get_assets <html5_appcache.appcache_base.BaseAppCache._get_assets>`:
  to add assets to the **CACHE** section
* :py:meth:`BaseAppCache._get_network <html5_appcache.appcache_base.BaseAppCache._get_network>`:
  to add urls to the **NETWORK** section
* :py:meth:`BaseAppCache._get_fallback <html5_appcache.appcache_base.BaseAppCache._get_fallback>`:
  to add urls to the **FALLBACK** section


.. _markup-customization:

Markup
------

When using :setting:`sitemap <HTML5_APPCACHE_USE_SITEMAP>`, by default
every relative URL is considered to be cached, while external URLs are not cached.
It's possible to control the behavior of each url by using custom attributes
in your tags.

For each ``img``, ``script`` and ``link`` tag, you can add data-attributes to
control how each referenced url is considered:

* `data-appcache='appcache'`: the referenced url is added to the CACHEe section
* `data-appcache='noappcache'`: the referenced url is added to the NETWORK section
* `data-appcache-fallback=URL`: the referenced url is added in the FALLBACK section, with *URL* as a target
