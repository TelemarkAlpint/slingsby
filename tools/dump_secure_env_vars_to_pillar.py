#/usr/bin/env python
"""
Run this script to dump all secure env vars set by travis to a pillar file
which can then be used to render config files and stuff.

Will be dumped to pillar/secure/init.sls.
In your templates you can then do {{ pillar.get('SECRET_KEY') }} to insert the value.

Add any env var you want to include to TARGET_ENV_VARS.
"""

import os
import sys
import yaml

TARGET_ENV_VARS = [
    'FACEBOOK_API_KEY',
    'SECRET_KEY',
    'NEWRELIC_LICENSE_KEY',
]

_TARGET_FILE = os.path.join(os.path.dirname(__file__), '..', 'pillar', 'secure', 'init.sls')

def main():
    secure_vars = load_env_vars()
    dump_vars(secure_vars)

def load_env_vars():
    """ Load the env vars from the environment, and store them in a dictionary."""
    secure_vars = {}
    for key in TARGET_ENV_VARS:
        value = os.environ.get(key)
        if value is None:
            sys.stderr.write("Can't find var %s in current environ, make sure "
                "it's set in .travis.yml (with '- secure: <ENCRYPTED_VAR>' "
                "under the env.global key)" % key)
            sys.exit(1)
        secure_vars[key] = value
    return secure_vars

def dump_vars(env_vars):
    # Create target dir if it doesn't exist
    if not os.path.exists(os.path.dirname(_TARGET_FILE)):
        os.makedirs(os.path.dirname(_TARGET_FILE))

    with open(_TARGET_FILE, 'w') as target_file:
        yaml.dump(env_vars, target_file, default_flow_style=False)

if __name__ == '__main__':
    main()

