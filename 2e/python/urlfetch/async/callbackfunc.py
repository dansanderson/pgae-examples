import datetime
import time
import webapp2
from google.appengine.api import urlfetch

def process_results(handler, rpc):
    try:
        results = rpc.get_result()
        handler.response.write('<p>Read PGAE blog feed (%d characters).</p>'
                               % len(results.content))

    except urlfetch.Error, e:
        handler.response.write('<p>urlfetch.Error: %s</p>' % e)

def create_callback(handler, rpc):
    # Use a funciton to define the scope for the lambda.
    return lambda: process_results(handler, rpc)


class MainPage(webapp2.RequestHandler):
    def get(self):

        # Prepare RPC.
        #
        # We set the callback attribute of the RPC object after the RPC object
        # has been created, so we can pass the RPC object to
        # create_callback().
        rpc = urlfetch.create_rpc()
        rpc.callback = create_callback(self, rpc)
        urlfetch.make_fetch_call(rpc, 'http://ae-book.appspot.com/blog/atom.xml')
        
        # Do other things.
        time.sleep(2)
        
        # Tell RPCs to finish up.
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


app = webapp2.WSGIApplication([('/callbackfunc', MainPage)], debug=True)
