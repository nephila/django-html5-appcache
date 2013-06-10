.. _configuration:

**********************
Advanced configuration
**********************

While no specific configuration is needed to run ``html5-appcache``, you can
customize its behavior for your own needs with the following parameters:

.. setting:: HTML5_APPCACHE_DISABLE

HTML5_APPCACHE_DISABLE
======================

If you want to keep ``django-html5-appcache`` installed but you want to disable
it temporarely (for debug purposes, for example), set this parameter to ``True``:
it makes the manifest view return a non-caching manifest file and disables ``appcache_link``
templatetag.

.. versionadded:: 0.3.0

*Defaults*: ``False``

.. setting:: HTML5_APPCACHE_ADD_WILDCARD

HTML5_APPCACHE_ADD_WILDCARD
===========================
If ``True`` a wildcard entry is added in network section to allow browser to
download files not in the ``CACHE`` section.

.. versionadded:: 0.3.0

*Defaults*: ``True``

.. setting:: HTML5_APPCACHE_CACHE_KEY

HTML5_APPCACHE_CACHE_KEY
========================

Name of the cache key.

*Defaults*: ``html5_appcache``

.. setting:: HTML5_APPCACHE_CACHE_DURATION

HTML5_APPCACHE_CACHE_DURATION
=============================

Duration of the cache values.

*Default*: ``86400`` seconds

.. setting:: HTML5_APPCACHE_USE_SITEMAP

HTML5_APPCACHE_USE_SITEMAP
==========================

``django-html5-appcache`` can leverage the ``sitemap`` application of django to
discover the cacheable urls. If you want to disable, you must provide a urls list.

*Default*: ``True``

.. setting:: HTML5_APPCACHE_CACHED_URL

HTML5_APPCACHE_CACHED_URL
=========================

It's possible to provide a list of urls to include in the manifest file as cached
urls, if it's not discoverable by the django application (e.g.: it's not managed
by django or not linked to any page).

*Default*: ``[]``

.. setting:: HTML5_APPCACHE_EXCLUDE_URL

HTML5_APPCACHE_EXCLUDE_URL
==========================

It's possible to exclude specific url from being cached by using this parameter.
Contrary to :setting:`HTML5_APPCACHE_NETWORK_URL` URLs will be excluded by
cached urls but are **not** set in the **NETWORK** section of the manifest.
This way you can mask out *private* URLs or URLs that are not meant to be known.

.. warning::
    This is **not** a security feature. *Security through obscurity* is broken
    by design. This parameter is intended only to have a cleaner and more concise
    manifest.

.. versionadded:: 0.3.2

*Default*: ``[]``

.. setting:: HTML5_APPCACHE_NETWORK_URL

HTML5_APPCACHE_NETWORK_URL
==========================

You can exclude specific url from being cached by using this parameter.
URLs will be excluded by cached urls and set in the **NETWORK** section of the manifest.

*Default*: ``[]``

.. setting:: HTML5_APPCACHE_FALLBACK_URL

HTML5_APPCACHE_FALLBACK_URL
===========================

It's possible to provide a dictionary of urls to be included in the **FALLBACK**
section. Key is the *original* url, value is the *fallback* url.

*Default*: ``{}``

.. setting:: HTML5_APPCACHE_OVERRIDE_URLCONF

HTML5_APPCACHE_OVERRIDE_URLCONF
===============================

When using **django CMS** apphooks, you must provide an alternative urlconf for
``django-html5-appcache`` to be able to traverse the application urls, due to way
apphooks works.
See the **django CMS integration** section to know more (WiP)

*Default*: ``False``

.. setting:: HTML5_APPCACHE_OVERRIDDEN_URLCONF

HTML5_APPCACHE_OVERRIDDEN_URLCONF
=================================

This is used internally by ``django-html5-appcache`` and should remain to its
default value.

*Default*: ``False``
