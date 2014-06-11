Slingsby [![Build Status](https://travis-ci.org/TelemarkAlpint/slingsby.png?branch=master)](https://travis-ci.org/TelemarkAlpint/slingsby)
========

The homepage for [NTNUI Telemark/Alpint](http://ntnuita.no).

[Slingsby](http://en.wikipedia.org/wiki/William_Slingsby) was also the first man to conquer Store
Vengetind in Romsdalen, along with hundreds of summits in Jotunheimen. One of the hardest ski
routes in Romsdalen, down the east side of Store Vengetind, is named after his ascent.


Goals
-----

* Easily readable code (read: pythonic python and idiomatic javascript)
* Easy to get started for new developers
* Deployment handled automatically
* Well tested code
* Site works on all devices (but not necessarily look the same or provide the same experience)
* RESTful


About
-----

Our server is running on AWS, with deployments handled automatically by Travis CI.


Local development
-----------------

**tl;dr**: To setup a build environment and run the tests, check out `.travis.yml`. For more
in-depth explanation, read on.

We're advise using [virtualenvs](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) when
working on slingsby. First off, get pip and virtualenv if you haven't already:

    $ easy_install pip
    $ pip install virtualenv

Fetch the source code:

    $ git clone https://github.com/TelemarkAlpint/slingsby
    $ cd slingsby

Set up a virtualenv and install the python requirements:

    $ virtualenv venv
    $ . venv/bin/activate # windows: .\venv\Scripts\activate.bat
    $ pip install -r dev-requirements.txt

You now have everything needed to run the tests:

    $ python manage.py test

To run the server to test it in your browser, you need a little bit more work, because you need to
build the project first.

Slingsby uses [Grunt](http://gruntjs.com/) to run boring tasks that should be automated, like
compiling SASS stylesheet, minifying js and similar. To use grunt, you need NodeJS installed.
Follow the instructions over at [NodeJS](http://nodejs.org/) to install it for your system. The
node package manager *npm* is bundled with recent versions of node, we'll use that to install grunt
plugins we use. These are defined in the `package.json` file.

Once you have node and npm installed, you should install the grunt-cli, bower and all the grunt
plugins and frontend dependencies:

    $ npm install -g grunt-cli bower
    $ npm install
    $ bower install

You also need Compass for the stylesheets, which can be installed with
[RubyGems](https://rubygems.org/):

    $ gem install compass

Great! Now you can compile all the static files:

    $ grunt prep watch

Adding the `watch` task makes sure grunt will stay awake and listen for changes to the project
files, and re-run whatever has to be done for those files *and* reload your browser when done.
Magic!

And now, you can start the devserver:

    $ python manage.py runserver

This should start the devserver at port 8000, browse to `http://localhost:8000` to see it!
Starting the devserver like this will create a SQLite database you can use locally. Note that some
features will not work just like this, notably login, since you need to know our Facebook app
secret to be able to use that.

If you need to test login (and probably are lead developer of this project), you can decrypt the
secrets needed and start the devserver on port 80. You also need to add the following line to your
hosts file:

    127.0.0.1 ntnuita.local

Now add a very simple file `secret_settings.py` that only contains two lines:

    $ echo "from dev_settings import *" > secret_settings.py
    $ echo "SOCIAL_AUTH_FACEBOOK_SECRET='<secret>'" >> secret_settings.py

You can now start the devserver and use Facebook login:

    $ python manage.py runserver 80 --settings secret_settings

Hack away!


Testing on a server
-------------------

To test that stuff works in the same environment (or rather, very similar) to the one in
production, you can start a local machine with all the same software we're using in production by
using [VirtualBox](https://www.virtualbox.org/) and [Vagrant](http://www.vagrantup.com/). Once you
have installed the two, simply execute the following to start your VM and deploy the app to it:

    $ vagrant up
    $ fab deploy_vagrant

(This requires the app to have been built already: run `grunt build` first). You now have a server
running the app behind nginx, with uwsgi doing the heavy lifting, memcached doing caching, etc.


Dependencies
------------

Handled by four (!) different package managers for three different purposes: `pip` handles python
libraries we use, defined in `salt/slingsby/requirements.txt`. `bower` handles frontend
dependencies like jQuery and Handlebars, defined in `bower.json`. `npm` handles build dependencies
like grunt and the grunt plugins for SASS transiling and js minification, defined in
`package.json`. And lastly, you also need RubyGems (`gem`) be able to install compass, which is
needed by grunt-compass.
