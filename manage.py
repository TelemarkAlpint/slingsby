#!/usr/bin/env python
from django.core.management import execute_manager
import sys

try:
    import slingsby.settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'slingsby/settings.py' (or it's causing ImportError!)")
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(slingsby.settings)
