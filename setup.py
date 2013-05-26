# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    author="Iacopo Spalletti",
    author_email='info@nephila.it',
    name='html5-appcache',
    version='0.1.0',
    description='HTML5 AppCache manifest generator',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='http://www.nephila.it',
    license='see LICENCE.txt',
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
