.. _installation:

************
Installation
************

Requirements
------------

* ``django>=1.4``
* ``lxml``
* ``html5lib``

Installation
------------

To get started using ``django-html5-appcache`` install it with ``pip``::

    $ pip install git+https://github.com/nephila/django-html5-appcache.git#egg=django-html5-appcache

Requirements will be automatically installed.

Basic configuration
--------------------

* Add ``html5_appcache`` to ``INSTALLED_APPS``.
* Include in your ``URLCONF``::

    urlpatterns += patterns('',
        url('^', include('html5_appcache.urls')),
    )

.. warning::
    on Django 1.4+ (or django CMS 2.4+) you may need to use ``i18npatterns``
    instead of ``patterns`` above, depending on you project layout.

* Enable appcache discovery by adding the lines below in ``urls.py``::

    import html5_appcache
    html5_appcache.autodiscover()

* Add the middleware just below ``django.middleware.cache.UpdateCacheMiddleware``,
  if used, or at the topmost position::

    'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse'

* Insert ``appcache_link`` template tag in your templates::

   {% load appcache_tags  %}
   <html {% appcache_link %} >
    <head>
    ...
    </head>
    <body>
    ...
    </body>
   </html>

* Enable the cache for your project. Refer to Django :django:setting:`CACHES`
  configuration.

django CMS integration
----------------------

``django-html5-appcache`` supports django CMS out-of-the-box.
To enable, add the following to ``INSTALLED_APPS``:

* ``html5_appcache.packages.cms``
* ``html5_appcache.packages.filer`` (if you use ``django-filer``)
* ``html5_appcache.packages.cmsplugin_filer`` (if you use ``cmsplugin_filer``)

django CMS integration delivers support for all the the default plugins; to enable
your own plugins see :ref:`djangocms-plugins` section in :ref:`appcache`.