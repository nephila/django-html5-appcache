=====================
django-html5-appcache
=====================

.. image:: https://travis-ci.org/nephila/django-html5-appcache.png?branch=master
   :align: right

Application to manage HTML5 Appcache Manifest files for dynamic Django web applications.

While handy and quite simple in its structure, manifest files is quite burdensome
to keep up-to-date on dynamic websites.

``django-html5-appcache`` try to make this effortless, exploiting the batteries
included in Django to discover pages and assets as they are updated by the users.

While still in pre-alpha state it should be usable, at least for testing purposes.

Documentation is in progress.

At the moment it's only available from github, a later release on PyPi is planned
as soon as code is stabilized and full docs are written.

As generating manifest file can be quite resource intensive for larger sites,
it uses the Django cache system.

Requirements
------------

* `django>=1.4` (prior versions could work, but are not tested)
* `lxml`
* `html5lib`

Installation
------------

To get started using ``django-html5-appcache`` install it with ``pip``::

    $ pip install https://github.com/nephila/django-html5-appcache.git

Configuration
-------------

**Still WiP**

* Add ``html5-appcache`` to ``INSTALLED_APPS``.
* Add it to ``URLCONF``::

    urlpatterns = patterns('',
        url('^', include('django_appcache.urls')),
    )

Customization
#############

No further configuration is needed to make ``html5-appcache`` to run; you can
customize its behavior for your own needs with the following parameters:

HTML5_APPCACHE_CACHE_KEY
========================

Name of the cache key.

*Defaults*: `html5_appcache`

HTML5_APPCACHE_CACHE_DURATION
=============================

Duration of the cache values.

*Default*: `86400` seconds

HTML5_APPCACHE_USE_SITEMAP
==========================

``django-html5-appcache`` can leverage the ``sitemap`` application of django to
discover the cacheable urls. If you want to disable, you must provide a urls list.

*Default*: `True`

HTML5_APPCACHE_CACHED_URL
=========================

It's possible to provide a list of urls to include in the manifest file as cached
urls, if it's not discoverable by the django application (e.g.: it's not managed
by django or not linked to any page).

*Default*: `[]`

HTML5_APPCACHE_NETWORK_URL
==========================

You can exclude specific url from being cached by using this parameter.
Urls will be excluded by cached urls and set in the **network** section.

*Default*: `[]`

HTML5_APPCACHE_FALLBACK_URL
===========================

It's possible to provide a dictionary of urls to be included in the fallback
section. Key is the *original* url, value is the *fallback* url.

*Default*: `{}`

HTML5_APPCACHE_OVERRIDE_URLCONF
===============================

When using **django CMS** apphooks, you must provide an alternative urlconf for
``django-html5-appcache`` to be able to traverse the application urls, due to way
apphooks works.
See the **django CMS integration** section to know more (WiP)

*Default*: `False`

HTML5_APPCACHE_OVERRIDDEN_URLCONF
=================================

This is used internally by ``django-html5-appcache`` and should remain to its
default value.

*Default*: `False`
