from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-OE1',
    version=get_version('mopidy_oe1/__init__.py'),
    url='https://github.com/tischlda/mopidy-oe1',
    license='Apache License, Version 2.0',
    author='David Tischler',
    author_email='david@tischler.io',
    description='Mopidy backend to access the Austrian radio station OE1.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'simplejson',
        'python-dateutil',
        'beaker',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock >= 1.0',
    ],
    entry_points={
        'mopidy.ext': [
            'oe1 = mopidy_oe1:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
