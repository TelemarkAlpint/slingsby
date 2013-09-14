# This module is the main entry point to slingsby, as indicated in app.yaml.
# Request flow on app engine is app.yaml -> main.py -> slingsby.urls (approximately)

import slingsby

from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import os
import sys
import warnings

# Add a warning filter that will trigger warnings once for each location it's raised
warnings.simplefilter('default')

# Uncomment this to raise an exception on DeprecationWarnings, allowing you to see
# which line is causing the warning:
#warnings.simplefilter('error', DeprecationWarning)

# Capture warnings and log them
logging.captureWarnings(True)

# If we're in a activated VIRTUALENV the VIRTUAL_ENV env var points it's root
# and we can use that. Otherwise default to the one named 'venv_slingsby' in the
# folder as the slingsby package
virtualenv = os.environ.get('VIRTUAL_ENV', 'venv_slingsby')

windows = os.name == 'nt'

# Add dependencies from virtualenv to path to make sure app engine imports them
if windows:
    sys.path.insert(0, os.path.join(virtualenv, 'Lib', 'site-packages'))
else:
    sys.path.insert(0, os.path.join(virtualenv, 'lib', 'python2.7', 'site-packages'))


def main():

    # Run the WSGI handler
    run_wsgi_app(slingsby.application)

if __name__ == '__main__':
    main()
