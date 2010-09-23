Session Picker
==============

What does it do?
----------------

It acts as a simple wall for an unconference that can be used before the unconference kicks off.
The idea is that before your unconfernce starts some of your users can put their sessions up on it, and other users can 'like' the session which means that they would like to attend.  Then when the day starts you can take the 6 or 7 most popular sessions and put them in the biggest rooms.  That is all!

How do I get it working locally?
--------------------------------

OAUth is a bit tricky, so local stuff might not work right.
go to http://dev.twitter.com and register a new application.  Set it's callback url to be http://localhost:8000 or wherever you are hosting it.
copy the settings.py into local_settings.py and set your Consumer key and secret.
Hit your local copy, and click signin and click allow.  If you are lucky you'll be redirected back and logged into your own system.
Once you publish it to the web, update twitters callback url to the correct url.

How is it licensed?
-------------------

Lets say GPLv3, contact me if you have queries or want a different license

ToDo
----

There are some plans for this:

 * Admin pages
 * A Session Report
 * Be generic, so handle more than one conference.
   * Probably not within one instance, but within multiple instances
 * For more traditional conferences, don't allow the creation of new conferences except by admins, but allow like from anyone.
 * For real Barcamp style conferences, allow the sessions to be laid out in time/room grid view, and dragged around - replaces the wall totally
 * In some cases, show and order sessions by the number of likes
 
