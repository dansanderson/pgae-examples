import datetime
import time
from google.appengine.api import urlfetch

class CatalogUpdater(object):
    def prepare_urlfetch_rpc(self):
        self.rpc = urlfetch.create_rpc(callback=self.process_results)
        urlfetch.make_fetch_call(self.rpc, 'http://ae-book.appspot.com/blog/atom.xml/')
        return self.rpc

    def process_results(self):
        try:
            results = self.rpc.get_result()
            print '<p>Read PGAE blog feed (%d characters).</p>' % len(results.content)

        except urlfetch.Error, e:
            print '<p>urlfetch.Error: %s</p>' % e


print 'Content-Type: text/html'
print ''

# Prepare RPCs.
rpcs = []
catalog_updater = CatalogUpdater()
rpcs.append(catalog_updater.prepare_urlfetch_rpc())

# Do other things.
time.sleep(2)

# Tell all pending RPCs to finish up.
for rpc in rpcs:
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
