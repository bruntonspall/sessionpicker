import os
import datetime
import random
import google.appengine.api.labs.taskqueue 


from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api import users

import logging
from google.appengine.api.labs.taskqueue.taskqueue import Task
from google.appengine.api.labs import taskqueue


def render_admin_template(self, end_point, template_values):
    user = users.get_current_user()
    if user:
        template_values['greeting'] = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                    (user.nickname(), users.create_logout_url("/admin/")))

    render_template(self, end_point, template_values)

def render_template(self, end_point, template_values):
    path = os.path.join(os.path.dirname(__file__), "templates/" + end_point)
    self.response.out.write(template.render(path, template_values))
    
def slugify(word):
    return word.replace(' ', "-").lower()

