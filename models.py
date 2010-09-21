#These are our models
#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by MBS on 2010-08-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

import random
import datetime
import time
import logging

import helpers


class KeyValue(db.Model):
    k = db.StringProperty(required=True)
    v = db.StringProperty(required=True)
    
    @classmethod
    def get(cls, key, default=None):
        r = cls.all().filter('k =', key).get()
        if r:
            return r.v
        return default

    @classmethod
    def set(cls, key, value=None):
        r = cls.all().filter('k =', key).get()
        if r:
            r.v = value
            r.save()
            return r
        obj = cls(k=key, v=value)
        obj.save()
        return obj
