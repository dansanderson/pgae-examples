import datetime
import urllib2
from google.appengine.api import urlfetch

# Be sure to run this example using Python 2.5.  With Python 2.6, you
# may get an error regarding the "ctypes" library when running the
# development server.

print 'Content-Type: text/html'
print ''

try:
    newsfeed = urllib2.urlopen('http://ae-book.appspot.com/blog/atom.xml/')
    newsfeed_xml = newsfeed.read()

    print '<p>Read PGAE blog feed (%d characters).</p>' % len(newsfeed_xml)
    
except urllib2.URLError, e:
    print '<p>urllib2.URLError: %s</p>' % e

except urlfetch.Error, e:
    print '<p>urlfetch.Error: %s</p>' % e

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
