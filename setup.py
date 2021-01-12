#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name='hidsltools',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    python_requires='>=3.8',
    packages=['hidsltools'],
    entry_points={
        'console_scripts': [
            'hireset = hidsltools.reset:main',
            'hirestore = hidsltools.restore:main',
            'mkhidslimg = hidsltools.image:main',
        ],
    },
    url='https://github.com/homeinfogmbh/hidsltools',
    license='GPLv3',
    description='Image tools for HOMEINFO Digital Signage Linux systems.'
)
