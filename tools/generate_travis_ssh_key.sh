#!/bin/bash

#############################################################################

# This script creates a new SSH key for Travis, and encrypts the private part
# with travis' public key for the repo so that travis can decrypt it and use
# it to push changes to the prod server on changes to master.

# USAGE:
# ./generate_travis_ssh_key.sh
# Follow instructions given

# Use this if the travis SSH key gets compromised, or just do it regularly
# out of good habit.

# Requires the travis gem to be installed (gem install travis)
# Windows users recommended to try vagrant (see TelemarkAlpint/telemark-vm)

#############################################################################


# Generate a new keypair
ssh-keygen -t rsa -b 4096 -N "" -q -f /tmp/new_travis_key

# Print the public key
echo -e "Copy this into pillar/users.sls, as travis' new SSH key:\n"
python -c "with open('/tmp/new_travis_key.pub') as f: print(' '.join(f.read().split()[:2]))"

# Make a base64 encoded version of the private key
base64 --wrap=0 /tmp/new_travis_key > /tmp/new_travis_base64

# Split the base64 encoded key into parts of size 100B (~approx max size travis
# will encrypt), feed each part to `travis encrypt`, print the result.
ENCRYPTION_FILTER="echo \$(echo \"- secure: \")\$(travis encrypt \"\$FILE='\`cat $FILE\`'\" -r TelemarkAlpint/slingsby)"
echo -e "\nReplace the existing travis private SSH key part in .travis.yml with this:\n"
split --bytes=100 --numeric-suffixes --suffix-length=2 --filter="$ENCRYPTION_FILTER" /tmp/new_travis_base64 id_rsa_ 2>/dev/null

# Clean up
rm /tmp/new_travis_*
