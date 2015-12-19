#!/usr/bin/env python

# Get a password hash in crypt form

from __future__ import print_function

import pcrypt
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

    print(pcrypt.crypt(password, rounds=ROUNDS))

if __name__ == '__main__':
    main()
