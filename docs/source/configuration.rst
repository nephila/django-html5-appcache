.. _configuration:

**********************
Advanced configuration
**********************

While no specific configuration is needed to run ``html5-appcache``, you can
customize its behavior for your own needs with the following parameters:

HTML5_APPCACHE_DISABLE
======================

If you want to keep ``django-html5-appcache`` installed but you want to disable
it temporarely (for debug purposes, for example), set this parameter to ``True``:
it makes the manifest view return a non-caching manifest file and disables ``appcache_link``
templatetag.

*Defaults*: ``False``

HTML5_APPCACHE_CACHE_KEY
========================

Name of the cache key.

*Defaults*: ``html5_appcache``

HTML5_APPCACHE_CACHE_DURATION
=============================

Duration of the cache values.

*Default*: ``86400`` seconds

HTML5_APPCACHE_USE_SITEMAP
==========================

``django-html5-appcache`` can leverage the ``sitemap`` application of django to
discover the cacheable urls. If you want to disable, you must provide a urls list.

*Default*: ``True``

HTML5_APPCACHE_CACHED_URL
=========================

It's possible to provide a list of urls to include in the manifest file as cached
urls, if it's not discoverable by the django application (e.g.: it's not managed
by django or not linked to any page).

*Default*: ``[]``

HTML5_APPCACHE_NETWORK_URL
==========================

You can exclude specific url from being cached by using this parameter.
Urls will be excluded by cached urls and set in the **network** section.

*Default*: ``[]``

HTML5_APPCACHE_FALLBACK_URL
===========================

It's possible to provide a dictionary of urls to be included in the fallback
section. Key is the *original* url, value is the *fallback* url.

*Default*: ``{}``

HTML5_APPCACHE_OVERRIDE_URLCONF
===============================

When using **django CMS** apphooks, you must provide an alternative urlconf for
``django-html5-appcache`` to be able to traverse the application urls, due to way
apphooks works.
See the **django CMS integration** section to know more (WiP)

*Default*: ``False``

HTML5_APPCACHE_OVERRIDDEN_URLCONF
=================================

This is used internally by ``django-html5-appcache`` and should remain to its
default value.

*Default*: ``False``
