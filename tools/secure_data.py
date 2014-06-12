#!/usr/bin/env python
"""
    Encrypt/decrypt secrets for storage in salt/pillar.
"""

import argparse
import base64
import Crypto.Random
import Crypto.Cipher
import getpass
import os
import os.path
import yaml


def main():
    args = get_args()
    if args.key:
        # Key provided on CLI, use that
        base64_secret_key = args.key
    else:
        base64_secret_key = getpass.getpass('Enter key: ')
    secret_key = base64.b64decode(base64_secret_key)
    if args.mode == 'encrypt':
        encrypt(secret_key, args.values_to_encrypt)
    else:
        decrypt(secret_key)

def get_args():
    parser = argparse.ArgumentParser(description='Encrypt/decrypt secrets for storage in ' +
        'salt/pillar. If no arguments is given, will decrypt salt/secure/init.sls to ' +
        'pillar/secure/init.sls (and prompt for the key)')
    parser.add_argument('mode',
        choices=['encrypt', 'decrypt'],
        default='decrypt',
        help='Choose whether to encrypt or decrypt. Default: %(default)s')
    parser.add_argument('values_to_encrypt', nargs='?',
        help='New value to encrypt. Format is KEY=VALUE, output will be ' +
            'KEY=<base64-encoded encrypted data>. If you prefix the value with @, contents will ' +
            'read from the filename following the @. (eg. SSH_KEY=@id_rsa)')
    parser.add_argument('-k', '--key',
        help='The secret key to use. Will be prompted for if not provided')
    return parser.parse_args()


def encrypt(secret_key, value):
    key, val = value.split('=', 1)
    print 'Encryping %s...' % key
    if val[0] == '@':
        with open(val[1:]) as plaintext_fh:
            plaintext = plaintext_fh.read()
    else:
        plaintext = val
    ciphertext = aes_encrypt(secret_key, plaintext)
    encrypted_data = {
        key: ciphertext,
    }
    target_file = os.path.join(os.path.dirname(__file__), '..', 'salt', 'secure', 'init.sls')
    with open(target_file, 'a') as target_fh:
        yaml.dump(encrypted_data, target_fh, default_flow_style=False)
    print 'Done. The encrypted data has been appended to salt/secure/init.sls'


def decrypt(secret_key):
    print 'Decrypting...'
    source_file = os.path.join(os.path.dirname(__file__), '..', 'salt', 'secure', 'init.sls')
    with open(source_file) as fh:
        encrypted_data = yaml.load(fh.read())
    plaintext_data = {}
    for key, val in encrypted_data.items():
        plaintext_data[key] = aes_decrypt(secret_key, val)
    output_file = os.path.join(os.path.dirname(__file__), '..', 'pillar', 'secure', 'init.sls')
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(output_file, 'w') as fh:
        yaml.dump(plaintext_data, fh, default_flow_style=False)
    print 'Done. Data has been decrypted to pillar/secure/init.sls'


def aes_encrypt(key, plaintext):
    iv = Crypto.Random.new().read(Crypto.Cipher.AES.block_size) # pylint: disable=invalid-name
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    ciphertext = iv + cipher.encrypt(plaintext.encode('utf-8'))
    b64_ciphertext = base64.b64encode(ciphertext)
    return b64_ciphertext


def aes_decrypt(key, b64_ciphertext):
    iv_ciphertext = base64.b64decode(b64_ciphertext)
    iv = iv_ciphertext[:Crypto.Cipher.AES.block_size] # pylint: disable=invalid-name
    ciphertext = iv_ciphertext[Crypto.Cipher.AES.block_size:]
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


if __name__ == '__main__':
    main()
