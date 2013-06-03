.. _basic-concepts:

**************
Basic Concepts
**************

``django-html5-appcache`` leverages django ``cache``, ``test`` and ``signals``
frameworks to explore project pages and assets and generate an appcache manifest
file.

Manifest file generation
========================

The manifest file is generated collecting all the cached urls and exploring them
using the test client to gather asset urls and including them in the manifest
itself.

This can be quite resource intensive, so the manifest file is saved in the cache;
the view that actually delivers the file manifest to the browser can thus use
the cache to serve it with no performance impact.

The manifest file is generated out-of-band using a
:ref:`django command <command-cli>` so you can execute the command manually or in
a cron job.
Since 0.3.0 a view is provided, see :ref:`web_ui`_

Cache invalidation
------------------

Whenever a registered model is saved or deleted (see :ref:`appcache` on how to enable
this for your application), manifest cache is marked as **dirty**; this has no
immediate effect on the manifest file served, as the oudated copy is still served.

URL discovery
-------------

Using sitemap
#############

``django-html5-appcache`` uses the sitemap as a primary mean to discover urls in
the web application.

This is a two steps process:

1. get the sitemap and extract the urls declared
2. visit each url and extract the asset urls

Customizing urls
################

Additional to the sitemap method above, you can define your own
:ref:`custom url list<custom-urls>`; in this case, it's your duty to define the
list of assets in those urls.
