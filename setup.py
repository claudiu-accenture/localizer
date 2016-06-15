#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='Localize',
    version='0.2.5',
    install_requires=['requests', 'docopt', 'pyyaml'],
    packages=['localize'],
    entry_points={
        'console_scripts': [
            'localize=localize.main:main',
        ],
    }
)