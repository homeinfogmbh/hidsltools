#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name='hidsl',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    python_requires='>=3.8',
    packages=['hidsl'],
    scripts=['scripts/hireset', 'scripts/hirestore', 'scripts/mkhidslimg'],
    url='https://github.com/homeinfogmbh/hidsltools',
    license='GPLv3',
    description='Image tools for HOMEINFO Digital Signage Linux systems.'
)
