The production server configuration
===================================

We want to treat our servers like cattle, not pets [1]. The effect of this, is that you should hopefully
never have to ssh to the servers to fix anything, if it's dead you kill it and fire up a new one.

We have an AMI with all users and salt-minion installed, so if anything happens, fire up one of those instances, run salt, and re-associate the elastic IP to point to the new server.

Note that all users account operations are performed as the first step in the salt step (by the key order: 1), so that you
don't always have to require the user account 'www' for example everywhere.

The AMI was created from a Ubuntu Server 12.04 LTS AMI, after having performed these steps:

- ssh in to the box with the master key (located in dropbox accounts db) and the 'ubuntu' user

- do the most elementary upgrades, so that salt doesnt have to work that hard

    $ sudo apt-get update
    $ sudo apt-get upgrade -y

- Install salt-minion (v0.17.0 is latest release as of 7.10.13)

    $ curl -L http://bootstrap.saltstack.org | sudo sh -s -- git develop

- Install up-to-date setuptools
    
    $ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | sudo python

- tar the salt and the pillar directories and scp it to the server:
    
    $ tar czf salt_and_pillar.tar.gz salt pillar
    $ scp salt_and_pillar.tar.gz slingsby:~
    $ ssh slingsby "sudo tar xf salt_and_pillar.tar.gz -C /srv && sudo salt-call --local state.sls users,sudo,ssh exclude=\"[{'id': 'ubuntu'}]\" && sudo rm -rf /srv/salt /srv/pillar"

Done. Save the result as an AMI, and use that AMI the next time (done from the web console).

## Notes

syncdb is only called on provision runs where slingsby is already installed (that is, everyone after the first one).
So the first time you're setting up a server you'll have to run `grunt build provision deploy provision`.

It's of uttermost importance that files with sensitive data (such as API_KEYS or similar) are managed with the
show_diff-flag set to False. Failing to do so might expose the keys in the travis build log. Silencing all
output from the provisioning at Travis might be another way to enforce this, but that would kill the entire log,
which might be nice to have.

## Debugging 101

Can't connect to an instance? First points to check:

- Have you assigned it a elastic IP? If you're using some hostname to connect to the instance (like ntnuita.no), you have to make sure that the IP associated with this DNS lookup points to the correct instance. This can be changed in the AWS console, under Elastic IPs.

- Have you assigned the instance to the correct security groups? Failing to do so will mean lead to you being stopped in the Amazon firewall.

- Are you connecting to the instance on the right port? We're running SSH on non-standard ports for increased security, make sure you try to connect to the right one.

# Extra

Just to keep it down somewhere, for creating a new DB instance, you fire it up, add a master account (see password in dropbox account db), and execute the following:

    $ mysql -u master -p -u <db-instance-endpoint>
    # Gives access to the slingsby user on the private VPC only
    CREATE USER 'slingsby'@'172.31.0.0/255.255.0.0' IDENTIFIED BY '<slingsby_pw as encrypted in .travis.yml>';
    GRANT ALL ON slingsby_rel.* TO 'slingsby'@'172.31.0.0/255.255.0.0';

[1]: http://www.theregister.co.uk/2013/03/18/servers_pets_or_cattle_cern/
