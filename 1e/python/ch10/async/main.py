import datetime
import time
from google.appengine.api import urlfetch

print 'Content-Type: text/html'
print ''

try:
    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(rpc, 'http://ae-book.appspot.com/blog/atom.xml/')

    # Do other things.
    time.sleep(2)

    newsfeed = rpc.get_result()
    newsfeed_xml = newsfeed.content

    print '<p>Read PGAE blog feed (%d characters).</p>' % len(newsfeed_xml)
    
except urlfetch.Error, e:
    print '<p>urlfetch.Error: %s</p>' % e

print '''
<p>Try these:</p>
<ul>
  <li><a href="/">a simple async call</a></li>
  <li><a href="/callbackobj">using a callback object</a></li>
  <li><a href="/callbackfunc">using a callback function</a></li>
</ul>
'''

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
