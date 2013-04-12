import webapp2
from google.appengine.ext import zipserve

# The official instructions for zipserve state to invoke the zipserve
# script directly using the module path in app.yaml, like so:
#
# - url: /archive/.*
#   script: $PYTHON_LIB/google/appengine/ext/zipserve
#
# As of App Engine 1.7.2, zipserve is only available as a CGI handler,
# not as a WSGIApplication instance.  The python27 runtime environment
# requires that all handlers mentioned in app.yaml be WSGIApplication
# instances if multithreading is enabled.  We can work around this by
# implementing our own WSGIApplication instance, calling
# zipserve.ZipHandler directly.

app = webapp2.WSGIApplication([('/([^/]+)/(.*)', zipserve.ZipHandler)])
