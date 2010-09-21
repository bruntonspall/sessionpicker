#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.dist import use_library
use_library('django', '1.1')
import helpers
import models
import settings
import appengine_utilities.sessions
import oauth
import logging



class MainHandler(webapp.RequestHandler):
    def get(self):
        user = None
        session = appengine_utilities.sessions.Session()
        username = session.get('user', None)
        if username:
            user = models.User.get_by_key_name(username)
        helpers.render_template(self, 'mainpage.html', {'user':user, 'sessions':models.Session.all()})

class TwitterSigninHandler(webapp.RequestHandler):
    def get(self):
        client = oauth.TwitterClient(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, 'http://sessionpicker.appspot.com/twitter/callback')
        self.redirect(client.get_authorization_url())
        
class TwitterCallbackHandler(webapp.RequestHandler):
    def get(self):
        client = oauth.TwitterClient(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, 'http://sessionpicker.appspot.com/twitter/callback')
        auth_token = self.request.get("oauth_token")
        auth_verifier = self.request.get("oauth_verifier")
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
        user = models.User.get_or_insert( user_info['username'],
           twitter_name = user_info['username'],
           display_name = user_info['name'],
           image_url = user_info['picture'],
           oauth_token = user_info['token'],
           oauth_secret = user_info['secret']
        )
        session = appengine_utilities.sessions.Session()
        session['user'] = user.twitter_name
        self.redirect('/')

class CreateSessionHandler(webapp.RequestHandler):
    def post(self):
        session = appengine_utilities.sessions.Session()
        user = helpers.get_session_user()
        title = self.request.get('title')
        description = self.request.get('description')
        logging.info('title: %s description: %s' % (title, description))
        session = models.Session(title=title, description=description, submitter=user).save()
        self.redirect('/')
class LikeSessionHandler(webapp.RequestHandler):
    def get(self, id):
        user = helpers.get_session_user()
        session = models.Session.get(id)
        if not session:
            self.redirect('/')
        #We only want to count a like once, if we find an object, don't increment the count
        obj = models.Like.all().filter('session =', session).filter('user =', user).get()
        if not obj:
            obj = models.Like(session=session, user=user).save()
            sess.likes += 1
            sess.save()        
        self.redirect('/')
        

class FakeUserHandler(webapp.RequestHandler):
    def get(self):
        session = appengine_utilities.sessions.Session()
        session['user'] = 'bruntonspall'
        self.redirect('/')
        
def main():
    application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/twitter/signin', TwitterSigninHandler),
    ('/twitter/callback', TwitterCallbackHandler),
    ('/session/new', CreateSessionHandler),
    ('/session/(?P<id>[a-zA-Z0-9-]+)/like', LikeSessionHandler),
#    ('/debug/fakeuser', FakeUserHandler),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':

    main()
