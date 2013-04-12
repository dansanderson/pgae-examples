import datetime
from google.appengine.api import urlfetch

print 'Content-Type: text/html'
print ''

try:
    newsfeed = urlfetch.fetch('http://ae-book.appspot.com/blog/atom.xml/',
                              allow_truncated=False,
                              follow_redirects=False,
                              deadline=10)
    newsfeed_xml = newsfeed.content

    print '<p>Read PGAE blog feed (%d characters).</p>' % len(newsfeed_xml)
    
except urlfetch.Error, e:
    print '<p>urlfetch.Error: %s</p>' % e

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
