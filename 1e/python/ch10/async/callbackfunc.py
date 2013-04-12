import datetime
import time
from google.appengine.api import urlfetch

def process_results(rpc):
    try:
        results = rpc.get_result()
        print '<p>Read PGAE blog feed (%d characters).</p>' % len(results.content)

    except urlfetch.Error, e:
        print '<p>urlfetch.Error: %s</p>' % e

def create_callback(rpc):
    # Use a funciton to define the scope for the lambda.
    return lambda: process_results(rpc)


print 'Content-Type: text/html'
print ''

# Prepare RPC.
#
# We set the callback attribute of the RPC object after the RPC object
# has been created, so we can pass the RPC object to
# create_callback().
rpc = urlfetch.create_rpc()
rpc.callback = create_callback(rpc)
urlfetch.make_fetch_call(rpc, 'http://ae-book.appspot.com/blog/atom.xml/')

# Do other things.
time.sleep(2)

# Tell RPCs to finish up.
rpc.wait()


print '''
<p>Try these:</p>
<ul>
  <li><a href="/">a simple async call</a></li>
  <li><a href="/callbackobj">using a callback object</a></li>
  <li><a href="/callbackfunc">using a callback function</a></li>
</ul>
'''

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
