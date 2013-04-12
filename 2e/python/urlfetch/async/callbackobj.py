import datetime
import time
import webapp2
from google.appengine.api import urlfetch

class CatalogUpdater(object):
    def prepare_urlfetch_rpc(self, handler):
        self.handler = handler
        self.rpc = urlfetch.create_rpc(callback=self.process_results)
        urlfetch.make_fetch_call(self.rpc, 'http://ae-book.appspot.com/blog/atom.xml')
        return self.rpc

    def process_results(self):
        try:
            results = self.rpc.get_result()
            self.handler.response.write(
                '<p>Read PGAE blog feed (%d characters).</p>'
                % len(results.content))

        except urlfetch.Error, e:
            self.handler.response.write('<p>urlfetch.Error: %s</p>' % e)


class MainPage(webapp2.RequestHandler):
    def get(self):

        # Prepare RPCs.
        rpcs = []
        catalog_updater = CatalogUpdater()
        rpcs.append(catalog_updater.prepare_urlfetch_rpc(self))
        
        # Do other things.
        time.sleep(2)
        
        # Tell all pending RPCs to finish up.
        for rpc in rpcs:
            rpc.wait()
        
        self.response.write('''
        <p>Try these:</p>
        <ul>
          <li><a href="/">a simple async call</a></li>
          <li><a href="/callbackobj">using a callback object</a></li>
          <li><a href="/callbackfunc">using a callback function</a></li>
        </ul>
        ''')
        
        self.response.write('<p>The time is: %s</p>'
                            % str(datetime.datetime.now()))


app = webapp2.WSGIApplication([('/callbackobj', MainPage)], debug=True)
