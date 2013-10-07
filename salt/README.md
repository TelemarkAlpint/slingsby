The production server configuration
===================================

We want to treat our servers like cattle, not pets [1]. The effect of this, is that you should hopefully
never have to ssh to the servers to fix anything, if it's dead you kill it and fire up a new one.

We have an AMI with all users and salt-minion installed, so if anything happens, fire up one of those instances, run salt, and re-associate the elastic IP to point to the new server.

Note that all users account operations are performed as the first step in the salt step (by the key order: 1), so that you
don't always have to require the user account 'www' for example everywhere.

The AMI was created from a Ubuntu Server 12.04 LTS AMI, after having performed these steps:

- ssh in to the box with some keypair and the 'ubuntu' user

- do the most elementary upgrades, so that salt doesnt have to work that hard

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get dist-upgrade

- Install salt-minion (v0.17.0 is latest release as of 7.10.13)

    $ curl -L http://bootstrap.saltstack.org | sudo sh -s -- git v0.17.0

- Install up-to-date setuptools
    
    $ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | sudo python

- tar the slingsby/salt directory and scp it to the server:
    
    $ tar czf salt.tar.gz salt # assuming cd=slingsby
    $ scp salt.tar.gz <your_username>@<public_dns_of_new_instance>:~
    $ ssh <your_username>@<public_dns_of_new_instance>
    $ tar xf salt.tar.gz -C /srv

- Set up users and sudoers:

    $ sudo salt-call --local state.sls users,sudo

- Log out, log in using your own user, run `sudo salt-call --local state.sls users' again to remove the ubuntu user.

Done. Save the result as an AMI, and use that AMI the next time (done from the web console).

## Notes

syncdb is only called on provision runs where slingsby is already installed (that is, everyone after the first one).
So the first time you're setting up a server you'll have to run `grunt build provision deploy provision`.

It's of uttermost importance that files with sensitive data (such as API_KEYS or similar) are managed with the
show_diff-flag set to False. Failing to do so might expose the keys in the travis build log. Silencing all
output from the provisioning at Travis might be another way to enforce this, but that would kill the entire log,
which might be nice to have.

[1]: http://www.theregister.co.uk/2013/03/18/servers_pets_or_cattle_cern/
