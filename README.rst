=====================
django-html5-appcache
=====================

.. image:: https://badge.fury.io/py/django-html5-appcache.png
        :target: http://badge.fury.io/py/django-html5-appcache

.. image:: https://travis-ci.org/nephila/django-html5-appcache.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-twitter

.. image:: https://pypip.in/d/django-html5-appcache/badge.png
        :target: https://crate.io/packages/django-html5-appcache?version=latest

.. image:: https://coveralls.io/repos/nephila/django-html5-appcache/badge.png?branch=master
        :target: https://coveralls.io/r/nephila/django-html5-appcache?branch=master

Application to manage HTML5 Appcache Manifest files for dynamic Django web applications.

While handy and quite simple in its structure, manifest file is quite burdensome
to keep up-to-date on dynamic websites.

``django-html5-appcache`` try to make this effortless, exploiting the batteries
included in Django to discover pages and assets as they are updated by the users.

While still in pre-alpha state it should be usable, at least for testing purposes.

Documentation is in progress.

As generating manifest file can be quite resource intensive for larger sites,
it uses the Django cache system.

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

See `Documentation <https://django-html5-appcache.readthedocs.org>`_ for further details.


.. image:: https://d2weczhvl823v0.cloudfront.net/nephila/django-html5-appcache/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

