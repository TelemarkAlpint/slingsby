#!/usr/bin/env python
import slingsby
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_settings')

if __name__ == '__main__':
    slingsby.manage()
