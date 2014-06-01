# pylint: disable=unused-wildcard-import,wildcard-import

from dev_settings import *

import yaml
import sys

secrets_file = os.path.join(os.path.dirname(__file__), 'pillar', 'secure', 'init.sls')

with open(secrets_file) as secrets_fh:
    secret_data = yaml.load(secrets_fh)

if secret_data:
    local_variables = locals()
    for key, val in secret_data.items():
        local_variables[key] = val
else:
    print('Error! Secrets needs to be decrypted before you can use them.\nRun ' +
        '`python tools/secure_data.py decrypt` to do so.\nThe secret key can be found in ' +
        'Kontoer.kdbx in the webkom dropbox')
    sys.exit(1)
