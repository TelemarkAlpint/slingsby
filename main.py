# Add dependencies from virtualenv to path to make sure app engine imports them
import sys
from os import path
sys.path.insert(0, path.join('virtualenv_slingsby', 'lib', 'python2.7', 'site-packages'))

import slingsby
from google.appengine.ext.webapp import util


def main():

    # Run the WSGI CGI handler with the slingsby app
    util.run_wsgi_app(slingsby.application)

if __name__ == '__main__':
    main()
