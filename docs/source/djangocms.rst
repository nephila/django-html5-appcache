
.. _djangocms:

==========
django CMS
==========

``django-html5-appcache`` supports django CMS out-of-the-box.

django CMS integration delivers support for all the the default plugins; to enable
your own plugins see :ref:`djangocms-plugins` below.

.. _djangocms-installation:

Installation
------------

Plugins
=======

To enable, add the following to ``INSTALLED_APPS``:

* ``html5_appcache.packages.cms``
* ``html5_appcache.packages.filer`` (if you use ``django-filer``)
* ``html5_appcache.packages.cmsplugin_filer`` (if you use ``cmsplugin_filer``)


Apphooks
========

If you use applications hooked to django CMS **AppHooks**, you have to write the
:ref:`AppCache <appcache>` class; if you use the sitemap method to discover
the urls, you **must** add conditional urls loading to the main``urls.py``.

As the scraping uses the internal testserver to deliver the contents, **Apphooks**
are not *hooked* so you have to provide an alternate method to attach the urls.

For this purpose use the following snippet::

    if getattr(settings, 'HTML5_APPCACHE_OVERRIDDEN_URLCONF', False):
        urlpatterns += patterns('',
            url(r'^my-url', include("my-app.urls")),
            ...
        )

Where *my-url* is the url where the apphook is attached to, and *my-app.urls* is
the urlconf of you application.
Repeat for every attached apphook and for every slug they are attached to.

.. _djangocms-plugins:

django CMS plugins
------------------

To enable cache invalidation for your own plugins, you must create an ``AppCache``
class for your plugin models too.

The example below is the implementation of an appcache for django CMS text plugin::

    from html5_appcache import appcache_registry
    from html5_appcache.appcache_base import BaseAppCache
    from cms.plugins.text.models import Text

    class CmsTextAppCache(BaseAppCache):
        models = (Text, )

        def signal_connector(self, instance, **kwargs):
            self.manager.reset_manifest()
    appcache_registry.register(CmsTextAppCache())
