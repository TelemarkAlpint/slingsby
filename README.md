Slingsby
========

[![Build Status](https://travis-ci.org/TelemarkAlpint/slingsby.png?branch=master)](https://travis-ci.org/TelemarkAlpint/slingsby)

A Django-powered webengine!

[Slingsby](http://en.wikipedia.org/wiki/William_Slingsby) was also the first man to conquer Store Vengetind in Romsdalen, along with hundreds of summits
in Jotunheimen. One of the hardest ski routes in Romsdalen, down the east side of Store Vengetind, is
named after his ascent.

Features
--------

* Write and publish articles
* User authentication integrated with ntnui.no
* Host events, let people sign up for events
* Users may suggest and vote on songs for our monday evening excersises
* Image gallery

Local development
-----------------

We're using virtualenvs when working on slingsby. First off, get pip and virtualenv if you haven't already:

    $ easy_install pip
    $ pip install virtualenv

Fetch the source code:

    $ git clone git@github.com:TelemarkAlpint/slingsby.git
    $ cd slingsby

Set up a virtualenv and install the python requirements:

    $ virtualenv venv_slingsby
    $ . venv_slingsby/bin/activate
    $ pip install -r requirements.txt

Slingsby uses [Grunt](http://gruntjs.com/) to run boring tasks that should be automated, like compiling SASS stylesheet and such.
To use grunt, you need NodeJS installed. Follow the instructions over at [NodeJS](http://nodejs.org/) to install it for your system.
The node package manager *npm* is bundled with recent versions of node, we're using npm to install grunt plugins we use. These are
defined in the package.json file.

Once you have node and npm installed, you should install the grunt-cli and all the grunt plugins:

    $ npm install -g grunt-cli
    $ npm install

Great! Now you can compile all the static files:

    $ grunt build

And now, you can start the devserver:

    $ python manage.py runserver --settings dev_settings

This should start the devserver at port 8000, browse to http://localhost:8000 to see it! Eventually you can use the grunt
task `grunt server`, which will run both `grunt watch` and start the devserver on port **80**. This also uses the `secret_settings.py`
module, so make sure to create that one first (see a couple of paragraphs further down for how and why to do that).

If you want to log in to the devserver, you need to start the devserver on port 80 and add a line to your hosts file to redirect 
requests to ntnuita.no to the devserver, since facebook will only authenticate towards that domain. Add this line to 
your hosts file (`/etc/hosts` on *nix, `C:\Windows\System32\Drivers\etc\hosts` on windows):

    127.0.0.1 ntnuita.no

Remmember to comment out this line when you're done testing, so that you'll be able to reach the actual pages later.

Note that for the Facebook auth to work, you need to have the correct SOCIAL_AUTH_FACEBOOK_SECRET set in your settings.
To achieve this you can either edit the dev_settings.py to include the correct key, but this might be a bit dangerous in
case you accidentally commit the change to the repo. A better solution might be to have a very simple file `secret_settings.py`
that only contains two lines:

    $ echo "from dev_settings import *" > secret_settings.py
    $ echo "SOCIAL_AUTH_FACEBOOK_SECRET='<secret>'" >> secret_settings.py

You might notice that there's not much in your database yet. You can of course start populating it manually by
creating articles, events, songs, sponsors etc, but that's boring, so instead you can find a complete db dump in the dropbox folder
that you can import into mysql, and then you should have an environment that quite closely matches what we have in production.

You should now be all set to start making your changes. If you're not the dev lead, submit your changes as pull requests on GitHub, and dev
lead will take a look at them, and hopefully admit your change into the repo.

About
-----

Our server is running on AWS, with deployments handled automatically by Travis CI. Static files are hosted on org.ntnu.no.

### Goals

We strive towards a clean, predictable URL scheme, and try to provide every resource as both HTML and JSON. Try browsing the site with Firefox,
with network.http.accept.default set to any string that prioritizes JSON over HTML, like text/html,application/json;q=1.1. This API is not entirely
documented yet and is subject to large changes, but if you want to program towards the site, this is how you want to do it.

A major goal for the site is to try to follow best practices as far as possible, as the site will be the first entry point to the "real world"
for many of the developers working on it, and we try to make that as easy as possible. This goes for both compliance to protocols like HTTP,
that GETS never should have any consquences, and we try to be RESTful, and it means trying to write Django as it's supposed to be written,
and it means writing easy to understand Python code.

On possible controversy might be that we don't document much code. I'm a huge fan of the "clean code" approach, and think that code should be
self-documenting. If you cannot express yourself clearly in code, you're not doing it simple enough or you do not understand what you're doing well
enough. Others might disagree, but with short functions with descriptive names, this has worked for us so far.

We also strive towards implementing as mush as possible with native HTML5 elements, like audio and video. We also hope to provide more responsive
pages soon, enhancing the mobile experience.

Dependencies
------------

See salt\slingsby\requirements.txt.
