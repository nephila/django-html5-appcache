# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: WWW/HTTP :: Site Management',
]


setup(
    author="Iacopo Spalletti",
    author_email='info@nephila.it',
    name='django-html5-appcache',
    version='0.4.0',
    description='HTML5 AppCache manifest generator',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='http://www.nephila.it',
    download_url='https://github.com/nephila/django-html5-appcache',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        "Django",
        "lxml",
        "html5lib"
    ],
    packages=find_packages(),
    include_package_data=True,
    test_suite = "html5_appcache.test_utils.run_tests",
    zip_safe=False,
    dependency_links=[
    ],
)
