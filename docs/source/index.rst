.. django-html5-appcache documentation master file, created by
   sphinx-quickstart on Sat Jun  1 23:51:58 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-html5-appcache's documentation!
=================================================

This document refers to version |release|

Application to manage `HTML5 Appcache Manifest <http://en.wikipedia.org/wiki/Cache_manifest_in_HTML5>`_
files for dynamic Django web applications.

While handy and quite simple in its structure, manifest files is quite burdensome
to keep up-to-date on dynamic websites.

``django-html5-appcache`` try to make this effortless, exploiting the batteries
included in Django to discover pages and assets as they are updated by the users.

See :ref:`Basic Concepts<basic-concepts>` for further details.


*******
Install
*******

.. toctree::
   :maxdepth: 1

   installation.rst
   configuration.rst
   changelog.rst

*****
Usage
*****

.. toctree::
   :maxdepth: 1

   concepts.rst
   appcache.rst
   djangocms.rst
   excluding.rst
   web.rst
   cli.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 1

   autodoc.rst
