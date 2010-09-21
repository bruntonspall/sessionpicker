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
import helpers
import models
import settings
import appengine_utilities.sessions
import oauth

class MainHandler(webapp.RequestHandler):
    def get(self):
        session = appengine_utilities.sessions.Session()
        user = session.get('user', None)
        helpers.render_template(self, 'mainpage.html', {'user':user})

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
        user = models.User.get_or_insert(
           twitter_name = user_info['username'],
           display_name = user_info['name'],
           image_url = user_info['picture'],
           oauth_token = user_info['token'],
           oauth_secret = user_info['secret']
        )
        session = appengine_utilities.sessions.Session()
        session['user'] = user
        self.redirect('/')

def main():
    application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/twitter/signin', TwitterSigninHandler),
    ('/twitter/callback', TwitterCallbackHandler),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
