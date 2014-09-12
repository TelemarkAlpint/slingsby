Tools
=====

These are some small utilities that might come in handy during development.


check_for_updates.py
--------------------

Scans your virtualenv to see if any packages are out of date.


coverage_to_gh_pages.sh
-----------------------

Used by Travis to deploy the directory `./cover` to the `gh-pages` branch.


generate_travis_ssh_key.sh
--------------------------

Run this to generate a new SSH key for travis and output it as secure env vars that can be included
in `.travis.yml`. The public key must also be added to travis' account under `pillar/users`.


secure_data.py
--------------

Used to encrypt and decrypt secret values that are stored in `./salt/secure/init.sls`. Decryption
key can be found in the styre-dropbox `Kontoer.kdbx` file.
