*********
Changelog
*********


0.4.1 (2014-01-05)
------------------

* Django 1.6 support

0.4 (2013-06-26)
------------------

* Manifest file is now authentication-sensitive (see docs)
* Add data-appcache optin parameter
* Add HTML5_APPCACHE_EXCLUDE_URL setting
* Fix HTML5_APPCACHE_NETWORK_URL and HTML5_APPCACHE_FALLBACK_URL settings

0.3.1 (2013-06-08)
------------------

* Fix view-generated manifest

0.3.0 (2013-06-06)
------------------
.. warning::
    0.3.0 introduces migrations. Run ``migrate html5_appcache`` on upgrade

* Special permissions for management views
* Templatetag to show the chache status and update the manifest (see :ref:`web_ui`)
* ``HTML5_APPCACHE_DISABLE`` parameter to disable manifest file (see :ref:`configuration`)


0.2.2 (2013-06-02)
------------------
* Fixes issue with Google Chrome

0.2.0 (2013-06-02)
------------------
* Initial release
