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

    $ pip install django-html5-appcache

If you want to use the development version install from github::

    $ pip install git+https://github.com/nephila/django-html5-appcache.git#egg=django-html5-appcache

Requirements will be automatically installed.

Run migrate command to sync your database::

    $ python manage.py migrate

.. warning::
    Migrations have been added in 0.3.0. Don't skip this if you are upgrading from
    0.2.

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