#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess
from os import path

def get_version():
    """ Set version to git hash for each build. This is used as a prefix for cache keys,
    to keep cached data separate between versions and preventing data bleed.
    """
    version = subprocess.check_output('git rev-parse --short HEAD').strip()
    return version

setup(
    name='slingsby',
    version=get_version(),
    author='NTNUI Telemark/Alpint',
    author_email='telemark-webmaster@ntnui.no',
    url='https://github.com/TelemarkAlpint/slingsby',
    description='NTNUI Telemark/Alpints website',
    packages=find_packages(),
    package_data={
        '': [
            path.join('templates', '*.html'),
            path.join('templates', '*', '*.html'),
            path.join('server-assets', '*'),
            path.join('test-data', '*.json'),
            'log_conf.yaml',
        ],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'manage.py = slingsby:manage'
        ]
    }
)
