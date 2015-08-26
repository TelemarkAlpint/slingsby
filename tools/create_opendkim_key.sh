#!/bin/sh

# Generate a new opendkim key

set -e

domain=ntnuita.no
selector=$(date +"%Y%m%d")
key_size=2048

privkey_fifo="/tmp/$selector.private"
mkfifo --mode=0600 "$privkey_fifo"

# Using openssl directly together with named pipe instead of going through
# opendkim-genkey to prevent key from hitting disk
echo "Add this to your DNS config: $selector._domainkey.$domain IN TXT \"v=DKIM1; k=rsa; p=$(openssl rsa -in $privkey_fifo -pubout 2>/dev/null | tail -n +2 | head -n -1 | tr -d '\n')\"" &
openssl genrsa $key_size 2>/dev/null | tee $privkey_fifo | python tools/secure_data.py encrypt OPENDKIM_KEY_$selector=-

# Clean up
rm $privkey_fifo
