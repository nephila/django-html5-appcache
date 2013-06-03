.. _web_ui:

*************
Web interface
*************

Since 0.3.0 ``django-html5-appcache`` has a small web interface to check the
cache status and update the manifest file.

The ``appcache_icon`` templatag show the cache status icon and hooks it to an
ajax call that trigger the manifest update.


Installation
------------

Add the following lines to any template you want this to appear::

   {% load appcache_tags  %}
   ...
   ...
   {% appcache_link %}

.. _web_permissions:

Permissions
-----------

Both the view that shows the cache status and the view to update the manifest are
subject to specific permissions:

* ``can_view_cache_status``: required to access the view that show the cache status
* ``can_update_manifest``: required to trigger the manifest update

You need to explicitly add these permissions to any user who manages the appcache.

Both the views and the templatetag checks this permissions, so you can actually
write your own code to call the views and your code will still be safe.