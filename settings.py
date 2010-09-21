#OAUTH Twitter keys
CONSUMER_KEY=""
CONSUMER_SECRET=""

try:
    from local_settings import *
except ImportError:
    raise Exception("Please create a local_settings.py with your real settings in")