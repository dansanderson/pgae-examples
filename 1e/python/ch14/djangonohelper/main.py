from google.appengine.dist import use_library
use_library('django', '1.1')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
from google.appengine.ext.webapp import util

def main():
    # Run Django via WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
