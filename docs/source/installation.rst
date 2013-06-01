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

Basic configuration
--------------------

For standard django projects
############################

* Add ``html5-appcache`` to ``INSTALLED_APPS``.
* Include in your ``URLCONF``::

    urlpatterns = patterns('',
        url('^', include('html5_appcache.urls')),
    )

* Add the middleware just below ``django.middleware.cache.UpdateCacheMiddleware``
  if used, or at the topmost position::

    'html5_appcache.middleware.appcache_middleware.AppCacheAssetsFromResponse'

* Add the template tag to your templates::

   {% load appcache_templates %}
   <html {% appcache_link %} >
    <head>
    ...
    </head>
    <body>
    ...
    </body>
   </html>

* Enable the cache for your project. Refer to Django :django:setting:`CACHES` configuration.

Using django CMS
################

**TODO**
