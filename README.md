Slingsby
========

A Django-powered webengine!

[Slingsby](http://en.wikipedia.org/wiki/William_Slingsby) was also the first man to conquer Store Vengetind in Romsdalen, along with hundreds of summits
in Jotunheimen. One of the  hardest ski routes in Romsdalen, down the east side of Store Vengetind, is
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

Download the App Engine SDK and install it, instructions at [AppEngineSDK](https://developers.google.com/appengine/downloads).

Set up a virtualenv and install the python requirements:

    $ virtualenv virtualenv_slingsby
    $ . virtualenv_slingsby/bin/activate
    $ pip install -r requirements.txt
    $ deactivate

Why the deactivate? You don't need to be in your virtualenv to work on slingsby, since the path to the virtualenv is added
to the python path to make the App Engine SDK find it. As long as the SDK finds it you're golden. And by installing it in a
virtualenv, you didn't pollute your global python install. Neat!

Slingsby uses [Grunt](http://gruntjs.com/) to run boring tasks that should be automated, like compiling SASS stylesheet and such.
To use grunt, you need NodeJS installed. Follow the instructions over at [NodeJS](http://nodejs.org/) to install it for your system.
The node package manager *npm* is bundled with recent versions of node, we're using npm to install grunt plugins we use. These are
defined in the package.json file.

Once you have node and npm installed, you should install the grunt-cli and all the grunt plugins:

    $ cd slingsby
    $ npm install -g grunt-cli
    $ npm install

Great! Now you can compile all the static files:

    $ grunt build

What is left now? settings.py is looking for a file called secrets.py in the slingsby *package* (the slingsby folder within the
slingsby repo, package means that this is a python package (ie has a __init__.py), and can be imported with `import slingsby`),
this file should contain one variable called SECRET_KEY, which is used for signing cookies, to ensure they're not tampered with.
If you're not the dev lead, you can safely ignore this, but if you're taking over the project, you need to have something in that
file, since you'll be pushing code up to the webserver. If you're on a *nix platform you can either create a new key by using openssl
if you have it:

    $ openssl rand -base64 32

Or you can ask the previous dev lead to transfer you his file, that way we don't invalidate all the existing sessions (which has no
other consequence than people having to log in again).

You also need some database slingsby can use. In production we're using MySQL (through Google Cloud SQL), so I'd recommend using that
for local development too. If on a sensible system, setting up a local MySQL database is very easy:

    $ sudo apt-get install mysql # (or your favorite osx package manager, like brew or port)

In addition to MySQL, you'll need libmysqlclient-dev:

    $ sudo apt-get install libmysqlclient-dev
    
Now, install the mysql-python database connector for python inside of your virtual environment:

    $ . virtualenv_slingsby/bin/activate
    $ pip install mysql-python
    $ deactivate
    
Also, make sure that the password for the 'root' user in your mysql-server is set to '' (an empty string, i.e. nothing!)

Fetch the auth module from the Dropbox folder, and unzip it in the slingsby package. Once that's in place, you should be all set to start
the devserver, which can be found at the [Google App Engine site](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).

    $ dev_appserver.py .

This should start the devserver at port 8080, browse to http://localhost:8080 to see it! The App Engine SDK will also fire up a admin
panel at http://localhost:8000, which you can use for emptying the cache, among other things. Usually you can browse the datastore here,
but since we're using a separate MySQL database this won't be visible here.

Talking about data, you might notice that there's not much in your database yet. You can of course start populating it manually by
creating articles, events, songs, sponsors etc, but that's boring, so instead you can find a complete db dump in the dropbox folder
that you can import into mysql, and then you should have an environment that quite closely matches what we have in production.

You should now be all set to start making your changes. If you're not the dev lead, submit your changes as pull requests on GitHub, and dev
lead will take a look at them, and hopefully admit your change into the repo. If you're dev lead, to push changes to the server you should
make sure that you've incremented the version number in app.yaml, and then run

    $ appcfg.py update .

This will push the current state of the repo to the server. You should make sure you're on a clean branch when you're doing this, to avoid
pushing stuff unintended. Browse the new version of the code at <version number>.telemarkalpint.appspot.com, make sure everything looks OK,
and then swap the default version over to your new version in the App Engine console.

About
-----

Our servers are running on Google App Engine powered by Cloud SQL, with static files hosted on org.ntnu.no. We're running
Django 1.5.1.

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

* BeautifulSoup 4
* Pytz 2011k
* jQuery 1.9.1
* Modernizr 2.0.6
* WidgEditor 2008-03-01
* Zoombox
* dateutil 1.5
* Handlebars 1.0.0
* Compass
* Grunt
