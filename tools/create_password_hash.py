#!/usr/bin/env python

# Get a password hash in crypt form
# This script must be run in a *nix environment (the studorg server works)

from __future__ import print_function

import crypt
import os
import base64
import getpass

# How much we should slow down the hash computation. The higher the number of
# rounds, the harder it is to brute force the actual passwords if the shadow
# file is leaked.
ROUNDS = 10000

def main():
    password = 1
    password_repeat = 2
    while password != password_repeat:
        password = getpass.getpass('Enter password: ')
        password_repeat = getpass.getpass('Repeat password: ')
        if password != password_repeat:
            print('Passwords do not match, try again.')

    salt = base64.b64encode(os.urandom(6))
    print(crypt.crypt(password, "$6$rounds={rounds}${salt}".format(rounds=ROUNDS, salt=salt)))

if __name__ == '__main__':
    main()
