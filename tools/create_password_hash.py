#!/usr/bin/env python

# Get a password hash in crypt form
# This script must be run in a *nix environment (the studorg server works)

import crypt
import os
import base64
import getpass

ROUNDS = 10000

password = 1
password_repeat = 2
while password != password_repeat:
    password = getpass.getpass('Enter password: ')
    password_repeat = getpass.getpass('Repeat password: ')
    if password != password_repeat:
            print('Passwords do not match, try again.')

salt = base64.b64encode(os.urandom(6))
print(crypt.crypt(password, "$6$rounds={rounds}${salt}".format(rounds=ROUNDS, salt=salt)))
