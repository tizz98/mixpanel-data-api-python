#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md', 'r') as f:
        long_description = f.read()

from mixpanel_data import __version__

setup(
    name='mixpanel_data',
    version=__version__,
    description='A simple python wrapper for the Mixpanel Data Export API',
    long_description=long_description,
    url='https://github.com/tizz98/mixpanel-data-api-python',
    download_url='https://github.com/tizz98/mixpanel-data-api-python/'
                 'tarball/%s' % __version__,
    author='Elijah Wilson',
    license='GNU General Public License v3.0',
    packages=['mixpanel_data'],
    keywords="mixpanel data export api",
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'six',
    ],
)
