The production server configuration
===================================

Our server is a Raspberry Pi 2 running Raspbian hosted by ITEM, with a database at mysql.stud.ntnu.no and fileserver
at login.stud.ntnu.no. All software and configuration is handled by saltstack, so you should never have to install
anything manually. The only exception is when something has gone terribly wrong and you're bootstrapping the RPi from
scratch, which is the procedure explained here.

# Bootstrapping a new RPi

## Install Raspbian

We're now assuming that everything went bonkers and you have no hope of rescuing anything from the old memory card. If
the card still works, reformat it and follow the first guide you find on Google for how to install the latest Raspbian.

Once that's done, log in with the pi user (default password is `raspberry`, this user will be automatically deleted
later).

## Install saltstack

Install latest salt-minion:

    $ curl -L http://bootstrap.saltstack.org | sudo sh -s -- -U

Open `/etc/salt/minion` with your favorite text editor (like nano), and replace the current contents of the file with
this:

    id: ntnuita.no
    file_client: local
    grains:
      roles:
        - web

## Build and deploy

On your local machine, build the project and run an initial provisioning, installing all necessary software:
    
    $ grunt build
    $ python tools/secure_data.py decrypt
    $ fab provision:exclude_pi_user=True -H pi@<ip-address>

The decryption key for the secrets can be found in the Dropbox (look for Kontoer.kdbx, the password should have been
given to you if you're worthy).

This should install everything needed to run the webserver, configure the firewall and move SSH to a non-standard port,
in our case 3271, so on the next run you'll use your own user (which you had defined in `pillar/users/init.sls` before
you ran the previos command, right?):

    $ fab provision deploy -H <your-username>@<ip-address>:3271

Make sure the DNS is still correct (verify the output of `ip addr show` to `nslookup ntnuita.no`), if not you should
log on to [domeneshop](https://www.domeneshop.no/) and fix that.

The site should now be functional and you should verify this by opening it in your browser. If not, SSH in and check
some logs.

Done! Go fix some of the [issues](https://github.com/TelemarkAlpint/slingsby/issues), [Travis](https://travis-ci.org/)
will automatically push your updates to the server.

# Fileserver

User-uploaded media files are pushed to the fileserver as soon as any pre-processing is done (resizing images and
such). Since we can't create arbitrary accounts on the studorg server, slingsby needs access to a student account,
typically the webmaster. To make sure Travis can authorize as this user, copy Travis' pubkey (get it from
`pillar/users/init.sls`) into the user's `~/.ssh/authorized_keys` on the studorg server. Note that the user must have
access to `/home/groupswww/telemark`, which can be provided by an existing user from
`http://www.stud.ntnu.no/kundesenter/`.

The reason we use an external fileserver instead of hosting them ourselves on the RPi is because of size and backups.
NTNU maintains and takes backup of everything on the studorg-servers, as well as the database at mysql.stud.ntnu.no.
This means that there's no data loss for us if the SD card or something else is fried on the RPi, as we can just fire
up a new one. It's also a question of size, `/home/groupswww/telemark` + `/home/groups/telemark` is well above 50GB,
which is not fun to store on flimsy SD card.

# Notes

It's of uttermost importance that files with sensitive data (such as API_KEYS or similar) are managed with the
show_diff-flag set to False. Failing to do so might expose the keys in the travis build log. Silencing all
output from the provisioning at Travis might be another way to enforce this, but that would kill the entire log,
which might be nice to have.

# Debugging 101

Can't connect to the server? First points to check:

- Are you connecting to the instance on the right port? We're running SSH on non-standard port 3271 for increased
  security, make sure you specify this with either the `-p` argument to SSH, or put it in your `~/.ssh/config`.

- Is the IP correct? The RPi should have a static IP assigned to it from its MAC address, and is assigned the
  domain name `telemark.item.ntnu.no`. Is that IP the same as the one that ntnuita.no points to?

- Have you locked yourself out from the firewall? Tough luck. If you've managed to block SSH traffic or somehow
  moved the SSH port without updating the firewall, you're screwed. You need physical access to the device to fix this.
  See the current firewall policy with `sudo iptables -L -v -n`, try to figure out why stuff failed. It's recommended
  to never update saltstack in prod before you've tested that exact version in vagrant first, since a broken iptables
  module would probably lock you out.
