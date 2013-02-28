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

About
-----

Our servers are running on Google App Engine, with static files hosted on org.ntnu.no. We're running
Django-nonrel for the time being, but we're eventually aiming for Django 1.5 and Google Cloud SQL.

### Goals

We strive towards a clean, predictable URL scheme, and try to provide every resource as both HTML and JSON. Try browsing the site with Firefox,
with network.http.accept.default set to any string that prioritizes JSON over HTML, like text/html,application/json;q=1.1. This is not entirely
documented yet, and might change in the future, but if you want to program towards the site, this is how you want to do it.

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

* BeautifulSoup 3.2.0
* Pytz 2011k
* jQuery 1.8.1
* Modernizr 2.0.6
* WidgEditor 2008-03-01
* Zoombox
* dateutil 1.5
* Handlebars 1.0.0-rc3