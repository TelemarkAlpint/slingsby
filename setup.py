#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

setup(
    name='slingsby',
    version='1.0.0',
    author='NTNUI Telemark/Alpint',
    author_email='telemark-webmaster@ntnui.no',
    url='https://github.com/TelemarkAlpint/slingsby',
    description='NTNUI Telemark/Alpints website',
    packages=find_packages(),
    package_data={
        '': [
            path.join('templates', '*.html'),
            path.join('templates', '*', '*.html'),
            path.join('templates', '*', '*.js'),
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
